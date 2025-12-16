"""
Abstract Twitter service interface
"""
from abc import ABC, abstractmethod
from typing import List
from app.models.tweet import Tweet


class TwitterService(ABC):
    """
    Abstract base class for Twitter data retrieval services.
    This allows for easy swapping between different implementations
    (mocking, scraping, API calls, etc.)
    """
    
    @abstractmethod
    def get_tweets_by_hashtag(self, hashtag: str, limit: int = 30) -> List[Tweet]:
        """
        Retrieve tweets containing a specific hashtag
        
        Args:
            hashtag: The hashtag to search for (without # symbol)
            limit: Maximum number of tweets to return
            
        Returns:
            List of Tweet objects
            
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If service encounters an error
        """
        pass
    
    @abstractmethod
    def get_user_tweets(self, username: str, limit: int = 30) -> List[Tweet]:
        """
        Retrieve tweets from a specific user's timeline
        
        Args:
            username: Twitter username (without @ symbol)
            limit: Maximum number of tweets to return
            
        Returns:
            List of Tweet objects
            
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If service encounters an error
        """
        pass


