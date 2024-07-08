from openai import OpenAI
from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter()
client = OpenAI()

class BookRequest(BaseModel):
    topic: str

def generate_text(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content

@router.post("/generate_book")
async def generate_book(request: BookRequest):
    try:
        text = generate_text(f"Write a detailed book on the topic: {request.topic}")
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))