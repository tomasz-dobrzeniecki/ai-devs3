# S01E01

## Zadanie

Zaloguj się do systemu robotów pod adresem [https://xyz.ag3nts.org/](https://xyz.ag3nts.org/). Zdobyliśmy login i hasło do systemu (`tester` / `574e112a`). Problemem jednak jest ich system *anty-captcha*, który musisz spróbować obejść. Musisz jedynie zautomatyzować proces odpowiadania na pytanie zawarte w formularzu.

Przy okazji zaloguj się proszę w naszej centrali: [https://c3ntrala.ag3nts.org/](https://c3ntrala.ag3nts.org/). Tam też możesz zgłosić wszystkie znalezione do tej pory flagi.

**Nie analizuj jeszcze pamięci robota, którą przechwycisz. Zostawmy sobie to na jutro.**

### Co musisz zrobić w zadaniu?

- Zautomatyzuj logowanie do systemu robotów na stronie [https://xyz.ag3nts.org/](https://xyz.ag3nts.org/), korzystając z podanych danych dostępowych (`tester` / `574e112a`).
- Logowanie wymaga odpowiedzi na pytanie, które zmienia się co kilka sekund.
- Twoja aplikacja powinna:
  1. Pobierać aktualne pytanie ze strony (np. przez HTML + regex lub prosty parser tekstu).
  2. Wysyłać to pytanie do modelu LLM (np. GPT 4.1 Nano przez API) i pobierać odpowiedź.
  3. Wysyłać komplet danych (`username`, `password`, `answer`) do formularza logowania.

### Szczegóły techniczne

- **Adres logowania:** `https://xyz.ag3nts.org/`
- **Metoda:** `POST`
- **Nagłówki:**  
  `Content-Type: application/x-www-form-urlencoded`
- **Body:**  
  `username=tester&password=574e112a&answer=ODPOWIEDZ_Z_LLM`

Po przesłaniu formularza:
- Oczekuj odpowiedzi z adresem tajnej podstrony — odwiedź ją.
- Znajdziesz tam **flagę**, którą zgłoś na stronie: [https://c3ntrala.ag3nts.org/](https://c3ntrala.ag3nts.org/)

**Nie musisz korzystać z przeglądarki czy narzędzi typu Selenium. Wystarczy proste pobranie HTML (np. `requests` w Pythonie lub `fetch` w JS).**

**Dokumentacja Swagger:**  
[https://xyz.ag3nts.org/swagger-xyz/?spec=S01E01-28ewh223sf.json](https://xyz.ag3nts.org/swagger-xyz/?spec=S01E01-28ewh223sf.json)
---
## Wyjaśnienie rozwiązania zadania S01E01 (z loguru i wskazówkami dla AI engineer)

## Struktura rozwiązania
Projekt składa się z kilku modułów:
- `main.py` – główny plik uruchamiający cały proces.
- `web_client.py` – obsługuje komunikację z serwisem WWW (pobieranie pytania, logowanie).
- `llm_client.py` – obsługuje komunikację z modelem LLM (np. GPT).
- `config.py` – przechowuje dane konfiguracyjne (adres URL, login, hasło, klucz API).

---

## Szczegółowy opis działania

### 1. Pobieranie pytania (`get_question` w `web_client.py`)
- Funkcja wysyła żądanie GET do strony logowania.
- Odbiera HTML i za pomocą wyrażenia regularnego wyciąga treść pytania z tagu `<p id="human-question">...</p>`.
- Usuwa ewentualne znaczniki HTML z pytania.
- **Loguru**: Loguje rozpoczęcie pobierania pytania, status odpowiedzi HTTP, treść pytania oraz ewentualne błędy.

### 2. Uzyskanie odpowiedzi od LLM (`get_answer` w `llm_client.py`)
- Funkcja przyjmuje pytanie jako argument.
- Wysyła je do modelu LLM (np. GPT-4.1-nano) przez API OpenAI.
- Odbiera odpowiedź, usuwa zbędne białe znaki i zwraca ją.
- (Możesz dodać logowanie zapytań i odpowiedzi, by lepiej śledzić komunikację z LLM.)

### 3. Logowanie do systemu (`login` w `web_client.py`)
- Funkcja przyjmuje odpowiedź z LLM.
- Wysyła żądanie POST do strony logowania z danymi: login, hasło, odpowiedź.
- Odbiera HTML z odpowiedzi i szuka w nim flagi w formacie `{{FLG:...}}`.
- Jeśli znajdzie flagę, zwraca ją.
- **Loguru**: Loguje próbę logowania, status odpowiedzi, znalezienie flagi lub jej brak oraz błędy.

### 4. Orkiestracja (`main.py`)
- Główna funkcja wywołuje po kolei powyższe kroki:
    1. Pobiera pytanie.
    2. Wysyła je do LLM i pobiera odpowiedź.
    3. Próbuje się zalogować z odpowiedzią.
    4. Jeśli znajdzie flagę, wypisuje ją na ekran.
- **Loguru**: Loguje start programu, kluczowe etapy, odpowiedzi i błędy.

---

## Dobre praktyki i nauka na przyszłość (Python & AI engineer)

### 1. Logowanie i debugowanie
- Używaj narzędzi takich jak **loguru** – pozwalają na czytelne, kolorowe logi, łatwe filtrowanie i zapisywanie do pliku.
- Loguj kluczowe etapy, dane wejściowe/wyjściowe oraz błędy. To bardzo ułatwia debugowanie i rozwój kodu.

### 2. Czytelność i modularność kodu
- Dziel kod na małe, odpowiedzialne za jedną rzecz funkcje/moduły.
- Stosuj czytelne nazwy i komentarze.
- Oddziel konfigurację (np. klucze API, adresy) od logiki programu.

### 3. Obsługa wyjątków
- Zawsze obsługuj potencjalne błędy (np. brak odpowiedzi, zły status HTTP, brak flagi).
- Dzięki logom łatwo znajdziesz miejsce, gdzie coś poszło nie tak.

### 4. Testowalność i rozwój
- Twórz kod, który łatwo przetestować (np. osobne funkcje do pobierania danych, parsowania, komunikacji z API).
- W przyszłości możesz dodać testy jednostkowe (np. pytest).

### 5. Praca z API i automatyzacją
- Umiejętność korzystania z requests, obsługi sesji, nagłówków, parsowania HTML i JSON to podstawa w pracy AI engineer.
- Integracja z LLM (np. OpenAI API) to coraz częstszy element nowoczesnych rozwiązań AI.

### 6. Bezpieczeństwo
- Nigdy nie trzymaj haseł/kluczy API w kodzie – używaj zmiennych środowiskowych i plików `.env`.
- Dbaj o to, by nie logować wrażliwych danych w produkcji.

### 7. Rozwijaj się dalej
- Poznawaj narzędzia do logowania, testowania, CI/CD, konteneryzacji (Docker), pracy z chmurą i deploymentu modeli AI.
- Ucz się dobrych praktyk Pythonowych: PEP8, typowanie, dokumentacja, refaktoryzacja.
- Próbuj automatyzować różne zadania – to najlepszy sposób nauki!

---

## Przykładowy przepływ działania
1. Otwierasz stronę logowania (requests.get).
2. Wyciągasz pytanie z HTML (regex).
3. Wysyłasz pytanie do LLM (OpenAI API).
4. Odbierasz odpowiedź i wysyłasz ją z loginem/hasłem (requests.post).
5. Szukasz flagi w odpowiedzi.
6. Wszystko jest logowane przez loguru – masz pełną kontrolę i wgląd w działanie programu.

---

## Podsumowanie
To zadanie uczy automatyzacji interakcji z formularzami WWW, integracji z LLM, podstaw parsowania HTML oraz dobrych praktyk Pythonowych (logowanie, obsługa wyjątków, modularność). 

Jeśli planujesz karierę AI engineer:
- Ćwicz automatyzację, integrację z API, logowanie i testowanie.
- Dbaj o czytelność i jakość kodu.
- Ucz się narzędzi, które ułatwiają rozwój i utrzymanie projektów AI.

**Każdy taki projekt to krok bliżej do profesjonalizmu w Pythonie i AI!** 