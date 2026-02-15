"""
Cost tracking and governance for TrendOps.
Monitors API usage, token consumption, and enforces limits.
"""
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class ExecutionRecord:
    """Record of a single tool execution."""
    tool_name: str
    timestamp: str
    duration_ms: float
    status: str
    api_calls: int = 0
    estimated_tokens: int = 0
    error: str = None

class CostTracker:
    """In-memory cost and execution tracker for governance."""
    
    def __init__(self):
        self.execution_log: List[ExecutionRecord] = []
        self.session_stats = {
            "total_api_calls": 0,
            "total_estimated_tokens": 0,
            "total_executions": 0,
            "session_start": datetime.utcnow().isoformat()
        }
    
    def record_execution(self, record: ExecutionRecord):
        """Record a tool execution."""
        self.execution_log.append(record)
        self.session_stats["total_executions"] += 1
        self.session_stats["total_api_calls"] += record.api_calls
        self.session_stats["total_estimated_tokens"] += record.estimated_tokens
    
    def get_execution_trace(self) -> List[Dict]:
        """Get full execution trace."""
        return [asdict(record) for record in self.execution_log]
    
    def get_session_stats(self) -> Dict:
        """Get aggregated session statistics."""
        return self.session_stats.copy()
    
    def check_limits(self, max_requests: int) -> bool:
        """Check if session limits are exceeded."""
        return self.session_stats["total_api_calls"] < max_requests

# Global tracker instance
tracker = CostTracker()
