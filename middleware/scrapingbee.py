class ScrapingBeeMiddleware:
    def __init__(self, api_keys, enabled=False):
        self.api_keys = api_keys
        self.enabled = enabled
        self.key_pool = cycle(self.api_keys)
        self.current_key = next(self.key_pool)
        self.request_count = 0
        self.rotation_threshold = int(os.getenv('ROTATION_THRESHOLD', '150'))
        logger.info(f"ScrapingBee Middleware initialized with enabled={enabled}")

    @classmethod
    def from_crawler(cls, crawler):
        api_keys = [key.strip() for key in os.getenv('SCRAPINGBEE_API_KEYS', '').split(',') if key.strip()]
        enabled = crawler.settings.get('SCRAPINGBEE_ENABLED', False)

        if enabled and not api_keys:
            raise ValueError("No ScrapingBee API keys found in .env file")

        return cls(api_keys=api_keys, enabled=enabled)

    def rotate_key(self):
        self.current_key = next(self.key_pool)
        self.request_count = 0
        logger.info("Rotated to next ScrapingBee API key")

    def process_request(self, request, spider):
        if not self.enabled:
            return None

        if 'scrapingbee.com' in request.url:
            return None

        original_url = request.url

        if self.request_count >= self.rotation_threshold:
            self.rotate_key()

        try:
            bee_url = (
                f"https://app.scrapingbee.com/api/v1/"
                f"?api_key={self.current_key}"
                f"&url={quote(original_url)}"
                f"&render_js=false"
                f"&premium_proxy=false"
            )

            self.request_count += 1
            logger.info(f"Making ScrapingBee request for: {original_url}")

            return request.replace(
                url=bee_url,
                dont_filter=True,
                meta={**request.meta, 'original_url': original_url}
            )

        except Exception as e:
            logger.error(f"Error constructing ScrapingBee request: {e}")
            return request

    def process_response(self, request, response, spider):
        original_url = request.meta.get('original_url')
        if not original_url:
            return response

        if response.status in [401, 403, 405]:
            logger.warning(f"Received {response.status} from ScrapingBee for {original_url}, rotating key")
            self.rotate_key()
            return Request(original_url, dont_filter=True, meta={'original_url': original_url})

        return response.replace(url=original_url)
