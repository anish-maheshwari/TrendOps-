"""
YouTube Data API tool for TrendOps.
Fetches trending video data with proper error handling.
"""
import httpx
from typing import Dict, Optional
from datetime import datetime
from app.utils.config import config
from app.utils.logging import get_logger
from app.utils.cost_tracker import tracker, ExecutionRecord

logger = get_logger(__name__)

class YouTubeTool:
    """MCP tool for fetching YouTube trending data."""
    
    def __init__(self):
        self.base_url = config.YOUTUBE_API_BASE_URL
        self.api_key = config.YOUTUBE_API_KEY
    
    async def fetch_trending_videos(
        self,
        region_code: str = "US",
        category_id: Optional[str] = None,
        max_results: int = 25
    ) -> Dict:
        """
        Fetch trending videos from YouTube Data API.
        
        Args:
            region_code: ISO 3166-1 alpha-2 country code
            category_id: YouTube category ID (optional)
            max_results: Maximum number of results (1-50)
        
        Returns:
            Structured JSON with video data
        """
        start_time = datetime.utcnow()
        
        try:
            # Validate inputs
            if region_code not in config.VALID_REGIONS:
                raise ValueError(f"Invalid region code: {region_code}")
            
            if category_id and category_id not in config.VALID_CATEGORIES:
                raise ValueError(f"Invalid category ID: {category_id}")
            
            if max_results > config.MAX_RESULTS_PER_REQUEST:
                max_results = config.MAX_RESULTS_PER_REQUEST
            
            # Build request
            params = {
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "regionCode": region_code,
                "maxResults": max_results,
                "key": self.api_key
            }
            
            if category_id:
                params["videoCategoryId"] = category_id
            
            logger.info(
                "Fetching YouTube trending videos",
                region=region_code,
                category=category_id,
                max_results=max_results
            )
            
            # Make API call
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/videos",
                    params=params,
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
            
            # Transform to structured format
            videos = []
            for item in data.get("items", []):
                snippet = item.get("snippet", {})
                stats = item.get("statistics", {})
                
                videos.append({
                    "videoId": item.get("id"),
                    "title": snippet.get("title"),
                    "description": snippet.get("description", ""),
                    "tags": snippet.get("tags", []),
                    "viewCount": int(stats.get("viewCount", 0)),
                    "likeCount": int(stats.get("likeCount", 0)),
                    "commentCount": int(stats.get("commentCount", 0)),
                    "publishedAt": snippet.get("publishedAt"),
                    "channelTitle": snippet.get("channelTitle")
                })
            
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Record execution
            tracker.record_execution(ExecutionRecord(
                tool_name="youtube_fetch_trending",
                timestamp=start_time.isoformat(),
                duration_ms=duration_ms,
                status="success",
                api_calls=1,
                estimated_tokens=0
            ))
            
            logger.info(
                "Successfully fetched trending videos",
                video_count=len(videos),
                duration_ms=duration_ms
            )
            
            return {
                "videos": videos,
                "metadata": {
                    "region": region_code,
                    "category": category_id,
                    "fetched_at": datetime.utcnow().isoformat(),
                    "count": len(videos)
                }
            }
        
        except httpx.HTTPStatusError as e:
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            error_msg = f"YouTube API error: {e.response.status_code}"
            
            tracker.record_execution(ExecutionRecord(
                tool_name="youtube_fetch_trending",
                timestamp=start_time.isoformat(),
                duration_ms=duration_ms,
                status="error",
                api_calls=1,
                error=error_msg
            ))
            
            logger.error(error_msg, status_code=e.response.status_code)
            raise
        
        except Exception as e:
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            error_msg = f"Unexpected error: {str(e)}"
            
            tracker.record_execution(ExecutionRecord(
                tool_name="youtube_fetch_trending",
                timestamp=start_time.isoformat(),
                duration_ms=duration_ms,
                status="error",
                error=error_msg
            ))
            
            logger.error(error_msg, exception=str(e))
            raise

youtube_tool = YouTubeTool()
