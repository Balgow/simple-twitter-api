"""
Tests for Twitter service implementations
"""
import pytest
from app.services.twitter_mock_service import TwitterMockService
from app.models.tweet import Tweet


class TestTwitterMockService:
    """Test cases for TwitterMockService"""
    
    @pytest.fixture
    def service(self):
        """Create service instance for testing"""
        return TwitterMockService()
    
    def test_get_tweets_by_hashtag_returns_tweets(self, service):
        """Test that get_tweets_by_hashtag returns Tweet objects"""
        tweets = service.get_tweets_by_hashtag("python", limit=5)
        
        assert len(tweets) == 5
        assert all(isinstance(tweet, Tweet) for tweet in tweets)
    
    def test_get_tweets_by_hashtag_includes_hashtag(self, service):
        """Test that returned tweets include the requested hashtag"""
        tweets = service.get_tweets_by_hashtag("python", limit=5)
        
        for tweet in tweets:
            # Hashtags should be lowercase for comparison
            tweet_hashtags_lower = [tag.lower() for tag in tweet.hashtags]
            assert "#python" in tweet_hashtags_lower
    
    def test_get_tweets_by_hashtag_respects_limit(self, service):
        """Test that get_tweets_by_hashtag respects the limit parameter"""
        for limit in [5, 10, 20]:
            tweets = service.get_tweets_by_hashtag("python", limit=limit)
            assert len(tweets) == limit
    
    def test_get_tweets_by_hashtag_empty_hashtag(self, service):
        """Test that empty hashtag raises ValueError"""
        with pytest.raises(ValueError, match="Hashtag cannot be empty"):
            service.get_tweets_by_hashtag("", limit=5)
    
    def test_get_tweets_by_hashtag_normalizes_hashtag(self, service):
        """Test that hashtag is normalized (# removed)"""
        tweets = service.get_tweets_by_hashtag("#python", limit=5)
        assert len(tweets) == 5
    
    def test_get_user_tweets_returns_tweets(self, service):
        """Test that get_user_tweets returns Tweet objects"""
        tweets = service.get_user_tweets("twitter", limit=5)
        
        assert len(tweets) == 5
        assert all(isinstance(tweet, Tweet) for tweet in tweets)
    
    def test_get_user_tweets_respects_limit(self, service):
        """Test that get_user_tweets respects the limit parameter"""
        for limit in [5, 10, 20]:
            tweets = service.get_user_tweets("twitter", limit=limit)
            assert len(tweets) == limit
    
    def test_get_user_tweets_empty_username(self, service):
        """Test that empty username raises ValueError"""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            service.get_user_tweets("", limit=5)
    
    def test_get_user_tweets_normalizes_username(self, service):
        """Test that username is normalized (@ removed)"""
        tweets = service.get_user_tweets("@twitter", limit=5)
        assert len(tweets) == 5
    
    def test_get_user_tweets_known_user(self, service):
        """Test getting tweets for a known user"""
        tweets = service.get_user_tweets("twitter", limit=5)
        
        # All tweets should be from the same account
        assert all(tweet.account.href == "/Twitter" for tweet in tweets)
    
    def test_get_user_tweets_unknown_user(self, service):
        """Test getting tweets for an unknown user"""
        tweets = service.get_user_tweets("unknownuser123", limit=5)
        
        assert len(tweets) == 5
        # Should create account for unknown user
        assert all(tweet.account.href == "/unknownuser123" for tweet in tweets)
    
    def test_tweet_structure(self, service):
        """Test that tweets have the correct structure"""
        tweets = service.get_tweets_by_hashtag("python", limit=1)
        tweet = tweets[0]
        
        # Check all required fields are present
        assert hasattr(tweet, 'account')
        assert hasattr(tweet, 'date')
        assert hasattr(tweet, 'text')
        assert hasattr(tweet, 'replies')
        assert hasattr(tweet, 'retweets')
        assert hasattr(tweet, 'likes')
        assert hasattr(tweet, 'hashtags')
        
        # Check account structure
        assert hasattr(tweet.account, 'fullname')
        assert hasattr(tweet.account, 'href')
        assert hasattr(tweet.account, 'id')
        
        # Check types
        assert isinstance(tweet.account.fullname, str)
        assert isinstance(tweet.account.href, str)
        assert isinstance(tweet.account.id, int)
        assert isinstance(tweet.date, str)
        assert isinstance(tweet.text, str)
        assert isinstance(tweet.replies, int)
        assert isinstance(tweet.retweets, int)
        assert isinstance(tweet.likes, int)
        assert isinstance(tweet.hashtags, list)


