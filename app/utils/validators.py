"""
Input validation utilities
"""
from config import Config


def validate_limit(limit_str, default=None):
    """
    Validate and normalize the limit parameter
    
    Args:
        limit_str: Limit value as string from request args
        default: Default value if limit_str is None
        
    Returns:
        Validated integer limit value
        
    Raises:
        ValueError: If limit is invalid
    """
    if default is None:
        default = Config.DEFAULT_TWEET_LIMIT
    
    if limit_str is None:
        return default
    
    try:
        limit = int(limit_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid limit value: {limit_str}. Must be an integer.")
    
    min_limit = Config.MIN_TWEET_LIMIT
    max_limit = Config.MAX_TWEET_LIMIT
    
    if limit < min_limit:
        raise ValueError(f"Limit must be at least {min_limit}")
    
    if limit > max_limit:
        raise ValueError(f"Limit cannot exceed {max_limit}")
    
    return limit
