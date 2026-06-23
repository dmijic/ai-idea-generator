import os
import json
import argparse
from dotenv import load_dotenv
from anthropic import Anthropic
from pathlib import Path
from datetime import datetime

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_ideas(topic: str, count: int) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Generiraj točno {count} ideje za sadržaj na temu: {topic}. Primjer: [\"ideja 1\", \"ideja 2\", \"ideja 3\"]. Vrati SAMO JSON array, bez backtickova, bez code blokova, bez ikakvog dodatnog teksta."
        }]
    )
    return message.content[0].text

def save_ideas(topic: str, ideas: list[str]) -> Path:
    Path("output").mkdir(exist_ok=True)
    filename = f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{topic[:20]}.json"
    data = {"topic": topic, "ideas": ideas, "generated_at": datetime.now().isoformat()}
    Path(filename).write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return Path(filename)

def parse_args():
    parser = argparse.ArgumentParser(description="AI Idea Generator")
    parser.add_argument("--topic", type=str, help="Tema za generiranje ideja")
    parser.add_argument("--count", type=int, default=3, choices=range(1, 11), help="Broj ideja za generiranje")
    parser.add_argument("--history", action="store_true", help="Prikaži povijest generiranih ideja")
    return parser.parse_args()

def print_ideas(ideas: list[str]):
    print("Generirane ideje:")
    for i, idea in enumerate(ideas, start=1):
        print(f"{i}. {idea}")

def show_history():
    files = sorted(Path("output").iterdir())
    for f in files:
        data = json.loads(Path(f).read_text())
        topic = data.get("topic", "Nepoznata tema")
        ideas = data.get("ideas", [])
        timestamp = datetime.fromisoformat(data.get("generated_at", "Nepoznat datum"))
        print("-" * 40)
        print(f"Datum generiranja: {timestamp.strftime('%d.%m.%Y. u %H:%M')}")
        print(f"Tema: {topic}")
        print("Ideje:")
        for i, idea in enumerate(ideas, start=1):
            print(f"  {i}. {idea}")


def main():
    args = parse_args()
    topic = args.topic
    count = args.count
    raw = None
    if args.history:
        show_history()
        return
    if not args.topic:
        print("Greška: Tema je obavezna. Dodaj --topic 'tvoja tema' argument.")
        return
    try:
        raw = generate_ideas(topic, count)
        ideas = json.loads(raw)
        print_ideas(ideas)
        saved = save_ideas(topic, ideas)
        print(f"Spremljeno u {saved}")
        show_history()
    except json.JSONDecodeError:
        print(f"Claude nije vratio validni JSON: {raw}")
        return
    except Exception as e:
        print(f"Greška pri pozivu API-ja: {e}")
        return

if __name__ == "__main__":
    main()