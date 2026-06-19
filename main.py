import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic as ai
from pathlib import Path
from datetime import datetime

load_dotenv()
client = ai(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_ideas(topic: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Generiraj točno 3 ideje za sadržaj na temu: {topic}. Odgovori kao JSON array stringova, bez ikakvog dodatnog teksta. Primjer: [\"ideja 1\", \"ideja 2\", \"ideja 3\"]"
        }]
    )
    return message.content[0].text

def save_ideas(topic: str, ideas: list[str]) -> Path:
    Path("output").mkdir(exist_ok=True)
    filename = f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{topic[:20]}.json"
    data = {"topic": topic, "ideas": ideas, "generated_at": datetime.now().isoformat()}
    Path(filename).write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return Path(filename)

def main():
    topic = input("Unesi temu: ")
    raw = None
    try:
        raw = generate_ideas(topic)
        ideas = json.loads(raw)
        saved = save_ideas(topic, ideas)
        print(f"Spremljeno u {saved}")
    except json.JSONDecodeError:
        print(f"Claude nije vratio validni JSON: {raw}")
        return
    except Exception as e:
        print(f"Greška pri pozivu API-ja: {e}")
        return

if __name__ == "__main__":
    main()