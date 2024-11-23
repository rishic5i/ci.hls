import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class URLTracker:
    def __init__(self, tracker_dir):
        self.tracker_dir = Path(tracker_dir)
        self.tracker_dir.mkdir(exist_ok=True)
        self.trackers = {}

    def load_tracker(self, source_name):
        """Load URL tracker for a source"""
        tracker_file = self.tracker_dir / f"{source_name}_tracker.json"
        try:
            if tracker_file.exists():
                with open(tracker_file, 'r', encoding='utf-8') as f:
                    self.trackers[source_name] = set(json.load(f))
            else:
                self.trackers[source_name] = set()
            return self.trackers[source_name]
        except Exception as e:
            logger.error(f"Error loading tracker for {source_name}: {e}")
            return set()

    def save_tracker(self, source_name):
        """Save URL tracker for a source"""
        if source_name not in self.trackers:
            return

        tracker_file = self.tracker_dir / f"{source_name}_tracker.json"
        try:
            with open(tracker_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.trackers[source_name]), f, indent=4)
            logger.info(f"Updated tracker for {source_name}")
        except Exception as e:
            logger.error(f"Error saving tracker for {source_name}: {e}")

    def add_url(self, source_name, url):
        """Add URL to tracker"""
        if source_name not in self.trackers:
            self.load_tracker(source_name)
        self.trackers[source_name].add(url)

    def remove_url(self, source_name, url):
        """Remove URL from tracker"""
        if source_name in self.trackers:
            self.trackers[source_name].discard(url)

    def url_exists(self, source_name, url):
        """Check if URL exists in tracker"""
        return source_name in self.trackers and url in self.trackers[source_name]
