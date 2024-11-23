def get_settings(use_scrapingbee=False):
    """Get Scrapy settings with optional ScrapingBee integration"""
    settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'SCRAPINGBEE_ENABLED': use_scrapingbee,
        'CONCURRENT_REQUESTS': 2,
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 60,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 401, 403, 404, 408, 405],
        'LOG_LEVEL': 'INFO',
        'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S',
    }

    if use_scrapingbee:
        settings['DOWNLOADER_MIDDLEWARES'] = {
            'middleware.scrapingbee.ScrapingBeeMiddleware': 725
        }

    return settings

# Optional: Add custom settings for different environments
def get_development_settings():
    settings = get_settings()
    settings.update({
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 3,
        'LOG_LEVEL': 'DEBUG'
    })
    return settings

def get_production_settings():
    settings = get_settings()
    settings.update({
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 1,
        'LOG_LEVEL': 'INFO'
    })
    return settings
