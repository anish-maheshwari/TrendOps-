"""
Intelligence Agent for TrendOps.
Responsible for generating executive insights using LLM.
"""
from typing import Dict
from datetime import datetime
import warnings

# Use a more robust suppression for the deprecated library notice
warnings.filterwarnings("ignore", message=".*google.generativeai.*")
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
from app.utils.config import config
from app.utils.logging import get_logger
from app.utils.cost_tracker import tracker, ExecutionRecord

logger = get_logger(__name__)

class IntelligenceAgent:
    """
    MCP Agent: Intelligence & Insights
    
    Responsibilities:
    - Generate executive summaries
    - Identify emerging patterns
    - Suggest strategic opportunities
    - Produce investor-ready insights
    """
    
    def __init__(self):
        self.name = "IntelligenceAgent"
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    async def generate_intelligence_report(
        self,
        analytics_data: Dict,
        raw_data: Dict
    ) -> Dict:
        """
        Generate executive intelligence report using LLM.
        
        Args:
            analytics_data: Processed analytics from AnalyticsAgent
            raw_data: Original data context
        
        Returns:
            Structured intelligence report
        """
        start_time = datetime.utcnow()
        
        logger.info(f"{self.name}: Generating intelligence report")
        
        try:
            # Build context for LLM
            context = self._build_context(analytics_data, raw_data)
            
            # Generate report using Gemini
            response = self.model.generate_content(
                self._build_prompt(context),
                generation_config={
                    'temperature': 0.7,
                    'max_output_tokens': 2000,
                }
            )
            
            report_text = response.text
            
            # Estimate token usage (Gemini doesn't provide exact counts in free tier)
            estimated_tokens = len(context.split()) + len(report_text.split())
            
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Record execution
            tracker.record_execution(ExecutionRecord(
                tool_name="intelligence_generation",
                timestamp=start_time.isoformat(),
                duration_ms=duration_ms,
                status="success",
                api_calls=1,
                estimated_tokens=estimated_tokens
            ))
            
            logger.info(
                f"{self.name}: Report generated",
                duration_ms=duration_ms,
                tokens_used=estimated_tokens
            )
            
            return {
                "executiveSummary": self._extract_section(report_text, "EXECUTIVE SUMMARY"),
                "emergingPatterns": self._extract_section(report_text, "EMERGING PATTERNS"),
                "strategicImplications": self._extract_section(report_text, "STRATEGIC IMPLICATIONS"),
                "startupOpportunities": self._extract_list_section(report_text, "STARTUP OPPORTUNITIES"),
                "contentIdeas": self._extract_list_section(report_text, "CONTENT IDEAS"),
                "fullReport": report_text,
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "tokens_used": estimated_tokens,
                    "model": "gemini-flash-latest"
                }
            }
        
        except Exception as e:
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            tracker.record_execution(ExecutionRecord(
                tool_name="intelligence_generation",
                timestamp=start_time.isoformat(),
                duration_ms=duration_ms,
                status="error",
                error=str(e)
            ))
            
            logger.error(f"{self.name}: Report generation failed", error=str(e))
            raise
    
    def _build_context(self, analytics_data: Dict, raw_data: Dict) -> str:
        """Build context string for LLM."""
        
        region = raw_data.get("metadata", {}).get("region", "Unknown")
        video_count = analytics_data.get("metrics", {}).get("total_videos", 0)
        avg_engagement = analytics_data.get("metrics", {}).get("avg_engagement", 0)
        
        themes = analytics_data.get("topThemes", [])
        keywords = analytics_data.get("topKeywords", [])
        anomalies = analytics_data.get("anomalies", [])
        
        context = f"""
REGION: {region}
VIDEOS ANALYZED: {video_count}
AVERAGE ENGAGEMENT: {avg_engagement:.2f}/100

TOP THEMES:
"""
        for theme in themes[:5]:
            context += f"- {theme.get('theme')}: {theme.get('video_count')} videos, "
            context += f"engagement {theme.get('avg_engagement'):.2f}\n"
        
        context += "\nTOP KEYWORDS:\n"
        for kw in keywords[:10]:
            context += f"- {kw.get('keyword')} ({kw.get('frequency')} occurrences)\n"
        
        if anomalies:
            context += f"\nANOMALIES DETECTED: {len(anomalies)} videos with unusual engagement\n"
        
        return context
    
    def _build_prompt(self, context: str) -> str:
        """Build LLM prompt for intelligence generation."""
        
        return f"""You are a strategic intelligence analyst for TrendOps, an AI trend intelligence platform.

Analyze the following YouTube trending data and generate a professional, investor-ready intelligence report.

DATA:
{context}

Generate a structured report with the following sections:

## EXECUTIVE SUMMARY
(2-3 sentences summarizing key findings)

## EMERGING PATTERNS
(Identify 3-4 significant patterns or trends)

## STRATEGIC IMPLICATIONS
(What do these trends mean for businesses and creators?)

## STARTUP OPPORTUNITIES
(List exactly 3 specific startup ideas based on these trends)
1. [Idea name]: [One sentence description]
2. [Idea name]: [One sentence description]
3. [Idea name]: [One sentence description]

## CONTENT IDEAS
(List exactly 5 content creation opportunities)
1. [Content idea]
2. [Content idea]
3. [Content idea]
4. [Content idea]
5. [Content idea]

Keep the tone professional, data-driven, and actionable. Focus on insights that would be valuable to executives, investors, and content strategists.
"""
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from the report."""
        
        lines = text.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if section_name in line.upper():
                in_section = True
                continue
            elif line.startswith('##') and in_section:
                break
            elif in_section and line.strip():
                section_lines.append(line.strip())
        
        return ' '.join(section_lines) if section_lines else "Not available"
    
    def _extract_list_section(self, text: str, section_name: str) -> list:
        """Extract a list section from the report."""
        
        lines = text.split('\n')
        items = []
        in_section = False
        
        for line in lines:
            if section_name in line.upper():
                in_section = True
                continue
            elif line.startswith('##') and in_section:
                break
            elif in_section and line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-')):
                # Remove numbering/bullets
                item = line.strip().lstrip('0123456789.-) ')
                if item:
                    items.append(item)
        
        return items if items else ["Not available"]

intelligence_agent = IntelligenceAgent()
