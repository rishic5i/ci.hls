import argparse
from scrapy.crawler import CrawlerProcess
from config.settings import get_settings, get_development_settings, get_production_settings
from config.logging_config import setup_logging
from spiders.dynamic_spider import DynamicSpider
from config.selectors.selector_manager import SelectorManager
from dotenv import load_dotenv

def main():
    parser = argparse.ArgumentParser(description='Run the news scraper')
    parser.add_argument('--use-scrapingbee', action='store_true',
                       help='Enable ScrapingBee integration')
    parser.add_argument('--env', choices=['dev', 'prod'], default='dev',
                       help='Environment to run in (dev/prod)')
    parser.add_argument('--source', help='Specific source to scrape (e.g., pr_news)')
    parser.add_argument('--list-sources', action='store_true',
                       help='List all available sources')
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Initialize selector manager
    selector_manager = SelectorManager()

    # List sources if requested
    if args.list_sources:
        sources = selector_manager.get_all_sources()
        print("Available sources:")
        for source in sources:
            print(f"  - {source}")
        return

    # Add debug info
    if args.source:
        print(f"Running scraper for source: {args.source}")
        config_file = selector_manager.selectors_dir / f"{args.source}.json"
        print(f"Looking for config file at: {config_file}")
        if not config_file.exists():
            print(f"Error: Config file not found at {config_file}")
            return

    # Setup logging and settings
    if args.env == 'dev':
        loggers = setup_logging(log_level='DEBUG')
        settings = get_development_settings()
    else:
        loggers = setup_logging(log_level='INFO')
        settings = get_production_settings()

    settings['SCRAPINGBEE_ENABLED'] = args.use_scrapingbee

    # Initialize crawler process
    process = CrawlerProcess(settings)

    # Start the spider with specific source or all sources
    process.crawl(
        DynamicSpider,
        source_name=args.source,  # Will be None if not specified
        selector_manager=selector_manager,
        use_scrapingbee=args.use_scrapingbee
    )

    process.start()

if __name__ == '__main__':
    main()
