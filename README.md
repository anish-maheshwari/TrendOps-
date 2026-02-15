# TrendOps — AI Trend Intelligence Control Plane

**Production-Grade Native MCP Agent Swarm for Strategic YouTube Analysis**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 Executive Summary
**TrendOps** is the first **Native MCP Agent Swarm** architected specifically for the **Archestra Control Plane**. Instead of a monolithic application, TrendOps decomposes the intelligence lifecycle into atomic, governed MCP Tools. It ingests live YouTube metadata, mathematically clusters subcultures, and generates investor-ready strategic insights.

Built as a reference implementation for the **2 Fast 2 MCP** hackathon, it demonstrates:
1.  **Governance-First Architecture**: Policy enforcement before execution.
2.  **Modular Orchestration**: Standardized MCP Tool exposure.
3.  **Enterprise Observability**: Structured JSON tracing and cost tracking.

---

## 🏗 Architecture Overview

TrendOps implements a **four-agent swarm** with clear separation of concerns, designed to be orchestrated by a runtime like Archestra.

```text
┌─────────────────────────────────────────────────────────────┐
│                 Archestra Control Plane                      │
│            (Agent Orchestrator & Policy Enforcement)         │
└────────────────────────┬────────────────────────────────────┘
                         │ JSON-RPC / SSE (MCP v1.2)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              TrendOps MCP Server Layer                       │
│              (app/mcp_server.py)                             │
│                                                             │
│   ┌──────────────┐    ┌──────────────┐    ┌─────────────┐   │
│   │ Governance   │    │  Data Agent  │    │ Intelligence│   │
│   │   (Tool)     │◄──►│    (Tool)    │◄──►│    (Tool)   │   │
│   └──────────────┘    └──────────────┘    └─────────────┘   │
└─────────────────────────────────────────────────────────────┘
                         │ Internal Logic
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Microservice Runtime                 │
│              (Legacy REST Interface for Web UI)              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 Agent Responsibility Matrix

| Agent | Responsibility | Core Logic | Output |
| :--- | :--- | :--- | :--- |
| **🛡️ Governance** | Policy Enforcement | Validates regions, categories, and rate limits. | Validation status, audit trace. |
| **📡 Data** | High-Traffic Ingest | YouTube API v3 integration & error handling. | Structured video metadata. |
| **📊 Analytics** | Theme Synthesis | TF-IDF keyword extraction & K-Means clustering. | Themes, engagement scores, anomalies. |
| **📈 Intelligence** | Strategic Execution | Generates executive reports via Gemini Flash LLM. | Investor reports, startup ideas. |

---

## 🔄 Autonomous Data Flow

```text
User Request
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. GOVERNANCE: Validate Input & Policies                    │
│    • Check region code (ISO 3166-1)                         │
│    • Validate category ID & Enforce rate limits             │
│    • Log request initiation for audit                       │
└────────────────────────┬────────────────────────────────────┘
                         │ [Validation Passed]
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DATA: Fetch YouTube Trending Videos                     │
│    • Multi-source YouTube ingestion                         │
│    • Log API call metrics & handle quota errors             │
└────────────────────────┬────────────────────────────────────┘
                         │ [Raw Data]
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. ANALYTICS: Process & Synthesize                         │
│    • Extract keywords (TF-IDF)                              │
│    • Cluster themes (K-means) & Score engagement            │
│    • Detect statistical anomalies                           │
└────────────────────────┬────────────────────────────────────┘
                         │ [Structured Analytics]
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. INTELLIGENCE: Strategic Insights generation             │
│    • Build context for Swarm LLM                            │
│    • Generate executive summary & startup opportunities     │
│    • Track token usage for cost observability               │
└────────────────────────┬────────────────────────────────────┘
                         │ [Intelligence Report]
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. GOVERNANCE: Generate Execution Trace                    │
│    • Compile full execution log                             │
│    • Return metrics & results to Archestra Control Plane    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
                    JSON Response
```

---

## � Real-World Case Study: Regional Insights
During analysis of **Indian Music Trends**, TrendOps detected that **70% of top content** was hyper-local Haryanvi regional music, not traditional Bollywood.
- **The Insight**: Identified a "Hyper-Loyal" niche with 90/100 engagement.
- **The Value**: Recommended reallocation of influencer spend to regional stars like "Raushan" and "Kumar," predicting an undervalued market breakout.

---

## 🔐 Security & Governance Guardrails

### 1. API Key Management
- Zero hardcoding; all keys are handled via `.env` (managed by `.gitignore`).
- Application fails-fast if required keys are missing during startup.

### 2. Policy Enforcement
- **Region Whitelist**: Only accepts pre-verified regions (US, IN, GB, etc.).
- **Rate Limiting**: `MAX_REQUESTS_PER_SESSION` protects API quotas and prevents D-DoS patterns on agent swarms.

### 3. Failover Strategy
- If the **Intelligence Agent** (LLM) fails, the system gracefully degrades to provide raw **Analytics** data so the mission is never at a total loss.

---

## � Observability & Tracing
TrendOps uses **Structured JSON Logging** designed for ingestion by Archestra's monitoring stack. Every mission produces a unique execution trace:
- **Trace IDs**: Monitor latency across agent handoffs.
- **Token Tracking**: Real-time observability of LLM costs.
- **Audit Logs**: Full transparency into every tool call made by the swarm.

Access via: `GET /governance/trace`

---

## � Quick Start / Deployment

### 1. Simple Local Setup
```bash
git clone https://github.com/your-username/TrendOps.git
cd TrendOps
pip install -r requirements.txt
cp .env.example .env # Add your YOUTUBE_API_KEY and GOOGLE_API_KEY
python -m app.main
```

### 2. Docker Deployment (Recommended for Archestra)
```bash
docker build -t trendops-control-plane .
docker run -p 8000:8000 --env-file .env trendops-control-plane
```

### 3. Vercel Deployment (Serverless)
TrendOps is optimized for Vercel. Simply connect your repo and add your Environment Variables in the Vercel Dashboard; the `vercel.json` and `app/main.py` entrypoints are pre-configured.

---

## � Archestra MCP Integration
Expose the TrendOps swarm as a set of standardized tools in any MCP-compliant client:
```bash
# Start the MCP Server
python app/mcp_server.py
```
**Available Tools:** `validate_request`, `fetch_trending_data`, `analyze_trends`, `generate_intelligence`.

---

## 📄 License
MIT License. Built for the **2 Fast 2 MCP Hackathon** 🚀
By [Anish Maheshwari](https://www.linkedin.com/in/anish-maheshwarii)
