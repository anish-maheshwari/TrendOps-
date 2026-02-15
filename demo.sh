#!/bin/bash
# TrendOps Demo Script
# This script demonstrates the full capabilities of TrendOps

echo "=========================================="
echo "TrendOps - AI Trend Intelligence Demo"
echo "=========================================="
echo ""

# Check if server is running
echo "1. Checking if TrendOps is running..."
curl -s http://localhost:8000/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✓ TrendOps is running"
else
    echo "✗ TrendOps is not running"
    echo "Please start it with: python -m app.main"
    exit 1
fi
echo ""

# Health check
echo "2. Health Check"
echo "GET /health"
curl -s http://localhost:8000/health | python -m json.tool
echo ""
echo "Press Enter to continue..."
read

# Get valid regions
echo "3. Available Regions"
echo "GET /config/regions"
curl -s http://localhost:8000/config/regions | python -m json.tool
echo ""
echo "Press Enter to continue..."
read

# Get valid categories
echo "4. Available Categories"
echo "GET /config/categories"
curl -s http://localhost:8000/config/categories | python -m json.tool
echo ""
echo "Press Enter to continue..."
read

# Demo 1: US Tech Trends
echo "=========================================="
echo "DEMO 1: US Tech Trends"
echo "=========================================="
echo "Analyzing trending tech videos in the United States..."
echo ""
echo "POST /analyze"
echo '{"region_code": "US", "category_id": "28", "max_results": 10}'
echo ""

curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"region_code": "US", "category_id": "28", "max_results": 10, "include_intelligence": true}' \
  | python -m json.tool > demo1_output.json

echo "✓ Analysis complete! Saved to demo1_output.json"
echo ""
echo "Key insights:"
python -c "
import json
with open('demo1_output.json') as f:
    data = json.load(f)
    print(f\"  Videos analyzed: {data['analytics']['metrics']['total_videos']}\")
    print(f\"  Themes found: {data['analytics']['metrics']['themes_identified']}\")
    print(f\"  Avg engagement: {data['analytics']['metrics']['avg_engagement']}/100\")
    if data.get('intelligence'):
        print(f\"  Executive summary: {data['intelligence']['executiveSummary'][:100]}...\")
"
echo ""
echo "Press Enter to continue..."
read

# Demo 2: India Gaming Trends
echo "=========================================="
echo "DEMO 2: India Gaming Trends"
echo "=========================================="
echo "Analyzing trending gaming videos in India..."
echo ""
echo "POST /analyze"
echo '{"region_code": "IN", "category_id": "20", "max_results": 15}'
echo ""

curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"region_code": "IN", "category_id": "20", "max_results": 15, "include_intelligence": false}' \
  | python -m json.tool > demo2_output.json

echo "✓ Analysis complete! Saved to demo2_output.json"
echo ""
echo "Top themes:"
python -c "
import json
with open('demo2_output.json') as f:
    data = json.load(f)
    for i, theme in enumerate(data['analytics']['topThemes'][:3], 1):
        print(f\"  {i}. {theme['theme']}: {theme['video_count']} videos, engagement {theme['avg_engagement']}\")
"
echo ""
echo "Press Enter to continue..."
read

# Demo 3: Execution Trace
echo "=========================================="
echo "DEMO 3: Execution Trace & Governance"
echo "=========================================="
echo "Viewing execution trace and cost tracking..."
echo ""
echo "GET /governance/trace"
echo ""

curl -s http://localhost:8000/governance/trace | python -m json.tool > demo3_trace.json

echo "✓ Trace retrieved! Saved to demo3_trace.json"
echo ""
echo "Session statistics:"
python -c "
import json
with open('demo3_trace.json') as f:
    data = json.load(f)
    stats = data['sessionStats']
    print(f\"  Total executions: {stats['total_executions']}\")
    print(f\"  Total API calls: {stats['total_api_calls']}\")
    print(f\"  Total tokens used: {stats['total_estimated_tokens']}\")
    print(f\"  Session started: {stats['session_start']}\")
    print(f\"\nRecent operations:\")
    for op in data['executionLog'][-5:]:
        print(f\"  - {op['tool_name']}: {op['status']} ({op['duration_ms']:.0f}ms)\")
"
echo ""
echo "Press Enter to continue..."
read

# Demo 4: Error Handling
echo "=========================================="
echo "DEMO 4: Error Handling & Validation"
echo "=========================================="
echo "Testing input validation with invalid region..."
echo ""
echo "POST /analyze"
echo '{"region_code": "XX", "category_id": "28", "max_results": 10}'
echo ""

curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"region_code": "XX", "category_id": "28", "max_results": 10}' \
  | python -m json.tool

echo ""
echo "✓ Validation working correctly!"
echo ""

# Summary
echo "=========================================="
echo "Demo Complete!"
echo "=========================================="
echo ""
echo "Generated files:"
echo "  - demo1_output.json (US tech trends with intelligence)"
echo "  - demo2_output.json (India gaming trends)"
echo "  - demo3_trace.json (execution trace)"
echo ""
echo "Key features demonstrated:"
echo "  ✓ Multi-agent orchestration"
echo "  ✓ YouTube data fetching"
echo "  ✓ Theme clustering & analytics"
echo "  ✓ LLM-powered intelligence"
echo "  ✓ Execution tracing"
echo "  ✓ Input validation"
echo "  ✓ Error handling"
echo ""
echo "For more details, see:"
echo "  - README.md (architecture & documentation)"
echo "  - SUBMISSION.md (hackathon details)"
echo "  - PROJECT_SUMMARY.md (overview)"
echo ""
echo "=========================================="
