# TrendOps - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Get Your API Keys

1. **YouTube Data API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable "YouTube Data API v3"
   - Create credentials → API Key
   - Copy the key

2. **Anthropic API Key**
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Sign up or log in
   - Navigate to API Keys
   - Create a new key
   - Copy the key

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and paste your keys
# YOUTUBE_API_KEY=AIzaSy...
# ANTHROPIC_API_KEY=sk-ant-...
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Setup

```bash
python test_setup.py
```

### Step 5: Run TrendOps

```bash
python -m app.main
```

Visit: http://localhost:8000

### 📦 Deployment
Deploy with a single command to any container runtime (Kubernetes, AWS ECS, Google Cloud Run):

```bash
docker run -p 8000:8000 --env-file .env trendops:latest
```

This stateless design ensures TrendOps is ready for **horizontal auto-scaling** within an orchestrated environment.

### Step 6: Test the API

```bash
# Health check
curl http://localhost:8000/health

# Analyze US tech trends
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"region_code": "US", "category_id": "28", "max_results": 10}'
```

## 🐳 Docker Quick Start

```bash
# Build
docker build -t trendops .

# Run
docker run -p 8000:8000 \
  -e YOUTUBE_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  trendops
```

## 📚 Next Steps

- Read the full [README.md](README.md) for architecture details
- Check [API Documentation](http://localhost:8000/docs) (when running)
- View execution traces at `/governance/trace`

## ❓ Troubleshooting

**Import errors?**
```bash
pip install -r requirements.txt
```

**API key errors?**
- Check `.env` file exists
- Verify keys are correct
- Ensure no extra spaces

**Port 8000 in use?**
```bash
# Change port in app/main.py or run:
uvicorn app.main:app --port 8080
```

---

Built for **2 Fast 2 MCP** hackathon 🏁
