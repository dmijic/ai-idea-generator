from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from app import IdeaGenerator

load_dotenv()
api_key=os.getenv("ANTHROPIC_API_KEY")

app = FastAPI()
generator = IdeaGenerator(api_key = api_key)


class GenerateRequest(BaseModel):
    topic: str
    count: int = 3

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/generate")
def generate_ideas(request: GenerateRequest):
    try:
        raw = generator.generate(topic=request.topic, count=request.count)
        ideas = json.loads(raw)
        saved = generator.save(topic=request.topic, ideas=ideas)
        return {"message": f"Ideje su generirane i spremljene: {str(saved)}."}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Claude nije vratio validni JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Interna greška servera.")

@app.get("/history")
def get_history():
    try:
        history = generator.history()
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Interna greška servera.")