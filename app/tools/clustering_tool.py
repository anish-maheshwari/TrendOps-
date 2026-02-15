"""
Clustering and theme extraction tool for TrendOps.
Uses NLP techniques to identify trending themes.
"""
from typing import List, Dict
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

class ClusteringTool:
    """MCP tool for theme clustering and keyword extraction."""
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
    
    def extract_keywords(self, texts: List[str], top_n: int = 20) -> List[Dict]:
        """
        Extract top keywords from text corpus.
        
        Args:
            texts: List of text strings (titles + descriptions)
            top_n: Number of top keywords to return
        
        Returns:
            List of {keyword, frequency} dicts
        """
        # Tokenize and clean
        all_words = []
        for text in texts:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            all_words.extend([w for w in words if w not in self.stop_words])
        
        # Count frequencies
        word_counts = Counter(all_words)
        top_keywords = word_counts.most_common(top_n)
        
        return [
            {"keyword": word, "frequency": count}
            for word, count in top_keywords
        ]
    
    def cluster_themes(self, texts: List[str], n_clusters: int = 5) -> List[Dict]:
        """
        Cluster texts into themes using K-means.
        
        Args:
            texts: List of text strings
            n_clusters: Number of clusters to create
        
        Returns:
            List of theme clusters with representative keywords
        """
        if len(texts) < n_clusters:
            n_clusters = max(2, len(texts) // 2)
        
        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(tfidf_matrix)
            
            # Extract top terms per cluster
            feature_names = vectorizer.get_feature_names_out()
            themes = []
            
            for cluster_id in range(n_clusters):
                # Get top terms for this cluster
                center = kmeans.cluster_centers_[cluster_id]
                top_indices = center.argsort()[-5:][::-1]
                top_terms = [feature_names[i] for i in top_indices]
                
                # Count videos in cluster
                cluster_size = np.sum(kmeans.labels_ == cluster_id)
                
                themes.append({
                    "theme_id": cluster_id,
                    "keywords": top_terms,
                    "video_count": int(cluster_size),
                    "representative_term": top_terms[0]
                })
            
            # Sort by cluster size
            themes.sort(key=lambda x: x["video_count"], reverse=True)
            
            return themes
        
        except Exception as e:
            # Fallback to simple keyword extraction
            keywords = self.extract_keywords(texts, top_n=10)
            return [{
                "theme_id": 0,
                "keywords": [k["keyword"] for k in keywords[:5]],
                "video_count": len(texts),
                "representative_term": keywords[0]["keyword"] if keywords else "general"
            }]

clustering_tool = ClusteringTool()
