from pathlib import Path
from typing import Dict, Any
import yaml
import logging

class Config:
    def __init__(self, config_path: str = "src/config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[Any, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {self.config_path}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[Any, Any]:
        """Return default configuration"""
        return {
            "paths": {
                "bronze": "data/bronze",
                "silver": "data/silver",
                "gold": "data/gold"
            },
            "processing": {
                "batch_size": 1000,
                "max_retries": 3,
                "retry_delay": 1  # seconds
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(levelname)s - %(message)s",
                "file": "logs/pipeline.log"
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
