"""
Application configuration
"""
import os


class Config:
    """Base configuration"""
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # API settings
    DEFAULT_TWEET_LIMIT = 30
    MAX_TWEET_LIMIT = 100
    MIN_TWEET_LIMIT = 1
    
    # Twitter/X scraping settings
    TWITTER_BASE_URL = "https://twitter.com"
    REQUEST_TIMEOUT = 10
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Config dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


