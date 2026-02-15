"""
TrendOps - AI Trend Intelligence Control Plane
Main FastAPI application with multi-agent orchestration.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

from app.agents.data_agent import data_agent
from app.agents.analytics_agent import analytics_agent
from app.agents.intelligence_agent import intelligence_agent
from app.agents.governance_agent import governance_agent
from app.utils.config import config
from app.utils.logging import get_logger

# Validate configuration on startup
try:
    config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please set YOUTUBE_API_KEY and ANTHROPIC_API_KEY environment variables")
    exit(1)

logger = get_logger(__name__)

app = FastAPI(
    title="TrendOps",
    description="AI Trend Intelligence Control Plane - Multi-Agent MCP System",
    version="1.0.0"
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

class TrendAnalysisRequest(BaseModel):
    """Request model for trend analysis."""
    region_code: str = Field(default="US", description="ISO 3166-1 alpha-2 country code")
    category_id: Optional[str] = Field(default=None, description="YouTube category ID")
    max_results: int = Field(default=25, ge=1, le=50, description="Number of videos to analyze")
    include_intelligence: bool = Field(default=True, description="Generate LLM-based intelligence report")

class TrendAnalysisResponse(BaseModel):
    """Response model for trend analysis."""
    status: str
    data: dict
    analytics: dict
    intelligence: Optional[dict] = None
    governance: dict

@app.get("/")
async def root(request: Request):
    """Render the SaaS landing page."""
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    """Render the enterprise dashboard UI."""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "agents": {
            "data_agent": "ready",
            "analytics_agent": "ready",
            "intelligence_agent": "ready",
            "governance_agent": "ready"
        },
        "configuration": {
            "youtube_api": "configured" if config.YOUTUBE_API_KEY else "missing",
            "google_api": "configured" if config.GOOGLE_API_KEY else "missing"
        }
    }

@app.post("/analyze", response_model=TrendAnalysisResponse)
async def analyze_trends(request: TrendAnalysisRequest):
    """
    Main orchestration endpoint for trend analysis.
    
    Orchestration Flow:
    1. GovernanceAgent validates input
    2. DataAgent fetches YouTube data
    3. AnalyticsAgent processes data
    4. IntelligenceAgent generates insights (optional)
    5. GovernanceAgent returns execution trace
    """
    logger.info(
        "Received trend analysis request",
        region=request.region_code,
        category=request.category_id
    )
    
    try:
        # STEP 1: Governance - Validate Request
        validation = governance_agent.validate_request(
            region_code=request.region_code,
            category_id=request.category_id,
            max_results=request.max_results
        )
        
        if not validation["valid"]:
            governance_agent.log_final_metrics(success=False, error="Validation failed")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Validation failed",
                    "details": validation["errors"]
                }
            )
        
        params = validation["sanitized_params"]
        
        # STEP 2: Data Agent - Fetch Trending Data
        raw_data = await data_agent.fetch_trending_data(
            region_code=params["region_code"],
            category_id=params["category_id"],
            max_results=params["max_results"]
        )
        
        # STEP 3: Analytics Agent - Process Data
        analytics_results = analytics_agent.analyze_trending_data(raw_data)
        
        # STEP 4: Intelligence Agent - Generate Insights (Optional)
        intelligence_results = None
        if request.include_intelligence:
            intelligence_results = await intelligence_agent.generate_intelligence_report(
                analytics_data=analytics_results,
                raw_data=raw_data
            )
        
        # STEP 5: Governance - Get Execution Trace
        execution_trace = governance_agent.get_execution_trace()
        governance_agent.log_final_metrics(success=True)
        
        logger.info("Trend analysis completed successfully")
        
        return TrendAnalysisResponse(
            status="success",
            data=raw_data,
            analytics=analytics_results,
            intelligence=intelligence_results,
            governance=execution_trace
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Trend analysis failed", error=str(e))
        governance_agent.log_final_metrics(success=False, error=str(e))
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": str(e)
            }
        )

@app.get("/governance/trace")
async def get_execution_trace():
    """Get current execution trace for observability."""
    return governance_agent.get_execution_trace()

@app.get("/config/regions")
async def get_valid_regions():
    """Get list of valid region codes."""
    return {
        "valid_regions": list(config.VALID_REGIONS)
    }

@app.get("/config/categories")
async def get_valid_categories():
    """Get list of valid YouTube categories."""
    return {
        "valid_categories": config.VALID_CATEGORIES
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
