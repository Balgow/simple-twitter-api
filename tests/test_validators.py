"""
Tests for validation utilities
"""
import pytest
from app.utils.validators import validate_limit


class TestValidateLimit:
    """Test cases for validate_limit function"""
    
    def test_valid_limit(self):
        """Test validation with valid limit value"""
        result = validate_limit("50")
        assert result == 50
    
    def test_default_limit(self):
        """Test validation returns default when limit is None"""
        result = validate_limit(None)
        assert result == 30  # DEFAULT_TWEET_LIMIT
    
    def test_limit_below_minimum(self):
        """Test validation rejects limit below minimum"""
        with pytest.raises(ValueError, match="Limit must be at least"):
            validate_limit("0")
    
    def test_limit_above_maximum(self):
        """Test validation rejects limit above maximum"""
        with pytest.raises(ValueError, match="Limit cannot exceed"):
            validate_limit("200")
    
    def test_invalid_limit_format(self):
        """Test validation rejects non-integer limit"""
        with pytest.raises(ValueError, match="Invalid limit value"):
            validate_limit("abc")
    
    def test_limit_boundary_minimum(self):
        """Test validation accepts minimum limit"""
        result = validate_limit("1")
        assert result == 1
    
    def test_limit_boundary_maximum(self):
        """Test validation accepts maximum limit"""
        result = validate_limit("100")
        assert result == 100
