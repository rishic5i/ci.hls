import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class JSONHandler:
    def __init__(self, directory_manager):
        self.dir_manager = directory_manager

    def safely_write_json(self, data, source):
        """Safely write JSON data to file with error handling and atomic writing"""
        try:
            filename = f"{source}.json"
            file_path = self.dir_manager.data_dir / filename

            # Load existing data or create new array
            existing_data = []
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                        if not isinstance(existing_data, list):
                            existing_data = [existing_data]
                except json.JSONDecodeError:
                    logger.warning(f"Couldn't decode existing file {file_path}, starting fresh")

            # Append new data
            existing_data.append(data)

            # Write to temporary file first
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)

            # Atomic rename
            temp_path.replace(file_path)
            logger.info(f"Successfully wrote data to {file_path}")

        except Exception as e:
            logger.error(f"Error writing JSON file {filename}: {e}")
            raise
