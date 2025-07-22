from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Jesteś robotem poruszającym się po siatce magazynowej o 6 kolumnach (A do F) i 4 rzędach (1 do 4). A1 to górny lewy róg, F4 to dolny prawy róg.

Twoja pozycja początkowa to A4. Celem jest dotarcie do F4. Możesz poruszać się tylko: UP, DOWN, LEFT, RIGHT. Nie możesz przechodzić przez ściany.

Oto mapa magazynu (czytaj od góry):

Rząd 1: . # . . . .   → A1 B1 C1 D1 E1 F1  
Rząd 2: . . . # . .   → A2 B2 C2 D2 E2 F2  
Rząd 3: . # . # . .   → A3 B3 C3 D3 E3 F3  
Rząd 4: S # . . . C   → A4 B4 C4 D4 E4 F4  

S = start (A4), C = komputer (F4), # = ściana

Podaj wynik w formacie JSON:

{
  "thinking": "Startuję w A4. Idę w górę do A3 (wolne), potem do A2 (wolne), w prawo do B2 (wolne), w prawo do C2 (wolne), w dół do C3 (wolne), w dół do C4 (wolne), potem w prawo do D4, E4, F4.",
  "steps": "UP, UP, RIGHT, RIGHT, DOWN, DOWN, RIGHT, RIGHT, RIGHT"
}

Zwróć tylko poprawny JSON. Nie dodawaj komentarzy.
"""
prompt2 = """Jesteś robotem przemysłowym poruszającym się po siatce magazynowej. Siatka składa się z:
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
response = client.responses.create(
    model="gpt-4o-mini",
    input=prompt,
    temperature=0
)
print(response.output_text)