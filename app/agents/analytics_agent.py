"""
Analytics Agent for TrendOps.
Responsible for data processing and theme extraction.
"""
from typing import Dict, List
from datetime import datetime
from app.tools.clustering_tool import clustering_tool
from app.tools.scoring_tool import scoring_tool
from app.utils.logging import get_logger
from app.utils.cost_tracker import tracker, ExecutionRecord

logger = get_logger(__name__)

class AnalyticsAgent:
    """
    MCP Agent: Analytics & Processing
    
    Responsibilities:
    - Extract keywords and themes
    - Calculate engagement scores
    - Rank content by engagement
    - Detect anomalies
    """
    
    def __init__(self):
        self.name = "AnalyticsAgent"
        self.clustering = clustering_tool
        self.scoring = scoring_tool
    
    def analyze_trending_data(self, data: Dict) -> Dict:
        """
        Perform comprehensive analytics on trending data.
        
        Args:
            data: Raw video data from DataAgent
        
        Returns:
            Structured analytics results
        """
        start_time = datetime.utcnow()
        
        logger.info(f"{self.name}: Starting analytics")
        
        try:
            videos = data.get("videos", [])
            
            if not videos:
                return {
                    "topThemes": [],
                    "engagementInsights": "No data available for analysis",
                    "anomalies": []
                }
            
            # Extract text corpus
            texts = [
                f"{v.get('title', '')} {v.get('description', '')}"
                for v in videos
            ]
            
            # 1. Extract keywords
            keywords = self.clustering.extract_keywords(texts, top_n=15)
            
            # 2. Cluster themes
            themes = self.clustering.cluster_themes(texts, n_clusters=5)
            
            # 3. Calculate engagement scores
            scored_videos = self.scoring.rank_by_engagement(videos)
            
            # 4. Calculate theme engagement
            theme_engagement = self.scoring.calculate_theme_engagement(
                scored_videos,
                themes
            )
            
            # 5. Detect anomalies
            anomalies = self.scoring.detect_anomalies(scored_videos)
            
            # 6. Generate insights summary
            avg_engagement = sum(v.get("engagement_score", 0) for v in scored_videos) / len(scored_videos)
            top_video = scored_videos[0] if scored_videos else {}
            
            insights = self._generate_insights(
                avg_engagement=avg_engagement,
                top_video=top_video,
                theme_engagement=theme_engagement,
                anomaly_count=len(anomalies)
            )
            
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Record execution
            tracker.record_execution(ExecutionRecord(
                tool_name="analytics_processing",
                timestamp=start_time.isoformat(),
                duration_ms=duration_ms,
                status="success",
                api_calls=0,
                estimated_tokens=0
            ))
            
            logger.info(
                f"{self.name}: Analytics complete",
                duration_ms=duration_ms,
                themes_found=len(themes)
            )
            
            return {
                "topThemes": theme_engagement,
                "topKeywords": keywords[:10],
                "engagementInsights": insights,
                "anomalies": anomalies,
                "metrics": {
                    "avg_engagement": round(avg_engagement, 2),
                    "total_videos": len(videos),
                    "themes_identified": len(themes)
                }
            }
        
        except Exception as e:
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            tracker.record_execution(ExecutionRecord(
                tool_name="analytics_processing",
                timestamp=start_time.isoformat(),
                duration_ms=duration_ms,
                status="error",
                error=str(e)
            ))
            
            logger.error(f"{self.name}: Analytics failed", error=str(e))
            raise
    
    def _generate_insights(
        self,
        avg_engagement: float,
        top_video: Dict,
        theme_engagement: List[Dict],
        anomaly_count: int
    ) -> str:
        """Generate human-readable insights summary."""
        
        insights = []
        
        insights.append(f"Average engagement score: {avg_engagement:.2f}/100")
        
        if top_video:
            insights.append(
                f"Highest engagement: '{top_video.get('title', 'N/A')}' "
                f"({top_video.get('engagement_score', 0):.2f})"
            )
        
        if theme_engagement:
            top_theme = theme_engagement[0]
            insights.append(
                f"Leading theme: '{top_theme.get('theme')}' "
                f"with {top_theme.get('video_count')} videos"
            )
        
        if anomaly_count > 0:
            insights.append(f"Detected {anomaly_count} engagement anomalies")
        
        return " | ".join(insights)

analytics_agent = AnalyticsAgent()
