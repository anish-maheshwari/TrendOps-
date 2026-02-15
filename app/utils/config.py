"""
Configuration management for TrendOps.
Loads environment variables and validates required settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Central configuration for TrendOps system."""
    
    # API Keys
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # YouTube API Configuration
    YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"
    
    # Governance Limits
    MAX_REQUESTS_PER_SESSION = 100
    MAX_RESULTS_PER_REQUEST = 50
    DEFAULT_MAX_RESULTS = 25
    
    # Valid YouTube Region Codes (subset for validation)
    VALID_REGIONS = {
        "US", "IN", "GB", "CA", "AU", "DE", "FR", "JP", "KR", "BR"
    }
    
    # Valid YouTube Category IDs
    VALID_CATEGORIES = {
        "1": "Film & Animation",
        "2": "Autos & Vehicles",
        "10": "Music",
        "15": "Pets & Animals",
        "17": "Sports",
        "19": "Travel & Events",
        "20": "Gaming",
        "22": "People & Blogs",
        "23": "Comedy",
        "24": "Entertainment",
        "25": "News & Politics",
        "26": "Howto & Style",
        "27": "Education",
        "28": "Science & Technology",
        "29": "Nonprofits & Activism"
    }
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.YOUTUBE_API_KEY:
            raise ValueError("YOUTUBE_API_KEY environment variable is required")
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")

config = Config()
