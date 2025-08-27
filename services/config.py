import os
from typing import Dict, Any


class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    DATA_FILE_PATH = "data/progress.json"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATA_FILE_PATH = "data/progress.json"


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATA_FILE_PATH = "data/test_progress.json"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    DATA_FILE_PATH = os.getenv("DATA_FILE_PATH", "data/progress.json")


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """Get configuration class based on environment."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])