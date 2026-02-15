"""
Archestra MCP Server Entry Point

This module exposes TrendOps agents as standardized MCP Tools.
Archestra (or any MCP Client) can connect to this server via stdio/SSE to orchestrate the swarm.
"""
from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from app.agents.governance_agent import governance_agent
from app.agents.data_agent import data_agent
from app.agents.analytics_agent import analytics_agent
from app.agents.intelligence_agent import intelligence_agent

# Initialize standard MCP Server
mcp = FastMCP("TrendOps-Intelligence-Swarm")

@mcp.tool()
async def validate_request(region_code: str, category_id: Optional[str] = None, max_results: int = 25) -> str:
    """
    GOVERNANCE: Validate request parameters against security policies.
    Returns JSON string with validation status.
    """
    result = governance_agent.validate_request(region_code, category_id, max_results)
    return str(result)

@mcp.tool()
async def fetch_trending_data(region_code: str, category_id: Optional[str] = None, max_results: int = 25) -> str:
    """
    DATA: Fetch raw trending video data from YouTube API.
    Returns JSON string with video metadata.
    """
    result = await data_agent.fetch_trending_data(region_code, category_id, max_results)
    return str(result)

@mcp.tool()
def analyze_trends(data_json: str) -> str:
    """
    ANALYTICS: Perform clustering and engagement scoring on raw data.
    Takes JSON string of video data. Returns analysis results.
    """
    import json
    data = json.loads(data_json)
    result = analytics_agent.analyze_trending_data(data)
    return str(result)

@mcp.tool()
async def generate_intelligence(analytics_json: str, raw_data_json: str) -> str:
    """
    INTELLIGENCE: Generate executive strategy report using LLM.
    Takes JSON strings of analytics and raw data. Returns intelligence report.
    """
    import json
    analytics = json.loads(analytics_json)
    raw = json.loads(raw_data_json)
    result = await intelligence_agent.generate_intelligence_report(analytics, raw)
    return str(result)

if __name__ == "__main__":
    # Start the MCP server for Archestra orchestration
    mcp.run()
