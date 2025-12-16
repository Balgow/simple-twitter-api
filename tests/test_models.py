"""
Tests for data models
"""
import pytest
from app.models.tweet import Tweet, Account


class TestAccount:
    """Test cases for Account model"""
    
    def test_account_creation(self):
        """Test creating an Account instance"""
        account = Account(
            fullname="Test User",
            href="/testuser",
            id=12345
        )
        
        assert account.fullname == "Test User"
        assert account.href == "/testuser"
        assert account.id == 12345
    
    def test_account_to_dict(self):
        """Test converting Account to dictionary"""
        account = Account(
            fullname="Test User",
            href="/testuser",
            id=12345
        )
        
        account_dict = account.to_dict()
        
        assert isinstance(account_dict, dict)
        assert account_dict['fullname'] == "Test User"
        assert account_dict['href'] == "/testuser"
        assert account_dict['id'] == 12345


class TestTweet:
    """Test cases for Tweet model"""
    
    def test_tweet_creation(self):
        """Test creating a Tweet instance"""
        account = Account(
            fullname="Test User",
            href="/testuser",
            id=12345
        )
        
        tweet = Tweet(
            account=account,
            date="2:54 PM - 8 Mar 2018",
            text="Test tweet #python",
            replies=10,
            retweets=20,
            likes=100,
            hashtags=["#python"]
        )
        
        assert tweet.account == account
        assert tweet.date == "2:54 PM - 8 Mar 2018"
        assert tweet.text == "Test tweet #python"
        assert tweet.replies == 10
        assert tweet.retweets == 20
        assert tweet.likes == 100
        assert tweet.hashtags == ["#python"]
    
    def test_tweet_to_dict(self):
        """Test converting Tweet to dictionary"""
        account = Account(
            fullname="Test User",
            href="/testuser",
            id=12345
        )
        
        tweet = Tweet(
            account=account,
            date="2:54 PM - 8 Mar 2018",
            text="Test tweet #python",
            replies=10,
            retweets=20,
            likes=100,
            hashtags=["#python"]
        )
        
        tweet_dict = tweet.to_dict()
        
        assert isinstance(tweet_dict, dict)
        assert isinstance(tweet_dict['account'], dict)
        assert tweet_dict['account']['fullname'] == "Test User"
        assert tweet_dict['date'] == "2:54 PM - 8 Mar 2018"
        assert tweet_dict['text'] == "Test tweet #python"
        assert tweet_dict['replies'] == 10
        assert tweet_dict['retweets'] == 20
        assert tweet_dict['likes'] == 100
        assert tweet_dict['hashtags'] == ["#python"]


