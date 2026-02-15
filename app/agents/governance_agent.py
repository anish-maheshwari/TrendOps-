"""
Governance Agent for TrendOps.
Responsible for validation, logging, and cost tracking.
"""
from typing import Dict, Optional
from datetime import datetime
from app.utils.config import config
from app.utils.logging import get_logger
from app.utils.cost_tracker import tracker, ExecutionRecord

logger = get_logger(__name__)

class GovernanceAgent:
    """
    MCP Agent: Governance & Compliance
    
    Responsibilities:
    - Validate all inputs
    - Enforce rate limits
    - Track execution metrics
    - Maintain audit logs
    - Generate execution traces
    """
    
    def __init__(self):
        self.name = "GovernanceAgent"
    
    def validate_request(
        self,
        region_code: str,
        category_id: Optional[str],
        max_results: int
    ) -> Dict:
        """
        Validate incoming request parameters.
        
        Args:
            region_code: Country code
            category_id: YouTube category ID
            max_results: Number of results
        
        Returns:
            Validation result with status and sanitized params
        """
        start_time = datetime.utcnow()
        
        logger.info(
            f"{self.name}: Validating request",
            region=region_code,
            category=category_id
        )
        
        errors = []
        
        # Validate region code
        if region_code not in config.VALID_REGIONS:
            errors.append(f"Invalid region code: {region_code}. Must be one of {list(config.VALID_REGIONS)}")
        
        # Validate category
        if category_id and category_id not in config.VALID_CATEGORIES:
            errors.append(f"Invalid category ID: {category_id}. Must be one of {list(config.VALID_CATEGORIES.keys())}")
        
        # Validate max results
        if max_results < 1 or max_results > config.MAX_RESULTS_PER_REQUEST:
            errors.append(f"max_results must be between 1 and {config.MAX_RESULTS_PER_REQUEST}")
        
        # Check rate limits
        if not tracker.check_limits(config.MAX_REQUESTS_PER_SESSION):
            errors.append(f"Session limit exceeded: {config.MAX_REQUESTS_PER_SESSION} requests")
        
        duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Record validation
        tracker.record_execution(ExecutionRecord(
            tool_name="governance_validation",
            timestamp=start_time.isoformat(),
            duration_ms=duration_ms,
            status="success" if not errors else "validation_failed",
            api_calls=0,
            error="; ".join(errors) if errors else None
        ))
        
        if errors:
            logger.error(
                f"{self.name}: Validation failed",
                errors=errors
            )
            return {
                "valid": False,
                "errors": errors
            }
        
        logger.info(f"{self.name}: Validation passed")
        
        return {
            "valid": True,
            "sanitized_params": {
                "region_code": region_code,
                "category_id": category_id,
                "max_results": min(max_results, config.MAX_RESULTS_PER_REQUEST)
            }
        }
    
    def get_execution_trace(self) -> Dict:
        """
        Get complete execution trace for observability.
        
        Returns:
            Execution trace with all logged operations
        """
        logger.info(f"{self.name}: Generating execution trace")
        
        return {
            "executionLog": tracker.get_execution_trace(),
            "sessionStats": tracker.get_session_stats(),
            "governance": {
                "max_requests_per_session": config.MAX_REQUESTS_PER_SESSION,
                "requests_remaining": config.MAX_REQUESTS_PER_SESSION - tracker.session_stats["total_api_calls"]
            }
        }
    
    def log_final_metrics(self, success: bool, error: Optional[str] = None):
        """
        Log final execution metrics.
        
        Args:
            success: Whether the overall operation succeeded
            error: Error message if failed
        """
        stats = tracker.get_session_stats()
        
        logger.info(
            f"{self.name}: Final execution metrics",
            success=success,
            total_executions=stats["total_executions"],
            total_api_calls=stats["total_api_calls"],
            total_tokens=stats["total_estimated_tokens"],
            error=error
        )

governance_agent = GovernanceAgent()
