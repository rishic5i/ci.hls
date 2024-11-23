from urllib.parse import urljoin, urlparse, parse_qs, unquote

class URLUtils:
    @staticmethod
    def get_base_url(url):
        """Extract base URL (protocol + domain)"""
        return '/'.join(url.split('/')[:3])

    @staticmethod
    def extract_category(url):
        """Extract category from URL"""
        parts = url.split('/')
        category = parts[-1]
        if category == '':
            category = parts[-2]
        return category

    @staticmethod
    def get_absolute_url(base_url, relative_url, source=None):
        """Get absolute URL with special case handling"""
        absolute_url = urljoin(base_url, relative_url)

        # Handle special cases for different sources
        if source == 'innocare':
            abs_url = urljoin(base_url, 'en')
            return abs_url + relative_url
        elif source == 'cilletron':
            abs_url = urljoin(base_url, 'en-us/company/media-center/press-release/')
            return abs_url + relative_url

        return absolute_url

    @staticmethod
    def extract_original_url(scrapingbee_url):
        """Extract original URL from ScrapingBee URL"""
        if 'scrapingbee.com' not in scrapingbee_url:
            return scrapingbee_url

        parsed = urlparse(scrapingbee_url)
        params = parse_qs(parsed.query)
        if 'url' in params:
            return unquote(params['url'][0])
        return scrapingbee_url
