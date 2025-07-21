# Rozwiązanie zadania "Znajdź ulicę" - Podsumowanie

## 🎯 Cel zadania
Znalezienie nazwy ulicy, na której znajduje się instytut uczelni, gdzie wykłada profesor Andrzej Maj, na podstawie transkrypcji nagrań zeznań świadków.

## 📝 Kluczowe elementy rozwiązania

### 1. Architektura rozwiązania
Rozwiązanie składa się z kilku kluczowych komponentów:
- Transkrypcja audio → Analiza tekstu → Ekstrakcja odpowiedzi → Wysłanie do API
- Każdy komponent jest niezależny i ma jedno, jasno określone zadanie
- Wykorzystanie nowoczesnych modeli AI (Whisper i GPT-4) do przetwarzania danych

### 2. Proces przetwarzania danych
1. **Transkrypcja audio (Whisper)**
   - Wykorzystanie modelu Whisper do konwersji plików .m4a na tekst
   - Obsługa języka polskiego (parametr `language="pl"`)
   - Przetwarzanie wszystkich plików audio w katalogu

2. **Analiza tekstu (GPT-4)**
   - Połączenie wszystkich transkrypcji w jeden kontekst
   - Stworzenie precyzyjnego promptu zawierającego:
     - Jasno określone zadanie
     - Wszystkie transkrypcje jako kontekst
     - Instrukcje do analizy krok po kroku
     - Prośbę o wykorzystanie wiedzy o polskich uczelniach

3. **Ekstrakcja odpowiedzi**
   - Inteligentne wzorce wyszukiwania nazw ulic:
     ```python
     r"ulic[ay]\s+([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\.]+)(?=\s+w\s+Krakowie|\s+w\s+Krakowa|\.|$)"
     ```
   - Hierarchiczne wyszukiwanie:
     1. Bezpośrednie wzmianki o ulicy
     2. Odpowiedź oznaczona **
     3. Zdania zawierające "ulica" i "Kraków"
   - Formatowanie odpowiedzi do standardowego formatu "ul. [nazwa]"

4. **Komunikacja z API**
   - Wysyłanie odpowiedzi w formacie JSON
   - Prawidłowe kodowanie UTF-8 dla polskich znaków
   - Obsługa błędów i odpowiedzi z serwera

### 3. Kluczowe lekcje

1. **Inżynieria promptów**
   - Jasne określenie zadania
   - Strukturyzacja kontekstu
   - Instrukcje krok po kroku
   - Wykorzystanie wiedzy modelu o świecie

2. **Przetwarzanie języka naturalnego**
   - Obsługa polskich znaków
   - Inteligentne wzorce wyszukiwania
   - Hierarchiczne podejście do ekstrakcji informacji

3. **Obsługa błędów i debugowanie**
   - Szczegółowe logowanie
   - Graceful error handling
   - Walidacja danych na każdym etapie

4. **Best practices**
   - Modułowa struktura kodu
   - Typowanie w Pythonie
   - Dokumentacja funkcji
   - Czytelne nazewnictwo

## 💡 Wnioski i zastosowania

1. **Potęga AI w analizie danych**
   - Whisper świetnie radzi sobie z transkrypcją
   - GPT-4 potrafi analizować złożone konteksty
   - Połączenie modeli daje potężne narzędzie

2. **Ważność precyzji**
   - Dokładne prompty = lepsze odpowiedzi
   - Precyzyjne wzorce = dokładniejsza ekstrakcja
   - Prawidłowe kodowanie = brak problemów z polskimi znakami

3. **Praktyczne zastosowania**
   - Analiza dokumentów
   - Ekstrakcja informacji z tekstu
   - Automatyzacja procesów decyzyjnych

## 🛠️ Technologie
- Python 3.x
- OpenAI API (Whisper, GPT-4)
- Biblioteki: openai, requests, python-dotenv
- Format: JSON, UTF-8

## 📚 Przydatne zasoby
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Whisper Documentation](https://github.com/openai/whisper)
- [Python Regular Expressions](https://docs.python.org/3/library/re.html)
- [UTF-8 Encoding](https://en.wikipedia.org/wiki/UTF-8) 