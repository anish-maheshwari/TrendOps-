"""
Data Agent for TrendOps.
Responsible for fetching YouTube trending data.
"""
from typing import Dict, Optional
from app.tools.youtube_tool import youtube_tool
from app.utils.logging import get_logger

logger = get_logger(__name__)

class DataAgent:
    """
    MCP Agent: Data Acquisition
    
    Responsibilities:
    - Fetch YouTube trending videos
    - Validate input parameters
    - Return structured data only
    - No analysis logic
    """
    
    def __init__(self):
        self.name = "DataAgent"
        self.youtube = youtube_tool
    
    async def fetch_trending_data(
        self,
        region_code: str = "US",
        category_id: Optional[str] = None,
        max_results: int = 25
    ) -> Dict:
        """
        Fetch trending video data from YouTube.
        
        Args:
            region_code: Country code (US, IN, GB, etc.)
            category_id: YouTube category ID (optional)
            max_results: Number of videos to fetch
        
        Returns:
            Structured video data
        """
        logger.info(
            f"{self.name}: Fetching trending data",
            region=region_code,
            category=category_id
        )
        
        try:
            data = await self.youtube.fetch_trending_videos(
                region_code=region_code,
                category_id=category_id,
                max_results=max_results
            )
            
            logger.info(
                f"{self.name}: Successfully fetched data",
                video_count=len(data.get("videos", []))
            )
            
            return data
        
        except Exception as e:
            logger.error(
                f"{self.name}: Failed to fetch data",
                error=str(e)
            )
            raise

data_agent = DataAgent()
