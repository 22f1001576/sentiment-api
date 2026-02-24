from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class CommentRequest(BaseModel):
    comment: str

SENTIMENT_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "sentiment_analysis",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "sentiment": {
                    "type": "string",
                    "enum": ["positive", "negative", "neutral"]
                },
                "rating": {
                    "type": "integer",
                    "enum": [1, 2, 3, 4, 5]
                }
            },
            "required": ["sentiment", "rating"],
            "additionalProperties": False
        }
    }
}

@app.post("/comment")
async def analyze_comment(request: CommentRequest):
    if not request.comment or not request.comment.strip():
        raise HTTPException(status_code=422, detail="Comment cannot be empty")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a sentiment analysis assistant. Analyze the sentiment of the given comment.\n"
                        "Return:\n"
                        "- sentiment: 'positive', 'negative', or 'neutral'\n"
                        "- rating: integer 1-5 where 5=highly positive, 3=neutral, 1=highly negative\n"
                        "Be consistent: positive sentiment → rating 4-5, neutral → 3, negative → 1-2."
                    )
                },
                {
                    "role": "user",
                    "content": request.comment
                }
            ],
            response_format=SENTIMENT_SCHEMA
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return JSONResponse(content=result, media_type="application/json")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API error: {str(e)}")


@app.get("/health")
async def health():
    return {"status": "ok"}
