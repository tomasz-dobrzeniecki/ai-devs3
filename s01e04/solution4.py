from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """Jesteś robotem przemysłowym poruszającym się po siatce magazynowej. Siatka składa się z:
Kolumn: A do F (od lewej do prawej)
Rzędów: 1 do 4 (od góry do dołu)
Każda pozycja opisana jest w formacie [kolumna][rząd], np. A1, C3, F4
Startujesz w pozycji A4, a twoim celem jest F4. Musisz poruszać się po siatce, wykonując dokładnie 9 kroków, aby dotrzeć do celu.
Możesz używać tylko następujących poleceń ruchu:
"UP" (w górę), "DOWN" (w dół), "LEFT" (w lewo), "RIGHT" (w prawo)
Twoim zadaniem jest wygenerować poprawny plik JSON zawierający dwa pola:
"thinking" – krótki opis trasy (np. jak obchodzisz przeszkody)
"steps" – pojedynczy string z dokładnie 9 ruchami, rozdzielonymi przecinkami, np. "UP, RIGHT, RIGHT, DOWN, RIGHT, UP, RIGHT, DOWN, RIGHT"
Zwróć tylko poprawny JSON.
Masz wykonać następującą trasę góra, góra, prawo, prawo, dół, dół, prawo, prawo, prawo"""

# Make the API call
response = client.chat.completions.create(
    model="gpt-4o-mini", 
    messages=[{"role": "user", "content": prompt}]
)

# Print the response
print(response.choices[0].message.content)