import json
import argparse
from app import IdeaGenerator
from app.config import settings
from app.logger import get_logger

logger = get_logger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="AI Idea Generator")
    parser.add_argument("--topic", type=str, help="Tema za generiranje ideja")
    parser.add_argument("--count", type=int, default=3, choices=range(1, 11), help="Broj ideja za generiranje")
    parser.add_argument("--history", action="store_true", help="Prikaži povijest generiranih ideja")
    return parser.parse_args()

def main():
    args = parse_args()
    generator = IdeaGenerator(api_key = settings.anthropic_api_key)
    topic = args.topic
    count = args.count
    raw = None
    if args.history:
        history = generator.history()
        generator.print_ideas(history)
        return
    if not args.topic:
        print("Greška: Tema je obavezna. Dodaj --topic 'tvoja tema' argument.")
        return
    try:
        raw = generator.generate(topic, count)
        ideas = json.loads(raw)
        saved = generator.save(topic, ideas)
        print(f"Spremljeno u {saved}")
    except json.JSONDecodeError:
        print(f"Claude nije vratio validni JSON: {raw}")
        return
    except Exception as e:
        logger.error(f"Greška pri pozivu API-ja: {e}")
        print(f"Greška pri pozivu API-ja: {e}")
        return