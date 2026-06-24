from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import IdeaGenerator, api_key
import json

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
        return {"ideas": ideas}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Claude nije vratio validni JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Interna greška servera.")
