Python skripta koja prima korisnikov upit i šalje prompt prema Anthropic API-ju.

User input:
tema za koju želimo da nam Claude generira 3 ideje za naslove.

Output:
json file u folderu output

struktura outputa:

tema:
prijedlozi naslova:
prijedlog naslova 1
prijedlog naslova 2
prijedlog naslova 3
timestamp

Pokretanje skripte:

ući u folder ai-idea-generator
cd ai-idea-generator
pokrenuti python venv naredbom:
source venv/bin/activate
pokrenuti main.py naredbom:
python main.py
