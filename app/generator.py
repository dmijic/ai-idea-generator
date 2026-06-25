import json
from anthropic import Anthropic
from pathlib import Path
from datetime import datetime

class IdeaGenerator:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
    
    def generate(self, topic: str, count: int) -> str:
        message = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"Generiraj točno {count} ideje za sadržaj na temu: {topic}. Primjer: [\"ideja 1\", \"ideja 2\", \"ideja 3\"]. Vrati SAMO JSON array, bez backtickova, bez code blokova, bez ikakvog dodatnog teksta."
            }]
        )
        return message.content[0].text
    
    def save(self, topic: str, ideas: list[str]) -> Path:
        Path("output").mkdir(exist_ok=True)
        filename = f"output/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{topic[:20]}.json"
        data = {"topic": topic, "ideas": ideas, "generated_at": datetime.now().isoformat()}
        Path(filename).write_text(json.dumps(data, indent=2, ensure_ascii=False))
        return Path(filename)

    def history(self):
        files = sorted(Path("output").iterdir())
        history = []
        for f in files:
            data = json.loads(Path(f).read_text())
            topic = data.get("topic", "Nepoznata tema")
            ideas = data.get("ideas", [])
            timestamp = datetime.fromisoformat(data.get("generated_at", "Nepoznat datum"))
            history.append({"topic": topic, "ideas": ideas, "timestamp": timestamp.strftime('%d.%m.%Y. u %H:%M')})
        return history

    def print_ideas(self, history):
        for entry in history:
            print("-" * 40)
            print(f"Datum generiranja: {entry['timestamp']}")
            print(f"Tema: {entry['topic']}")
            print("Ideje:")
            for i, idea in enumerate(entry['ideas'], start=1):
                print(f"  {i}. {idea}")