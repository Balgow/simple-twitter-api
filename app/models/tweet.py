"""
Tweet data models
"""
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Account:
    """Twitter account information"""
    fullname: str
    href: str
    id: int
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class Tweet:
    """Tweet data model"""
    account: Account
    date: str
    text: str
    replies: int
    retweets: int
    likes: int
    hashtags: List[str]
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'account': self.account.to_dict(),
            'date': self.date,
            'text': self.text,
            'replies': self.replies,
            'retweets': self.retweets,
            'likes': self.likes,
            'hashtags': self.hashtags
        }


