import scrapy
import json
import logging
from datetime import datetime
from pathlib import Path
from utils.url_utils import URLUtils
from utils.date_utils import parse_date
from storage.directory_manager import DirectoryManager
from storage.json_handler import JSONHandler
from extractors.field_extractor import FieldExtractor

logger = logging.getLogger(__name__)

class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'

    def __init__(self, selector_manager, source_name=None, use_scrapingbee=False, *args, **kwargs):
        super(DynamicSpider, self).__init__(*args, **kwargs)

        # Initialize components
        self.dir_manager = DirectoryManager()
        self.json_handler = JSONHandler(self.dir_manager)
        self.selector_manager = selector_manager

        try:
            # Load configs based on source_name
            if source_name:
                source_config = self.selector_manager.load_source_config(source_name)
                # Get the actual config from the first key (e.g., "PR News")
                source_key = list(source_config.keys())[0]
                self.config = {
                    source_name: source_config[source_key]  # Get the nested config
                }
            else:
                all_configs = self.selector_manager.load_all_configs()
                self.config = {}
                for source_name, source_config in all_configs.items():
                    source_key = list(source_config.keys())[0]
                    self.config[source_name] = source_config[source_key]

            # Initialize URL trackers
            self.url_trackers = {}
            for source_name, source_config in self.config.items():
                tracker_name = source_config['selectors']['source']
                self.url_trackers[tracker_name] = self.load_url_tracker(tracker_name)

            # Set start URLs
            self.start_urls = []
            for source_config in self.config.values():
                self.start_urls.extend(source_config['url'])

            logger.info(f"Starting spider with URLs: {self.start_urls}")

        except Exception as e:
            logger.error(f"Error initializing spider: {e}")
            raise

    def start_requests(self):
        """Override start_requests to include headers"""
        for url in self.start_urls:
            config = self.get_config(url)
            headers = config.get('headers', {})
            yield scrapy.Request(url, headers=headers, dont_filter=True)

    def load_url_tracker(self, source_name):
        """Load URL tracker for a source"""
        tracker_file = self.dir_manager.trackers_dir / f"{source_name}_tracker.json"
        try:
            if tracker_file.exists():
                with open(tracker_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            return set()
        except Exception as e:
            logger.error(f"Error loading tracker for {source_name}: {e}")
            return set()

    def save_url_tracker(self, source_name):
        """Save URL tracker for a source"""
        tracker_file = self.dir_manager.trackers_dir / f"{source_name}_tracker.json"
        try:
            with open(tracker_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.url_trackers[source_name]), f, indent=4)
            logger.info(f"Updated tracker for {source_name}")
        except Exception as e:
            logger.error(f"Error saving tracker for {source_name}: {e}")

    def get_config(self, url):
        """Get configuration for a given URL"""
        try:
            original_url = URLUtils.extract_original_url(url)
            for source_name, settings in self.config.items():
                if any(base_url in original_url for base_url in settings['url']):
                    return settings
        except Exception as e:
            logger.error(f"Error in get_config: {e}")
        return None

    def parse(self, response):
        original_url = response.meta.get('original_url', response.url)
        site_config = self.get_config(original_url)

        if site_config:
            logger.info(f"Parsing: {original_url} using config for {site_config['selectors']['source']}")
            return self.parse_catalog(response, site_config['selectors'], site_config['news_selector'])
        else:
            logger.warning(f"No configuration found for URL: {original_url}")

    def parse_catalog(self, response, selectors, news_selector):
        try:
            news = response.xpath(selectors['news'])
            original_url = response.meta.get('original_url', response.url)
            base_url = URLUtils.get_base_url(original_url)
            source = selectors['source']
            category = URLUtils.extract_category(original_url)

            config = self.get_config(original_url)
            headers = config.get('headers', {})

            logger.info(f"Catalog scraped from {original_url}")

            for article in news:
                # Extract fields
                abstract = FieldExtractor.extract_field(article, selectors, 'abstract')
                published_date = FieldExtractor.extract_field(article, selectors, 'published_date')
                if published_date:
                    published_date = parse_date(published_date)

                # Get article URL
                link = article.xpath(selectors['news_link']).get()
                if not link:
                    continue

                absolute_url = URLUtils.get_absolute_url(base_url, link, source)

                if absolute_url in self.url_trackers[source]:
                    logger.info(f"Skipping already scraped URL: {absolute_url}")
                    continue

                logger.info(f"New URL found for {source}: {absolute_url}")
                yield response.follow(
                    absolute_url,
                    self.parse_news,
                    headers=headers,
                    cb_kwargs={
                        'selectors': selectors,
                        'news_selector': news_selector,
                        'source': source,
                        'abstract': abstract,
                        'published_date': published_date,
                        'category': category
                    }
                )

        except Exception as e:
            logger.error(f"Error in parse_catalog: {str(e)}")

    def parse_news(self, response, selectors, news_selector, source, abstract, published_date, category):
        try:
            original_url = response.meta.get('original_url', response.url)

            if original_url in self.url_trackers[source]:
                logger.info(f"Already scraped URL (double-check): {original_url}")
                return

            self.url_trackers[source].add(original_url)
            base_url = URLUtils.get_base_url(original_url)

            # Extract all fields
            news_details = {
                'source': source,
                'category': category,
                'published_date': published_date,
                'article_date': None,
                'title': FieldExtractor.extract_field(response, news_selector, 'title'),
                'author': FieldExtractor.extract_field(response, news_selector, 'author'),
                'abstract': abstract,
                'detailed_news': FieldExtractor.extract_field(response, news_selector, 'content'),
                'article_url': original_url,
                'attachments': FieldExtractor.extract_field(response, news_selector, 'attachment', base_url),
                'contacts': FieldExtractor.extract_field(response, news_selector, 'contact_details'),
                'scraping_date': datetime.now().strftime("%Y-%m-%d"),
                'scraping_time': datetime.now().strftime("%H:%M")
            }

            # Process article date if present
            article_date = FieldExtractor.extract_field(response, news_selector, 'article_date')
            if article_date:
                news_details['article_date'] = parse_date(article_date)

            # Save data
            self.json_handler.safely_write_json(news_details, source)
            self.save_url_tracker(source)

            yield news_details

        except Exception as e:
            logger.error(f"Error parsing news page {response.url}: {e}")
            if original_url in self.url_trackers[source]:
                self.url_trackers[source].remove(original_url)

    def closed(self, reason):
        """Handle spider closure"""
        for source_name, tracker in self.url_trackers.items():
            self.save_url_tracker(source_name)
            logger.info(f"Final tracker save for {source_name}")
