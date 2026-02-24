# Sentiment Analysis FastAPI Endpoint

## Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Deploy to Railway (free, quick)
1. Push to GitHub
2. Connect repo at railway.app
3. Set env var: OPENAI_API_KEY
4. Deploy → get public URL

## Deploy to Render (free tier)
1. Push to GitHub
2. New Web Service at render.com
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Set OPENAI_API_KEY env var

## Test Locally
```bash
curl -X POST http://localhost:8000/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "This product is amazing!"}'
# Expected: {"sentiment": "positive", "rating": 5}

curl -X POST http://localhost:8000/comment \
  -H "Content-Type: application/json" \
  -d '{"comment": "Terrible experience, never buying again"}'
# Expected: {"sentiment": "negative", "rating": 1}
```

## Endpoint
- **POST /comment** — Analyze comment sentiment
- **GET /health** — Health check
