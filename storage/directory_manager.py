from pathlib import Path
import logging
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

class DirectoryManager:
    def __init__(self, base_dir="Data", tracker_dir="Tracker", timezone='Asia/Kolkata'):
        self.base_dir = Path(base_dir)
        self.tracker_dir = Path(tracker_dir)
        self.timezone = pytz.timezone(timezone)
        self._setup_directories()

    def _setup_directories(self):
        """Create necessary directories"""
        self.base_dir.mkdir(exist_ok=True)
        self.tracker_dir.mkdir(exist_ok=True)

        # Create today's date directory
        today = datetime.now(self.timezone).strftime("%d-%m-%Y")
        self.today_dir = self.base_dir / today
        self.today_dir.mkdir(exist_ok=True)

        logger.info(f"Created/verified directory structure: {self.today_dir}")

    @property
    def data_dir(self):
        return self.today_dir

    @property
    def trackers_dir(self):
        return self.tracker_dir
