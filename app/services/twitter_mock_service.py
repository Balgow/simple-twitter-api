"""
Mock Twitter service implementation for demonstration
This can be easily replaced with a real scraping or API implementation
"""
import random
from datetime import datetime, timedelta
from typing import List
from app.models.tweet import Tweet, Account
from app.services.twitter_service import TwitterService


class TwitterMockService(TwitterService):
    """
    Mock implementation of Twitter service that generates realistic sample data.
    
    In production, this would be replaced with:
    - Real scraping implementation using requests + BeautifulSoup
    - Twitter API v2 implementation with proper authentication
    - Third-party Twitter data provider
    
    This mock demonstrates the service architecture while being functional
    for testing and development.
    """
    
    # Sample data for generating realistic tweets
    SAMPLE_ACCOUNTS = [
        {"fullname": "Raymond Hettinger", "href": "/raymondh", "id": 14159138},
        {"fullname": "Guido van Rossum", "href": "/gvanrossum", "id": 10945672},
        {"fullname": "Python Software", "href": "/ThePSF", "id": 63873759},
        {"fullname": "Real Python", "href": "/realpython", "id": 752486881},
        {"fullname": "Python Weekly", "href": "/PythonWeekly", "id": 315766685},
        {"fullname": "Twitter", "href": "/Twitter", "id": 783214},
        {"fullname": "Tech News", "href": "/technews", "id": 123456789},
        {"fullname": "Code Academy", "href": "/codeacademy", "id": 987654321},
    ]
    
    SAMPLE_TEXTS = [
        "Just released a new #Python library for data processing! Check it out: github.com/example",
        "Historically, bash filename pattern matching was known as \"globbing\". Hence, the #python module called \"glob\".",
        "Excited to announce our new feature! #technology #innovation",
        "Working on some amazing #Python projects today. The productivity is real!",
        "Powerful voices. Inspiring women. #InternationalWomensDay",
        "New blog post about #programming best practices. Link in bio!",
        "Just deployed our latest microservice using #Python 3.12. Performance improvements are incredible!",
        "Anyone else loving the new features in Python 3.13? #python #coding",
        "Great conference talk today about #softwaredevelopment and #agile methodologies",
        "Remember: premature optimization is the root of all evil. #programming #python",
    ]
    
    def __init__(self):
        """Initialize the mock service"""
        random.seed(42)  # For reproducible results
    
    def get_tweets_by_hashtag(self, hashtag: str, limit: int = 30) -> List[Tweet]:
        """
        Generate mock tweets containing the specified hashtag
        
        Args:
            hashtag: The hashtag to search for (without # symbol)
            limit: Maximum number of tweets to return
            
        Returns:
            List of Tweet objects containing the hashtag
        """
        if not hashtag:
            raise ValueError("Hashtag cannot be empty")
        
        # Normalize hashtag (remove # if present)
        hashtag = hashtag.lstrip('#').lower()
        
        tweets = []
        for i in range(limit):
            account_data = random.choice(self.SAMPLE_ACCOUNTS)
            account = Account(**account_data)
            
            # Generate tweet text that includes the requested hashtag
            base_text = random.choice(self.SAMPLE_TEXTS)
            
            # Extract existing hashtags from text
            existing_hashtags = [word[1:].lower() for word in base_text.split() if word.startswith('#')]
            
            # Ensure the requested hashtag is included
            if hashtag not in existing_hashtags:
                existing_hashtags.insert(0, hashtag)
                base_text = f"{base_text}\n#{hashtag}"
            
            # Generate random engagement metrics
            tweet = Tweet(
                account=account,
                date=self._generate_date(i),
                text=base_text,
                replies=random.randint(0, 500),
                retweets=random.randint(0, 1000),
                likes=random.randint(0, 5000),
                hashtags=[f"#{tag}" for tag in existing_hashtags]
            )
            tweets.append(tweet)
        
        return tweets
    
    def get_user_tweets(self, username: str, limit: int = 30) -> List[Tweet]:
        """
        Generate mock tweets from the specified user's timeline
        
        Args:
            username: Twitter username (without @ symbol)
            limit: Maximum number of tweets to return
            
        Returns:
            List of Tweet objects from the user
        """
        if not username:
            raise ValueError("Username cannot be empty")
        
        # Normalize username (remove @ if present)
        username = username.lstrip('@')
        
        # Find or create account for this user
        matching_account = next(
            (acc for acc in self.SAMPLE_ACCOUNTS if acc['href'].lstrip('/').lower() == username.lower()),
            None
        )
        
        if matching_account:
            account = Account(**matching_account)
        else:
            # Create a new account for unknown users
            account = Account(
                fullname=username.title(),
                href=f"/{username}",
                id=random.randint(1000000, 99999999)
            )
        
        tweets = []
        for i in range(limit):
            base_text = random.choice(self.SAMPLE_TEXTS)
            
            # Extract hashtags from text
            hashtags = [word for word in base_text.split() if word.startswith('#')]
            
            # Generate random engagement metrics
            tweet = Tweet(
                account=account,
                date=self._generate_date(i),
                text=base_text,
                replies=random.randint(0, 500),
                retweets=random.randint(0, 1000),
                likes=random.randint(0, 5000),
                hashtags=hashtags
            )
            tweets.append(tweet)
        
        return tweets
    
    def _generate_date(self, index: int) -> str:
        """
        Generate a realistic tweet date/time string
        
        Args:
            index: Tweet index (more recent tweets have lower indices)
            
        Returns:
            Formatted date string like "2:54 PM - 8 Mar 2018"
        """
        # Generate dates going backwards in time
        days_ago = index * 0.5  # Roughly 2 tweets per day
        tweet_time = datetime.now() - timedelta(days=days_ago)
        
        return tweet_time.strftime("%-I:%M %p - %-d %b %Y")


