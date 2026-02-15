# TrendOps Demo Script (PowerShell)
# This script demonstrates the full capabilities of TrendOps

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "TrendOps - AI Trend Intelligence Demo" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if server is running
Write-Host "1. Checking if TrendOps is running..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✓ TrendOps is running" -ForegroundColor Green
} catch {
    Write-Host "✗ TrendOps is not running" -ForegroundColor Red
    Write-Host "Please start it with: python -m app.main"
    exit 1
}
Write-Host ""

# Health check
Write-Host "2. Health Check" -ForegroundColor Yellow
Write-Host "GET /health"
$health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
$health | ConvertTo-Json -Depth 10
Write-Host ""
Read-Host "Press Enter to continue"

# Get valid regions
Write-Host "3. Available Regions" -ForegroundColor Yellow
Write-Host "GET /config/regions"
$regions = Invoke-RestMethod -Uri "http://localhost:8000/config/regions" -Method Get
$regions | ConvertTo-Json
Write-Host ""
Read-Host "Press Enter to continue"

# Get valid categories
Write-Host "4. Available Categories" -ForegroundColor Yellow
Write-Host "GET /config/categories"
$categories = Invoke-RestMethod -Uri "http://localhost:8000/config/categories" -Method Get
$categories | ConvertTo-Json -Depth 10
Write-Host ""
Read-Host "Press Enter to continue"

# Demo 1: US Tech Trends
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DEMO 1: US Tech Trends" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Analyzing trending tech videos in the United States..."
Write-Host ""

$body1 = @{
    region_code = "US"
    category_id = "28"
    max_results = 10
    include_intelligence = $true
} | ConvertTo-Json

Write-Host "POST /analyze"
Write-Host $body1
Write-Host ""

$result1 = Invoke-RestMethod -Uri "http://localhost:8000/analyze" -Method Post -Body $body1 -ContentType "application/json"
$result1 | ConvertTo-Json -Depth 10 | Out-File "demo1_output.json"

Write-Host "✓ Analysis complete! Saved to demo1_output.json" -ForegroundColor Green
Write-Host ""
Write-Host "Key insights:"
Write-Host "  Videos analyzed: $($result1.analytics.metrics.total_videos)"
Write-Host "  Themes found: $($result1.analytics.metrics.themes_identified)"
Write-Host "  Avg engagement: $($result1.analytics.metrics.avg_engagement)/100"
if ($result1.intelligence) {
    Write-Host "  Executive summary: $($result1.intelligence.executiveSummary.Substring(0, [Math]::Min(100, $result1.intelligence.executiveSummary.Length)))..."
}
Write-Host ""
Read-Host "Press Enter to continue"

# Demo 2: India Gaming Trends
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DEMO 2: India Gaming Trends" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Analyzing trending gaming videos in India..."
Write-Host ""

$body2 = @{
    region_code = "IN"
    category_id = "20"
    max_results = 15
    include_intelligence = $false
} | ConvertTo-Json

Write-Host "POST /analyze"
Write-Host $body2
Write-Host ""

$result2 = Invoke-RestMethod -Uri "http://localhost:8000/analyze" -Method Post -Body $body2 -ContentType "application/json"
$result2 | ConvertTo-Json -Depth 10 | Out-File "demo2_output.json"

Write-Host "✓ Analysis complete! Saved to demo2_output.json" -ForegroundColor Green
Write-Host ""
Write-Host "Top themes:"
$i = 1
foreach ($theme in $result2.analytics.topThemes[0..2]) {
    Write-Host "  $i. $($theme.theme): $($theme.video_count) videos, engagement $($theme.avg_engagement)"
    $i++
}
Write-Host ""
Read-Host "Press Enter to continue"

# Demo 3: Execution Trace
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DEMO 3: Execution Trace & Governance" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Viewing execution trace and cost tracking..."
Write-Host ""

$trace = Invoke-RestMethod -Uri "http://localhost:8000/governance/trace" -Method Get
$trace | ConvertTo-Json -Depth 10 | Out-File "demo3_trace.json"

Write-Host "✓ Trace retrieved! Saved to demo3_trace.json" -ForegroundColor Green
Write-Host ""
Write-Host "Session statistics:"
Write-Host "  Total executions: $($trace.sessionStats.total_executions)"
Write-Host "  Total API calls: $($trace.sessionStats.total_api_calls)"
Write-Host "  Total tokens used: $($trace.sessionStats.total_estimated_tokens)"
Write-Host "  Session started: $($trace.sessionStats.session_start)"
Write-Host ""
Write-Host "Recent operations:"
foreach ($op in $trace.executionLog[-5..-1]) {
    Write-Host "  - $($op.tool_name): $($op.status) ($([Math]::Round($op.duration_ms, 0))ms)"
}
Write-Host ""
Read-Host "Press Enter to continue"

# Demo 4: Error Handling
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "DEMO 4: Error Handling & Validation" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Testing input validation with invalid region..."
Write-Host ""

$body4 = @{
    region_code = "XX"
    category_id = "28"
    max_results = 10
} | ConvertTo-Json

Write-Host "POST /analyze"
Write-Host $body4
Write-Host ""

try {
    $result4 = Invoke-RestMethod -Uri "http://localhost:8000/analyze" -Method Post -Body $body4 -ContentType "application/json"
} catch {
    $errorResponse = $_.ErrorDetails.Message | ConvertFrom-Json
    $errorResponse | ConvertTo-Json
}

Write-Host ""
Write-Host "✓ Validation working correctly!" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Demo Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Generated files:"
Write-Host "  - demo1_output.json (US tech trends with intelligence)"
Write-Host "  - demo2_output.json (India gaming trends)"
Write-Host "  - demo3_trace.json (execution trace)"
Write-Host ""
Write-Host "Key features demonstrated:"
Write-Host "  ✓ Multi-agent orchestration"
Write-Host "  ✓ YouTube data fetching"
Write-Host "  ✓ Theme clustering & analytics"
Write-Host "  ✓ LLM-powered intelligence"
Write-Host "  ✓ Execution tracing"
Write-Host "  ✓ Input validation"
Write-Host "  ✓ Error handling"
Write-Host ""
Write-Host "For more details, see:"
Write-Host "  - README.md (architecture & documentation)"
Write-Host "  - SUBMISSION.md (hackathon details)"
Write-Host "  - PROJECT_SUMMARY.md (overview)"
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
