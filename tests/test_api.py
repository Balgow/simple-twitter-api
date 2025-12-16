"""
Tests for API endpoints
"""
import pytest


class TestHashtagsEndpoint:
    """Test cases for /hashtags/<hashtag> endpoint"""
    
    def test_get_tweets_by_hashtag_success(self, client):
        """Test successful hashtag query"""
        response = client.get('/hashtags/python')
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 30  # Default limit
    
    def test_get_tweets_by_hashtag_with_limit(self, client):
        """Test hashtag query with custom limit"""
        response = client.get('/hashtags/python?limit=10')
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 10
    
    def test_get_tweets_by_hashtag_invalid_limit(self, client):
        """Test hashtag query with invalid limit"""
        response = client.get('/hashtags/python?limit=abc')
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_get_tweets_by_hashtag_limit_too_high(self, client):
        """Test hashtag query with limit exceeding maximum"""
        response = client.get('/hashtags/python?limit=200')
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_get_tweets_by_hashtag_limit_too_low(self, client):
        """Test hashtag query with limit below minimum"""
        response = client.get('/hashtags/python?limit=0')
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_get_tweets_by_hashtag_response_structure(self, client):
        """Test that response has correct structure"""
        response = client.get('/hashtags/python?limit=1')
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 1
        tweet = data[0]
        
        # Check required fields
        assert 'account' in tweet
        assert 'date' in tweet
        assert 'text' in tweet
        assert 'replies' in tweet
        assert 'retweets' in tweet
        assert 'likes' in tweet
        assert 'hashtags' in tweet
        
        # Check account structure
        account = tweet['account']
        assert 'fullname' in account
        assert 'href' in account
        assert 'id' in account
    
    def test_get_tweets_by_hashtag_content_type(self, client):
        """Test that response has correct content type"""
        response = client.get('/hashtags/python')
        
        assert 'application/json' in response.headers['content-type']


class TestUsersEndpoint:
    """Test cases for /users/<username> endpoint"""
    
    def test_get_user_tweets_success(self, client):
        """Test successful user query"""
        response = client.get('/users/twitter')
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 30  # Default limit
    
    def test_get_user_tweets_with_limit(self, client):
        """Test user query with custom limit"""
        response = client.get('/users/twitter?limit=20')
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 20
    
    def test_get_user_tweets_invalid_limit(self, client):
        """Test user query with invalid limit"""
        response = client.get('/users/twitter?limit=xyz')
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_get_user_tweets_limit_too_high(self, client):
        """Test user query with limit exceeding maximum"""
        response = client.get('/users/twitter?limit=150')
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_get_user_tweets_limit_too_low(self, client):
        """Test user query with limit below minimum"""
        response = client.get('/users/twitter?limit=-1')
        
        assert response.status_code == 422  # FastAPI validation error
    
    def test_get_user_tweets_response_structure(self, client):
        """Test that response has correct structure"""
        response = client.get('/users/twitter?limit=1')
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 1
        tweet = data[0]
        
        # Check required fields
        assert 'account' in tweet
        assert 'date' in tweet
        assert 'text' in tweet
        assert 'replies' in tweet
        assert 'retweets' in tweet
        assert 'likes' in tweet
        assert 'hashtags' in tweet
        
        # Check account structure
        account = tweet['account']
        assert 'fullname' in account
        assert 'href' in account
        assert 'id' in account
    
    def test_get_user_tweets_content_type(self, client):
        """Test that response has correct content type"""
        response = client.get('/users/twitter')
        
        assert 'application/json' in response.headers['content-type']


class TestHealthEndpoint:
    """Test cases for /health endpoint"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
