"""
Clustering and theme extraction tool for TrendOps.
Uses NLP techniques to identify trending themes.
Architected for high-performance with zero heavy-weight dependencies like scikit-learn.
"""
from typing import List, Dict
from collections import Counter
import re
import math

class ClusteringTool:
    """
    Lightweight MCP tool for theme clustering and keyword extraction.
    Uses a custom TF-IDF + K-Means implementation to maintain Vercel compatibility (under 250MB).
    """
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'video', 'official', 'music', 'new', 'latest', 'shorts', 'youtube'
        }
    
    def extract_keywords(self, texts: List[str], top_n: int = 20) -> List[Dict]:
        """Extract top keywords from text corpus using frequency."""
        all_words = []
        for text in texts:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            all_words.extend([w for w in words if w not in self.stop_words])
        
        word_counts = Counter(all_words)
        return [{"keyword": word, "frequency": count} for word, count in word_counts.most_common(top_n)]

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return [w for w in words if w not in self.stop_words]

    def cluster_themes(self, texts: List[str], n_clusters: int = 5) -> List[Dict]:
        """
        Cluster texts into themes using a custom TF-IDF + K-Means implementation.
        Preserves the project's analytical power while staying lightweight.
        """
        if not texts:
            return []
        
        if len(texts) < n_clusters:
            n_clusters = max(1, len(texts))

        # 1. Simple TF-IDF Vectorization
        tokens_list = [self._tokenize(t) for t in texts]
        vocabulary = list(set([word for tokens in tokens_list for word in tokens]))
        if not vocabulary:
            return [{"theme_id": 0, "keywords": ["general"], "video_count": len(texts), "representative_term": "general"}]

        word_to_idx = {word: i for i, word in enumerate(vocabulary)}
        idf = {}
        n_docs = len(texts)
        for word in vocabulary:
            doc_count = sum(1 for tokens in tokens_list if word in tokens)
            idf[word] = math.log(n_docs / (1 + doc_count))

        vectors = []
        for tokens in tokens_list:
            vector = [0.0] * len(vocabulary)
            counts = Counter(tokens)
            for word, freq in counts.items():
                if word in word_to_idx:
                    tf = freq / len(tokens) if tokens else 0
                    vector[word_to_idx[word]] = tf * idf[word]
            vectors.append(vector)

        # 2. Basic K-Means Implementation (Pure Python)
        # Initialize centroids randomly (first n_clusters docs)
        centroids = vectors[:n_clusters]
        labels = [0] * n_docs
        
        for _ in range(5): # 5 iterations is enough for small YouTube sets
            # Assignment
            new_labels = []
            for v in vectors:
                distances = []
                for c in centroids:
                    # Euclidean distance
                    dist = sum((a - b) ** 2 for a, b in zip(v, c))
                    distances.append(dist)
                new_labels.append(distances.index(min(distances)))
            
            if new_labels == labels:
                break
            labels = new_labels

            # Update centroids
            for i in range(n_clusters):
                cluster_points = [vectors[j] for j, l in enumerate(labels) if l == i]
                if cluster_points:
                    new_centroid = [sum(dim) / len(cluster_points) for dim in zip(*cluster_points)]
                    centroids[i] = new_centroid

        # 3. Extract Themes
        themes = []
        for i in range(n_clusters):
            cluster_indices = [j for j, l in enumerate(labels) if l == i]
            if not cluster_indices: continue
            
            # Find top keywords for this cluster (most frequent words in titles)
            cluster_words = []
            for idx in cluster_indices:
                cluster_words.extend(tokens_list[idx])
            
            top_terms = [word for word, count in Counter(cluster_words).most_common(5)]
            if not top_terms: top_terms = ["general"]

            themes.append({
                "theme_id": i,
                "keywords": top_terms,
                "video_count": len(cluster_indices),
                "representative_term": top_terms[0]
            })

        themes.sort(key=lambda x: x["video_count"], reverse=True)
        return themes

clustering_tool = ClusteringTool()
