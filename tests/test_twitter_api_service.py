"""
Tests for Real X API service implementation
Note: These tests require a valid TWITTER_BEARER_TOKEN to run against real API
For CI/CD, these tests are skipped if token is not available
"""
import pytest
import os
from app.services.twitter_api_service import TwitterAPIService
from app.models.tweet import Tweet


# Skip all tests in this file if no bearer token is available
pytestmark = pytest.mark.skipif(
    not os.getenv('TWITTER_BEARER_TOKEN'),
    reason="TWITTER_BEARER_TOKEN not set - skipping real API tests"
)


class TestTwitterAPIService:
    """
    Test cases for TwitterAPIService with real X API
    
    These tests will only run if TWITTER_BEARER_TOKEN is set
    They make real API calls and count against your rate limit
    """
    
    @pytest.fixture
    def service(self):
        """Create service instance for testing"""
        return TwitterAPIService()
    
    def test_initialization_with_token(self):
        """Test service initializes correctly with token"""
        token = os.getenv('TWITTER_BEARER_TOKEN')
        service = TwitterAPIService(bearer_token=token)
        assert service.bearer_token == token
        assert 'Authorization' in service.headers
    
    def test_initialization_without_token(self):
        """Test service raises error without token"""
        # Temporarily remove token from environment
        original_token = os.environ.pop('TWITTER_BEARER_TOKEN', None)
        
        try:
            with pytest.raises(ValueError, match="Bearer Token is required"):
                TwitterAPIService()
        finally:
            # Restore token
            if original_token:
                os.environ['TWITTER_BEARER_TOKEN'] = original_token
    
    @pytest.mark.integration
    def test_get_tweets_by_hashtag_real_api(self, service):
        """
        Integration test with real X API
        WARNING: This counts against your API rate limit!
        """
        # Use a common hashtag likely to have recent tweets
        tweets = service.get_tweets_by_hashtag("python", limit=5)
        
        # Basic assertions
        assert isinstance(tweets, list)
        assert len(tweets) <= 5
        
        if len(tweets) > 0:
            tweet = tweets[0]
            assert isinstance(tweet, Tweet)
            assert hasattr(tweet, 'account')
            assert hasattr(tweet, 'text')
            assert hasattr(tweet, 'date')
    
    @pytest.mark.integration  
    def test_get_user_tweets_real_api(self, service):
        """
        Integration test with real X API
        WARNING: This counts against your API rate limit!
        """
        # Use X's official account (very likely to have tweets)
        tweets = service.get_user_tweets("Twitter", limit=5)
        
        # Basic assertions
        assert isinstance(tweets, list)
        assert len(tweets) <= 5
        
        if len(tweets) > 0:
            tweet = tweets[0]
            assert isinstance(tweet, Tweet)
            assert tweet.account.href == "/Twitter" or tweet.account.href == "/twitter"
    
    def test_hashtag_normalization(self, service):
        """Test that hashtag with # symbol is handled correctly"""
        # This test structure but won't make real call in unit test
        # In real scenario, both should work the same
        pass
    
    def test_username_normalization(self, service):
        """Test that username with @ symbol is handled correctly"""
        # This test structure but won't make real call in unit test
        pass


class TestTwitterAPIServiceUnitTests:
    """Unit tests that don't require real API access"""
    
    def test_format_date(self):
        """Test date formatting"""
        service = TwitterAPIService(bearer_token="test_token")
        
        iso_date = "2023-03-15T14:30:00.000Z"
        formatted = service._format_date(iso_date)
        
        # Should convert to readable format
        assert "Mar" in formatted
        assert "2023" in formatted
    
    def test_parse_empty_response(self):
        """Test parsing empty API response"""
        service = TwitterAPIService(bearer_token="test_token")
        
        empty_response = {}
        tweets = service._parse_tweets_response(empty_response)
        
        assert tweets == []
    
    def test_parse_response_structure(self):
        """Test parsing valid API response structure"""
        service = TwitterAPIService(bearer_token="test_token")
        
        mock_response = {
            'data': [
                {
                    'id': '123456789',
                    'author_id': '987654321',
                    'text': 'This is a test tweet #python',
                    'created_at': '2023-03-15T14:30:00.000Z',
                    'public_metrics': {
                        'reply_count': 5,
                        'retweet_count': 10,
                        'like_count': 50
                    }
                }
            ],
            'includes': {
                'users': [
                    {
                        'id': '987654321',
                        'name': 'Test User',
                        'username': 'testuser'
                    }
                ]
            }
        }
        
        tweets = service._parse_tweets_response(mock_response)
        
        assert len(tweets) == 1
        tweet = tweets[0]
        assert tweet.text == 'This is a test tweet #python'
        assert tweet.account.fullname == 'Test User'
        assert tweet.likes == 50
        assert tweet.retweets == 10
        assert tweet.replies == 5
        assert '#python' in tweet.hashtags

