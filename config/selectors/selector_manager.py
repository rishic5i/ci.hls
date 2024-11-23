import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SelectorManager:
    def __init__(self):
        self.selectors_dir = Path(__file__).parent / 'sources'
        self.selectors_cache = {}

    def load_source_config(self, source_name):
        """Load config for a specific source"""
        source_file = self.selectors_dir / f"{source_name}.json"
        logger.debug(f"Looking for config file at: {source_file}")

        if not source_file.exists():
            logger.error(f"Config file not found: {source_file}")
            raise FileNotFoundError(f"No config file found for {source_name}")

        if source_name not in self.selectors_cache:
            logger.debug(f"Loading config file for {source_name}")
            try:
                with open(source_file) as f:
                    content = f.read()
                    logger.debug(f"File content: {content[:100]}...")  # First 100 chars
                    self.selectors_cache[source_name] = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in {source_file}: {e}")
                raise

        return self.selectors_cache[source_name]

    def get_all_sources(self):
        """Get list of all available source names"""
        return [f.stem for f in self.selectors_dir.glob("*.json")]

    def load_all_configs(self):
        """Load all source configurations"""
        all_configs = {}
        for source_name in self.get_all_sources():
            try:
                all_configs[source_name] = self.load_source_config(source_name)
            except Exception as e:
                logger.error(f"Error loading config for {source_name}: {e}")
        return all_configs

    def validate_config(self, config):
        """Validate a source configuration"""
        required_fields = {
            'type', 'url', 'selectors', 'news_selector'
        }
        required_selectors = {
            'source', 'news', 'news_link'
        }

        # Check main structure
        if not all(field in config for field in required_fields):
            missing = required_fields - set(config.keys())
            raise ValueError(f"Missing required fields: {missing}")

        # Check selectors
        if not all(field in config['selectors'] for field in required_selectors):
            missing = required_selectors - set(config['selectors'].keys())
            raise ValueError(f"Missing required selectors: {missing}")

        return True
