"""
Engagement scoring tool for TrendOps.
Calculates engagement metrics and detects anomalies.
"""
from typing import List, Dict
import numpy as np

class ScoringTool:
    """MCP tool for engagement scoring and anomaly detection."""
    
    def calculate_engagement_score(self, video: Dict) -> float:
        """
        Calculate engagement score for a video.
        
        Formula: (likes / views) * 1000 + (comments / views) * 500
        
        Args:
            video: Video data dict with viewCount, likeCount, commentCount
        
        Returns:
            Engagement score (0-100 normalized)
        """
        views = video.get("viewCount", 1)
        likes = video.get("likeCount", 0)
        comments = video.get("commentCount", 0)
        
        if views == 0:
            return 0.0
        
        # Weighted engagement score
        like_ratio = (likes / views) * 1000
        comment_ratio = (comments / views) * 500
        
        raw_score = like_ratio + comment_ratio
        
        # Normalize to 0-100 scale (cap at reasonable maximum)
        normalized = min(100, raw_score * 10)
        
        return round(normalized, 2)
    
    def rank_by_engagement(self, videos: List[Dict]) -> List[Dict]:
        """
        Rank videos by engagement score.
        
        Args:
            videos: List of video dicts
        
        Returns:
            Sorted list with engagement scores added
        """
        scored_videos = []
        
        for video in videos:
            score = self.calculate_engagement_score(video)
            video_with_score = video.copy()
            video_with_score["engagement_score"] = score
            scored_videos.append(video_with_score)
        
        # Sort by engagement score descending
        scored_videos.sort(key=lambda x: x["engagement_score"], reverse=True)
        
        return scored_videos
    
    def detect_anomalies(self, videos: List[Dict], threshold: float = 2.0) -> List[Dict]:
        """
        Detect engagement anomalies using statistical methods.
        
        Args:
            videos: List of video dicts with engagement scores
            threshold: Standard deviations from mean to flag as anomaly
        
        Returns:
            List of anomalous videos
        """
        if len(videos) < 3:
            return []
        
        scores = [v.get("engagement_score", 0) for v in videos]
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        
        if std_score == 0:
            return []
        
        anomalies = []
        
        for video in videos:
            score = video.get("engagement_score", 0)
            z_score = abs((score - mean_score) / std_score)
            
            if z_score > threshold:
                anomalies.append({
                    "title": video.get("title"),
                    "engagement_score": score,
                    "z_score": round(z_score, 2),
                    "type": "high" if score > mean_score else "low"
                })
        
        return anomalies
    
    def calculate_theme_engagement(
        self,
        videos: List[Dict],
        themes: List[Dict]
    ) -> List[Dict]:
        """
        Calculate average engagement per theme.
        
        Args:
            videos: List of videos with engagement scores
            themes: List of theme clusters
        
        Returns:
            Themes with engagement metrics
        """
        # Simple approach: match keywords in titles
        theme_scores = []
        
        for theme in themes:
            matching_videos = []
            keywords = theme.get("keywords", [])
            
            for video in videos:
                title_lower = video.get("title", "").lower()
                if any(keyword.lower() in title_lower for keyword in keywords):
                    matching_videos.append(video)
            
            if matching_videos:
                avg_engagement = np.mean([
                    v.get("engagement_score", 0) for v in matching_videos
                ])
                
                theme_scores.append({
                    "theme": theme.get("representative_term"),
                    "keywords": keywords,
                    "video_count": len(matching_videos),
                    "avg_engagement": round(avg_engagement, 2)
                })
        
        # Sort by engagement
        theme_scores.sort(key=lambda x: x["avg_engagement"], reverse=True)
        
        return theme_scores

scoring_tool = ScoringTool()
