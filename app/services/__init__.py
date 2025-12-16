"""
Service layer package
"""
import os
from app.services.twitter_service import TwitterService
from app.services.twitter_mock_service import TwitterMockService
from app.services.twitter_api_service import TwitterAPIService


def get_twitter_service():
    """
    Factory function to get the appropriate Twitter service implementation
    
    Behavior:
    - If TWITTER_BEARER_TOKEN is set: Use real X API v2
    - Otherwise: Use mock service for development/testing
    
    To use real X API:
    1. Sign up at https://developer.x.com
    2. Get your Bearer Token
    3. Set environment variable: export TWITTER_BEARER_TOKEN="your_token_here"
    
    Returns:
        TwitterService instance (either TwitterAPIService or TwitterMockService)
    """
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if bearer_token:
        # Use real X API if token is configured
        return TwitterAPIService(bearer_token)
    else:
        # Fall back to mock service for development
        return TwitterMockService()


__all__ = ['TwitterService', 'TwitterMockService', 'TwitterAPIService', 'get_twitter_service']


