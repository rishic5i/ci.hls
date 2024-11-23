# CI.HLS

A configurable, scalable web scraping framework built with Scrapy for extracting news articles from multiple sources. The system supports dynamic source configuration, proxy integration, and robust error handling.

## Architecture Overview

### Core Components
```
ci.hls/
│
├── spiders/            # Core scraping logic
├── middleware/         # Request/Response processing
├── trackers/          # URL deduplication
├── extractors/        # Field extraction logic
├── storage/           # Data persistence
├── utils/             # Helper utilities
├── config/            # Configuration management
│   └── selectors/     # Source-specific configs
└── Data/              # Output storage
```

### Key Features
- Source-specific configuration via JSON
- Modular architecture for easy extension
- ScrapingBee integration for proxy management
- Atomic file operations for data integrity
- Robust error handling and logging
- URL tracking for deduplication
- Environment-based configuration

## Technical Prerequisites

### System Requirements
- Python 3.12+
- pip/pipenv for dependency management
- Git for version control

### Dependencies
```bash
scrapy>=2.11.0
python-dotenv>=1.0.0
pytz>=2024.1
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rishic5i/ci.hls.git
cd modular-scraper
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configurations
```

## Configuration

### Environment Variables
```dotenv
SCRAPINGBEE_API_KEYS=key1,key2,key3
ROTATION_THRESHOLD=150
LOG_LEVEL=INFO
LOG_DIR=logs
CONCURRENT_REQUESTS=2
DOWNLOAD_DELAY=2
```

### Adding New Sources
1. Create source configuration in `config/selectors/sources/`:
```json
{
    "Source_Name": {
        "type": "catalog",
        "url": ["https://example.com/news"],
        "selectors": {
            "source": "unique_source_id",
            "news": "xpath_for_news_items",
            "news_link": "xpath_for_links"
        },
        "news_selector": {
            "title": "xpath_for_title",
            "content": "xpath_for_content"
        }
    }
}
```

## Usage

### Basic Usage
```bash
# Run scraper for all sources
python run.py

# Run specific source
python run.py --source source_name

# List available sources
python run.py --list-sources
```

### Environment Options
```bash
# Development mode
python run.py --env dev

# Production mode
python run.py --env prod --use-scrapingbee
```

## Development Guidelines

### Adding New Features
1. Create feature branch from main:
```bash
git checkout -b feature/feature-name
```

2. Follow modular structure:
- Add new extractors in `extractors/`
- Add new middleware in `middleware/`
- Add source configs in `config/selectors/sources/`

3. Update tests:
```bash
python -m pytest tests/
```

### Error Handling
- Use try-except blocks with specific exceptions
- Log errors with appropriate levels
- Implement graceful fallbacks
- Handle network timeouts and retries

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function arguments
- Document complex logic
- Use meaningful variable names

## Data Structure

### Output Format
```json
{
    "source": "source_name",
    "category": "news_category",
    "published_date": "YYYY-MM-DD",
    "title": "article_title",
    "content": "article_content",
    "url": "article_url",
    "scraping_date": "YYYY-MM-DD",
    "scraping_time": "HH:MM"
}
```

### Storage Pattern
```
Data/
└── DD-MM-YYYY/
    └── source_name.json
```

## Error Handling and Logging

### Log Levels
- DEBUG: Detailed debugging information
- INFO: General operational information
- WARNING: Warning messages for non-critical issues
- ERROR: Error messages for failed operations
- CRITICAL: Critical errors requiring immediate attention

### Log Files
```
logs/
├── scraper.log      # General logging
└── error.log        # Error-specific logging
```

## Performance Considerations

### Optimization
- Use selector caching
- Implement request delays
- Configure concurrent requests
- Rotate proxy settings

### Memory Management
- Implement batch processing
- Use file streaming for large datasets
- Clear URL trackers periodically

## Monitoring and Maintenance

### Health Checks
- Monitor log files for errors
- Track success rates
- Monitor proxy performance
- Check data integrity

### Regular Maintenance
- Update selectors if source HTML changes
- Rotate API keys
- Archive old data
- Clean up tracker files

## Troubleshooting

### Common Issues
1. Selector failures:
   - Check source HTML structure
   - Validate XPath expressions
   - Review selector configuration

2. Rate limiting:
   - Adjust DOWNLOAD_DELAY
   - Rotate proxy settings
   - Check API quotas

3. Data integrity:
   - Verify JSON structure
   - Check file permissions
   - Validate output format

## Contributing

1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Submit pull request

## License

MIT License - See LICENSE file for details
