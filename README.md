# CI.HLS

A configurable web scraping framework built with Scrapy for extracting news articles from multiple sources.


## Key Features

- 🛠️ Source-specific configuration via JSON
- 🧩 Modular architecture for easy extension
- 🐝 ScrapingBee integration for proxy management
- 📂 Atomic file operations for data integrity
- ⚙️ Robust error handling and logging
- 🔗 URL tracking for deduplication
- 🌍 Environment-based configuration
- ✉️ Custom headers support in the config

## Directory Structure
```
ci.hls/
├── config/
│   ├── __init__.py
│   └── selectors/
│       ├── __init__.py
│       ├── sources/
│       │   └── pr_news.json
│       └── selector_manager.py
├── spiders/
│   ├── __init__.py
│   └── dynamic_spider.py
├── middleware/
│   ├── __init__.py
│   └── scrapingbee.py
├── extractors/
│   ├── __init__.py
│   └── field_extractor.py
├── storage/
│   ├── __init__.py
│   ├── json_handler.py
│   └── directory_manager.py
├── utils/
│   ├── __init__.py
│   └── url_utils.py
├── Data/              # Created during runtime
├── Tracker/           # Created during runtime
├── logs/              # Log files
├── .env               # Environment variables
├── .gitignore
├── requirements.txt
└── run.py
```

## Prerequisites
- Python 3.12+
- pip for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rishic5i/ci.hls.git
cd ci.hls
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
Create `.env` file with the following variables:
```env
SCRAPINGBEE_API_KEYS=key1,key2,key3
ROTATION_THRESHOLD=150
LOG_LEVEL=INFO
LOG_DIR=logs
CONCURRENT_REQUESTS=2
DOWNLOAD_DELAY=2
```

## Usage

### List All Available Sources
```bash
python run.py --list-sources
```

### Run All Sources
```bash
python run.py
```

### Run Specific Source
```bash
python run.py --source pr_news
```

### Run with ScrapingBee
```bash
# Run all sources with ScrapingBee
python run.py --use-scrapingbee

# Run specific source with ScrapingBee
python run.py --source pr_news --use-scrapingbee
```

### Environment Options
```bash
# Development mode (default)
python run.py --env dev --source pr_news

# Production mode
python run.py --env prod --source pr_news

# Combine with ScrapingBee
python run.py --env prod --source pr_news --use-scrapingbee
```

## Adding New Sources

Add your source configuration in `config/selectors/sources/` (e.g., `your_source.json`):
```json
{
    "Source Name": {
        "type": "catalog",
        "url": [
            "https://example.com/news-url"
        ],
        "selectors": {
            "source": "SOURCE_NAME",
            "news": "xpath_for_news_list",
            "abstract": "xpath_for_abstract",
            "published_date": "xpath_for_date",
            "news_link": "xpath_for_link"
        },
        "news_selector": {
            "title": "xpath_for_title",
            "article_date": "xpath_for_article_date",
            "author": "xpath_for_author",
            "content": "xpath_for_content"
        }
    }
}
```

## Output Structure

### Data Storage
```
Data/
└── DD-MM-YYYY/
    └── source_name.json
```

### Output Format
```json
{
    "source": "source_name",
    "category": "category",
    "published_date": "formatted_date",
    "article_date": "formatted_date",
    "title": "article_title",
    "author": "author_name",
    "abstract": "article_abstract",
    "detailed_news": "article_content",
    "article_url": "url",
    "attachments": "attachment_url",
    "contacts": "contact_details",
    "scraping_date": "YYYY-MM-DD",
    "scraping_time": "HH:MM"
}
```

## URL Tracking
- URLs are tracked in `Tracker/source_name_tracker.json`
- Prevents duplicate scraping of articles

## Error Handling
- Comprehensive error logging in the logs directory
- Automatic retry for failed requests
- Proxy rotation with ScrapingBee integration

## Contributing
1. Fork the repository
2. Create your feature branch
3. Submit pull request

## License
MIT
