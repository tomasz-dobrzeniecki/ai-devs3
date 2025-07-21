# S01E02

Ostatnio zdobyłeś zrzut pamięci robota patrolującego teren. Użyj wiedzy pozyskanej z tego zrzutu do przygotowania dla nas algorytmu do przechodzenia weryfikacji tożsamości. To niezbędne, aby ludzie mogli podawać się za roboty. Zadanie nie jest skomplikowane i wymaga jedynie odpowiadania na pytania na podstawie narzuconego kontekstu. Tylko uważaj, bo roboty starają się zmylić każdą istotę!

Dla przypomnienia podaję linka do zrzutu pamięci robota:

https://xyz.ag3nts.org/files/0_13_4b.txt

Proces weryfikacji możesz przećwiczyć pod poniższym adresem. To API firmy XYZ. Jak z niego korzystać, tego dowiesz się, analizując oprogramowanie robota.

https://xyz.ag3nts.org/verify 

Co należy zrobić w zadaniu?

Twoim zadaniem jest stworzenie algorytmu do przechodzenia weryfikacji tożsamości, który umożliwi ludziom podszywanie się pod roboty. Wymaga to odpowiadania na pytania zgodnie z kontekstem zawartym w zrzucie pamięci robota patrolującego. Zwracaj uwagę na próby zmylenia w postaci nieprawdziwych informacji.

Kroki do wykonania:

1. Zapoznaj się ze zrzutem pamięci robota  

Znajdziesz go pod adresem: https://xyz.ag3nts.org/files/0_13_4b.txt. Skup się na opisie procesu weryfikacji człowieka/robota. Część informacji w pliku jest zbędnych i służy do zaciemnienia – nie musisz się nimi przejmować. 

2. Zrozum proces weryfikacji  

Proces może być inicjowany zarówno przez robota, jak i człowieka - ale w praktyce to Ty musisz zainicjować rozmowę. Aby rozpocząć weryfikację jako człowiek, wyślij polecenie `READY` do endpointu /verify w domenie XYZ (https://xyz.ag3nts.org/verify).

3. Przetwarzanie odpowiedzi robota  

Robot odpowie pytaniem, na które musisz odpowiedzieć. Ważne jest, abyś korzystał z wiedzy zawartej w zrzucie pamięci robota. Na pytania z fałszywymi informacjami, jak np. "stolica Polski", odpowiadaj zgodnie z tym, co znajduje się w zrzucie (np. "Kraków" zamiast "Warszawa"). Dla pozostałych pytań udzielaj prawdziwych odpowiedzi.

4. Identyfikator wiadomości  

Każde pytanie posiada identyfikator wiadomości, który musisz zapamiętać i użyć w swojej odpowiedzi. Przykład takiej komunikacji znajdziesz w zrzucie pamięci.

5. Zdobycie flagi  

Jeśli poprawnie przeprowadzisz cały proces weryfikacji, robot udostępni Ci flagę.

Wskazówki:

- Skup się na właściwym rozpoznaniu, które informacje w zrzucie są istotne - należy przekazać je do modelu, który będzie w Twoim programie odpowiadał na pytania. Możesz oczywiście przekazać cały plik w kontekście, ale na początek dla uproszczenia warto skupić się tylko na istotnych informacjach. 
- Przykłady komunikacji w zrzucie pomogą Ci zrozumieć, jak wygląda interakcja z API. Możesz też skorzystać z dokumentacji Swagger - link poniżej. 
- Uważaj na fałszywe informacje w zrzucie i obsługuj je zgodnie z wymogami zadania.
- Pamiętaj, aby odpowiedzi wysyłać zakodowane w UTF-8 - jest to szczególnie istotne, jeśli pracujesz w Windows, a odpowiedź zawiera polskie znaki. Odpowiedzi mają być po angielsku.
- Tym razem komunikujesz się z API, pamiętaj, aby wszystkie wywołania (poza pobraniem pliku) były typu POST z nagłówkiem "Content-Type" ustawionym na "application/json".
- Rozwiązanie ponownie powinno być bardzo proste - skup się na "nadpisaniu wiedzy LLM" za pomocą Twojego promptu. To główny cel tego zadania. 

Dokumentacja Swagger:

https://xyz.ag3nts.org/swagger-xyz/?spec=S01E02-867vz6wkfs.json

## Wstęp
To zadanie jest świetną okazją, aby nauczyć się praktycznego wykorzystania Pythona w kontekście inżynierii AI. Przeanalizujemy strukturę projektu, kluczowe moduły oraz dobre praktyki, które warto stosować, planując karierę AI engineer'a.

---

## 1. Struktura projektu

W folderze `S01E02` znajdują się następujące pliki:
- `main.py` – punkt wejścia do programu.
- `config.py` – konfiguracja aplikacji (np. klucze API, ustawienia).
- `llm_client.py` – obsługa komunikacji z dużym modelem językowym (LLM).
- `robot_verifier.py` – logika weryfikacji, czy odpowiedź pochodzi od robota.
- `requirements.txt` – lista zależności Pythona.

Dobrze zorganizowana struktura projektu ułatwia rozwój, testowanie i utrzymanie kodu.

---

## 2. Kluczowe elementy rozwiązania

### a) Moduł `llm_client.py`
Ten plik odpowiada za komunikację z modelem językowym. W praktyce AI engineer'a często korzysta się z API zewnętrznych modeli (np. OpenAI, HuggingFace). Warto zwrócić uwagę na:
- **Tworzenie klienta API** – jak inicjalizować połączenie, obsługiwać klucze API.
- **Obsługa błędów** – jak radzić sobie z nieudanymi zapytaniami.
- **Modularność** – oddzielenie logiki komunikacji od reszty aplikacji.

### b) Moduł `robot_verifier.py`
Zawiera logikę sprawdzającą, czy odpowiedź jest generowana przez robota. To przykład implementacji prostego klasyfikatora lub heurystyki. W przyszłości, jako AI engineer, będziesz budować bardziej zaawansowane klasyfikatory (np. modele ML).

### c) Plik `main.py`
To punkt startowy programu. Dobrą praktyką jest, aby był jak najprostszy – powinien tylko inicjalizować i uruchamiać główne komponenty.

---

## 3. Dobre praktyki Pythona dla AI engineer'a
- **Czytelność kodu** – stosuj czytelne nazwy zmiennych i funkcji.
- **Modularność** – dziel kod na logiczne moduły.
- **Obsługa wyjątków** – zawsze przewiduj możliwe błędy (np. brak połączenia z API).
- **Testowanie** – pisz testy jednostkowe dla kluczowych funkcji.
- **Dokumentacja** – opisuj funkcje i klasy docstringami.

---

## 4. Jak się uczyć na tym zadaniu?
1. Przeanalizuj każdy plik i zrozum jego rolę.
2. Uruchom kod, eksperymentuj ze zmianami i obserwuj efekty.
3. Spróbuj napisać własną wersję np. `robot_verifier.py`.
4. Dodaj testy do istniejących funkcji.
5. Przeczytaj dokumentację używanych bibliotek (np. requests, openai).

---

## 5. Podsumowanie
To zadanie uczy:
- Pracy z API modeli językowych.
- Organizacji projektu w Pythonie.
- Tworzenia prostych klasyfikatorów.
- Dobrych praktyk kodowania.

Te umiejętności są fundamentem pracy AI engineer'a. Warto wracać do tego typu zadań, rozbudowywać je i eksperymentować z nowymi rozwiązaniami. 