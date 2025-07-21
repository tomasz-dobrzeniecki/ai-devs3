Musisz poprawić plik kalibracyjny dla jednego z robotów przemysłowych. To dość popularny w 2024 roku format JSON. Dane testowe zawierają prawdopodobnie błędne obliczenia oraz luki w pytaniach otwartych. Popraw proszę ten plik i prześlij nam go już po poprawkach. Tylko uważaj na rozmiar kontekstu modeli LLM, z którymi pracujesz — plik się nie zmieści w tym limicie.

Plik do pobrania zabezpieczony jest Twoim kluczem API. Podmień “TWOJ-KLUCZ” w adresie na wartość klucza z centrali.

https://c3ntrala.ag3nts.org/data/TWOJ-KLUCZ/json.txt

Poprawną odpowiedź wyślij proszę pod poniższy adres, w formie takiej, jak w przypadku Poligonu. Nazwa zadanie to JSON.

https://c3ntrala.ag3nts.org/report 



Co trzeba zrobić w zadaniu?

1. Pobierasz plik TXT podany wyżej (tylko podmień TWOJ-KLUCZ) na poprawną wartość

2. Ten plik się nie zmienia. Nie musisz go pobierać cyklicznie. Jest statyczny.

3. Plik zawiera błędy w obliczeniach - musisz je poprawić (ale gdzie one są?). Czy tutaj potrzebujesz LLM?

4. Plik w niektórych danych testowych zawiera pole “test” z polami “q” (question/pytanie) oraz “a” (answer/odpowiedź). Użyj LLM do udzielenia odpowiedzi.

5. Rozmiar dokumentu jest zbyt duży, aby ogarnąć go współczesnymi LLM-ami (zmieści się w niektórych oknach kontekstowych wejścia, ale już nie w oknie wyjścia).

6. Zadanie na pewno trzeba rozbić na mniejsze części, a wywołanie LLM-a prawdopodobnie będzie wielokrotne (ale da się to także zrobić jednym requestem).

7. W tym zadaniu trzeba mądrze zdecydować, którą część zadania należy delegować do sztucznej inteligencji, a którą warto rozwiązać w klasyczny, programistyczny sposób. Decyzja oczywiście należy do Ciebie, ale zrób to proszę rozsądnie.



Wskazówki:

- zauważ że swój klucz API musisz umieścić w dwóch miejscach w odpowiedzi (zerknij na format odpowiedzi poniżej)
- w odpowiedzi, w polu "answer" ma znaleźć się cała zawartość poprawionego pliku, jako obiekt. Uważaj, aby nie wysłać go przypadkiem jako tekst :) 
- czy potrzebujesz LLM do obliczeń? Poprawianie obliczeń można wykonać programistycznie
- Pamiętaj, że odpowiedź wysyłasz jako JSON, metodą POST do API na endpoint: https://c3ntrala.ag3nts.org/report



Format odpowiedzi 

{
  "task": "JSON",
  "apikey": "%PUT-YOUR-API-KEY-HERE%",
  "answer": {
    "apikey": "%PUT-YOUR-API-KEY-HERE%",
    "description": "This is simple calibration data used for testing purposes. Do not use it in production environment!",
    "copyright": "Copyright (C) 2238 by BanAN Technologies Inc.",
    "test-data": [
      {
        "question": "45 + 86",
        "answer": 131
      },
      {
        "question": "97 + 34",
        "answer": 131
      },
      {
        "question": "97 + 6",
        "answer": 103,
        "test": {
          "q": "name of the 2020 USA president",
          "a": "???"
        }
      },
.........
    ]
  }
}


Dokumentacja Swagger

https://c3ntrala.ag3nts.org/swagger/?spec=S01E03-222lkaf89.json
--

# Wyjaśnienie działania modułów (S01E03)

Poniżej znajdziesz prosty opis, co robi każdy moduł w tym zadaniu:

---

**1. config.py**
Przechowuje ustawienia i zmienne konfiguracyjne, takie jak klucz API, adresy URL do pobierania i wysyłania plików. Dzięki temu łatwo zmienić ustawienia bez modyfikowania kodu w innych plikach.

**2. main.py**
To główny plik uruchamiający cały proces. Po kolei:
- Pobiera dane wejściowe z serwera,
- Przekazuje je do przetworzenia,
- Wysyła poprawione dane z powrotem na serwer.

**3. downloader.py**
Odpowiada za pobranie pliku wejściowego (JSON) z serwera. Zwraca dane w postaci słownika (dict).

**4. processor.py**
Przetwarza dane testowe:
- Sprawdza, czy odpowiedzi na pytania matematyczne są poprawne i poprawia je,
- Zbiera pytania otwarte (gdzie odpowiedź to "???") i przekazuje je do AI,
- Wstawia odpowiedzi AI z powrotem do danych.

**5. correction.py**
Zawiera funkcję do poprawiania prostych działań matematycznych (np. dodawania). Jeśli odpowiedź jest błędna, poprawia ją klasycznie, bez użycia AI.

**6. llm_client.py**
Komunikuje się z modelem językowym (np. OpenAI GPT). Wysyła pytania otwarte i odbiera odpowiedzi, które potem trafiają do danych.

**7. submitter.py**
Buduje końcowy plik z poprawionymi danymi i wysyła go na serwer za pomocą żądania POST.

**8. readme.md / exp.md**
Zawiera opis zadania, instrukcje oraz wyjaśnienia, jak działa cały proces.

---

### Podsumowanie

- Pobieramy dane z serwera.
- Poprawiamy matematyczne odpowiedzi klasycznie.
- Pytania otwarte uzupełniamy za pomocą AI.
- Wysyłamy poprawione dane z powrotem na serwer.

Dzięki podziałowi na moduły, kod jest czytelny, łatwy do utrzymania i można go łatwo rozbudować. 