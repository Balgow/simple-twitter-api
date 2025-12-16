"""
User-related API endpoints
"""
from fastapi import APIRouter, Query, HTTPException, Request
from typing import List
from app.services import get_twitter_service
from app.models.tweet import Tweet

router = APIRouter()


@router.get('/users/{username}', response_model=List[dict])
async def get_user_tweets(
    request: Request,
    username: str,
    limit: int = Query(default=30, ge=1, le=100)
):
    """
    Get tweets from a specific user's timeline
    
    Args:
        username: The Twitter username (from URL path)
        limit: Number of tweets to retrieve (default: 30, min: 1, max: 100)
        
    Returns:
        JSON array of tweet objects
        
    Example:
        GET /users/twitter?limit=20
    """
    try:
        # Get Twitter service instance
        twitter_service = get_twitter_service()
        
        # Fetch tweets
        tweets = twitter_service.get_user_tweets(username, limit)
        
        # Convert to dict for JSON serialization
        tweets_data = [tweet.to_dict() for tweet in tweets]
        
        return tweets_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f'Service error: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
