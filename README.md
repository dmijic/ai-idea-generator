# AI Idea Generator

Python CLI alat koji prima temu i generira ideje za sadržaj koristeći Claude API.

**Requirements:** Python 3.10+, Anthropic API key

## Pokretanje

1. Kloniraj repo i uđi u folder:

```bash
   git clone https://github.com/dmijic/ai-idea-generator.git
   cd ai-idea-generator
```

2. Kreiraj i aktiviraj venv:

```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Instaliraj dependencije:

```bash
   pip install -r requirements.txt
```

4. Kreiraj `.env` fajl s API ključem:

```
   ANTHROPIC_API_KEY=sk-ant-...
```

5. Pokreni:

```bash
   python main.py
```

## Output

JSON fajl u `output/` mapi sa strukturom:

```json
{
  "topic": "održiva gradnja",
  "ideas": ["ideja 1", "ideja 2", "ideja 3"],
  "generated_at": "2026-06-19T14:05:32"
}
```
