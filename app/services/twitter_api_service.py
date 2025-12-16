"""
Real X (Twitter) API v2 implementation
Requires X API credentials - sign up at https://developer.x.com
"""
import os
import requests
from typing import List, Optional
from datetime import datetime
from app.models.tweet import Tweet, Account
from app.services.twitter_service import TwitterService


class TwitterAPIService(TwitterService):
    """
    Production implementation using X API v2
    
    Authentication:
    - Requires Bearer Token (App-only authentication)
    - Set TWITTER_BEARER_TOKEN environment variable
    
    API Access Levels:
    - Free: 100 reads/month (testing only)
    - Basic: $200/month - 10,000 reads/month
    - Pro: $5,000/month - 1,000,000 reads/month
    
    Documentation: https://developer.x.com/en/docs/x-api
    """
    
    BASE_URL = "https://api.twitter.com/2"
    
    def __init__(self, bearer_token: Optional[str] = None):
        """
        Initialize the Twitter API service
        
        Args:
            bearer_token: X API Bearer Token. If not provided, reads from 
                         TWITTER_BEARER_TOKEN environment variable
        
        Raises:
            ValueError: If no bearer token is provided or found in environment
        """
        self.bearer_token = bearer_token or os.getenv('TWITTER_BEARER_TOKEN')
        
        if not self.bearer_token:
            raise ValueError(
                "Twitter API Bearer Token is required. "
                "Set TWITTER_BEARER_TOKEN environment variable or pass bearer_token parameter. "
                "Get your token at https://developer.x.com"
            )
        
        self.headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
    
    def get_tweets_by_hashtag(self, hashtag: str, limit: int = 30) -> List[Tweet]:
        """
        Retrieve tweets containing a specific hashtag using X API v2 search
        
        API Endpoint: GET /2/tweets/search/recent
        Docs: https://developer.x.com/en/docs/twitter-api/tweets/search/api-reference
        
        Args:
            hashtag: The hashtag to search for (without # symbol)
            limit: Maximum number of tweets to return (max 100 per request)
            
        Returns:
            List of Tweet objects
            
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If API request fails
        """
        if not hashtag:
            raise ValueError("Hashtag cannot be empty")
        
        # Normalize hashtag
        hashtag = hashtag.lstrip('#')
        
        # Build query - search for hashtag
        query = f"#{hashtag}"
        
        # API parameters
        params = {
            'query': query,
            'max_results': min(limit, 100),  # API max is 100 per request
            'tweet.fields': 'created_at,public_metrics,text',
            'expansions': 'author_id',
            'user.fields': 'id,name,username'
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/tweets/search/recent",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                raise RuntimeError(
                    "Rate limit exceeded. Please wait before making more requests. "
                    "Consider upgrading your X API access tier."
                )
            
            # Handle authentication errors
            if response.status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Please check your Bearer Token. "
                    "Get your token at https://developer.x.com"
                )
            
            # Handle forbidden (insufficient access level)
            if response.status_code == 403:
                raise RuntimeError(
                    "Access forbidden. This endpoint may require a higher API access tier. "
                    "Free tier has limited access. Consider upgrading at https://developer.x.com"
                )
            
            response.raise_for_status()
            data = response.json()
            
            return self._parse_tweets_response(data)
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
    
    def get_user_tweets(self, username: str, limit: int = 30) -> List[Tweet]:
        """
        Retrieve tweets from a specific user's timeline using X API v2
        
        API Endpoint: GET /2/users/by/username/:username (get user ID)
                     GET /2/users/:id/tweets (get user tweets)
        Docs: https://developer.x.com/en/docs/twitter-api/users/lookup
              https://developer.x.com/en/docs/twitter-api/tweets/timelines
        
        Args:
            username: Twitter username (without @ symbol)
            limit: Maximum number of tweets to return
            
        Returns:
            List of Tweet objects
            
        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If API request fails
        """
        if not username:
            raise ValueError("Username cannot be empty")
        
        # Normalize username
        username = username.lstrip('@')
        
        try:
            # Step 1: Get user ID from username
            user_response = requests.get(
                f"{self.BASE_URL}/users/by/username/{username}",
                headers=self.headers,
                params={'user.fields': 'id,name,username'},
                timeout=10
            )
            
            self._handle_api_errors(user_response)
            user_response.raise_for_status()
            user_data = user_response.json()
            
            if 'data' not in user_data:
                raise RuntimeError(f"User '{username}' not found")
            
            user_id = user_data['data']['id']
            
            # Step 2: Get user's tweets
            tweets_params = {
                'max_results': min(limit, 100),
                'tweet.fields': 'created_at,public_metrics,text',
                'user.fields': 'id,name,username'
            }
            
            tweets_response = requests.get(
                f"{self.BASE_URL}/users/{user_id}/tweets",
                headers=self.headers,
                params=tweets_params,
                timeout=10
            )
            
            self._handle_api_errors(tweets_response)
            tweets_response.raise_for_status()
            tweets_data = tweets_response.json()
            
            # Add user info to response for parsing
            if 'data' in tweets_data:
                tweets_data['includes'] = {'users': [user_data['data']]}
            
            return self._parse_tweets_response(tweets_data)
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
    
    def _handle_api_errors(self, response):
        """Handle common API errors"""
        if response.status_code == 429:
            raise RuntimeError(
                "Rate limit exceeded. Please wait before making more requests."
            )
        if response.status_code == 401:
            raise RuntimeError(
                "Authentication failed. Please check your Bearer Token."
            )
        if response.status_code == 403:
            raise RuntimeError(
                "Access forbidden. This may require a higher API access tier."
            )
    
    def _parse_tweets_response(self, data: dict) -> List[Tweet]:
        """
        Parse X API v2 response into Tweet objects
        
        Args:
            data: API response JSON
            
        Returns:
            List of Tweet objects
        """
        tweets = []
        
        if 'data' not in data:
            return tweets
        
        # Build user lookup dict
        users = {}
        if 'includes' in data and 'users' in data['includes']:
            for user in data['includes']['users']:
                users[user['id']] = user
        
        for tweet_data in data['data']:
            # Get author info
            author_id = tweet_data.get('author_id')
            author_info = users.get(author_id, {})
            
            account = Account(
                fullname=author_info.get('name', 'Unknown'),
                href=f"/{author_info.get('username', 'unknown')}",
                id=int(author_id) if author_id else 0
            )
            
            # Parse metrics
            metrics = tweet_data.get('public_metrics', {})
            
            # Extract hashtags from text
            text = tweet_data.get('text', '')
            hashtags = [word for word in text.split() if word.startswith('#')]
            
            # Format date
            created_at = tweet_data.get('created_at', '')
            formatted_date = self._format_date(created_at)
            
            tweet = Tweet(
                account=account,
                date=formatted_date,
                text=text,
                replies=metrics.get('reply_count', 0),
                retweets=metrics.get('retweet_count', 0),
                likes=metrics.get('like_count', 0),
                hashtags=hashtags
            )
            
            tweets.append(tweet)
        
        return tweets
    
    def _format_date(self, iso_date: str) -> str:
        """
        Convert ISO 8601 date to readable format
        
        Args:
            iso_date: ISO 8601 date string (e.g., "2023-03-15T14:30:00.000Z")
            
        Returns:
            Formatted date string (e.g., "2:30 PM - 15 Mar 2023")
        """
        try:
            dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
            return dt.strftime("%-I:%M %p - %-d %b %Y")
        except (ValueError, AttributeError):
            return iso_date

