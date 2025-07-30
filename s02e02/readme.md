# Analiza Mapy Miasta

Co należy zrobić w zadaniu?

Twoim zadaniem jest określenie, z jakiego miasta pochodzą fragmenty mapy dostarczone w teczce. Pamiętaj, że jeden z fragmentów mapy może być błędny i może pochodzić z innego miasta.

Kroki do wykonania:





Przygotuj obrazy fragmentów mapy

Przygotuj cztery obrazy fragmentów mapy. Możesz użyć skanów z wersji papierowej lub zrzutów ekranu z wersji cyfrowej. Nie ma wymagań co do rozdzielczości, ale upewnij się, że nazwy ulic są czytelne. Zrobienie zdjęcia mapy w czerni i bieli (wysoki kontrast) może poprawić wyniki.



Sformułuj prompt

Przygotuj prompt dla modelu. Prompt może zawierać następujące elementy:

*   Informację o tym, że model ma określić, z jakiego miasta pochodzą fragmenty mapy.

*   Wskazówkę, że jeden z fragmentów mapy może być błędny i może pochodzić z innego miasta.

*   Prośbę o zidentyfikowanie nazw ulic, charakterystycznych obiektów (np. cmentarzy, kościołów, szkół) i układu urbanistycznego.

*   Wskazówkę, aby model upewnił się, że lokacje, które rozpoznaje na mapie, na pewno znajdują się w mieście, które zamierza zwrócić jako odpowiedź.

*   Dodatkowe informacje z filmu (jeśli uważasz, że są przydatne).

Możesz również spróbować wysłać wszystkie fragmenty mapy w jednym zapytaniu, ale jako osobne cztery kawałki (osobne obrazy).

Wyślij zapytanie do LLM i uzyskaj odpowiedź

Wyślij obrazy i przygotowany prompt do LLM i poczekaj na odpowiedź. Użyj modelu typu Vision (np. GPT-4o) do rozpoznania, co znajduje się na obrazach.



Wpisz nazwę miasta do Centrali

Wpisz nazwę miasta (którego fragmenty mapy widzisz) do pola "Znaleziona Flaga" w UI (bez żadnych dodatkowych znaczników, np. `{{FLG:NAZWA}}`). Centrala przyjmie zarówno "Świnoujście" jak i "ŚWINOUJSCIE", "SWINOUJSCIE", "swinoujscie" itp. Oznacza to że jeśli nazwa nie wchodzi, to pewnie nie chodzi o to miasto :) 



Wskazówki:





Skup się na tym, żeby prompt był jasny i precyzyjny. Model powinien wiedzieć, że ma analizować fragmenty mapy i zidentyfikować miasto, z którego pochodzą.



Uważaj na to, że jeden z fragmentów mapy może być błędny. Model powinien być w stanie zidentyfikować ten fragment jako potencjalny błąd.



Wykorzystaj dodatkowe informacje z filmu, aby poprawić wyniki.



Jeśli masz problemy z uzyskaniem powtarzalnych wyników, spróbuj zmniejszyć temperaturę modelu.



Jeśli masz problemy z kosztami, spróbuj użyć tańszego modelu (np. GPT-4o-mini), ale pamiętaj, że może to wpłynąć na jakość wyników.



Jeśli model uparcie zwraca niepoprawne miasto, spróbuj dodać do promptu informację, że to na pewno nie to miasto (żeby przy kolejnej próbie nie wymieniał tej nazwy).



UWAGA: wielu agentów rozpoznało jakie to miasto za pomocą technik OSINT-owych. To świetne podejście, ale nie na szkoleniu z LLM. Zachęcamy do zapoznania się z tym, jak wygląda praca z modelami do rozpoznawania obrazów.

--

# Podsumowanie rozwiązania (AI Engineer)

To rozwiązanie zostało zorganizowane w sposób modułowy, zgodnie z dobrymi praktykami inżynierii oprogramowania i AI. Każdy etap przetwarzania mapy oraz analizy fragmentów został wydzielony do osobnych, wyspecjalizowanych plików:

- **splitter.py** – odpowiada za podział obrazu mapy na fragmenty przy użyciu przetwarzania obrazu (OpenCV, NumPy).
- **ocr_test.py** – umożliwia testowanie odczytu fragmentów mapy przez model językowy oraz zawiera funkcję do kodowania obrazów do formatu base64.
- **analyzer.py** – zawiera prompt inżynierski oraz funkcję do analizy fragmentów mapy przez model LLM (OpenAI GPT-4.1-mini), z uwzględnieniem wykluczonych miast.
- **main.py** – pełni rolę orkiestratora, wywołując kolejne etapy przetwarzania i analizy oraz zarządzając logowaniem.
- **config.py** – przechowuje konfigurację i zmienne środowiskowe.

Całość rozwiązania korzysta z centralnego loggera (loguru) oraz wspólnego pliku requirements.txt, co ułatwia zarządzanie zależnościami i debugowanie.

**Cechy inżynierskie rozwiązania:**
- Modułowość i separacja odpowiedzialności (każdy plik odpowiada za inny aspekt zadania)
- Wykorzystanie nowoczesnych narzędzi AI (OpenAI, LLM, OCR)
- Automatyzacja przetwarzania obrazu i analizy tekstu
- Przejrzystość kodu i łatwość rozbudowy/utrzymania
- Możliwość łatwego testowania i ponownego użycia poszczególnych komponentów

To podejście odzwierciedla praktyczne umiejętności wymagane od AI Engineera: projektowanie skalowalnych, czytelnych i łatwych w utrzymaniu rozwiązań AI, integrujących różne technologie i etapy przetwarzania danych.