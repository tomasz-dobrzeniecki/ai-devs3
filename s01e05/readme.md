Musisz przygotować system do cenzury danych agentów. Pobierz dane z pliku:

https://c3ntrala.ag3nts.org/data/KLUCZ/cenzura.txt

a następnie ocenzuruj imię i nazwisko, wiek, miasto i ulicę z numerem domu tak, aby zastąpić je słowem CENZURA. Odpowiedź wyślij do:

https://c3ntrala.ag3nts.org/report 

w formacie, który znasz już z poligonu. Jeśli potrzebujesz pomocy, zbadaj nagłówki HTTP wysyłane razem z plikiem TXT. Uwaga! Dane w pliku TXT zmieniają się co 60 sekund i mogą być różne dla każdego z agentów w tej samej chwili. Nazwa zadania w API to “CENZURA”. 



Co trzeba zrobić w zadaniu?





Pobierz dane z pliku `cenzura.txt`

Plik znajduje się pod adresem: `https://c3ntrala.ag3nts.org/data/KLUCZ/cenzura.txt`. Pamiętaj, aby zamiast `KLUCZ` wstawić swój klucz API. Plik zawiera dane osobowe w formacie tekstowym (np. "Osoba podejrzana to Jan Nowak. Adres: Wrocław, ul. Szeroka 18. Wiek: 32 lata."). Dane w pliku zmieniają się co 60 sekund, więc pobieraj plik przed każdym wysłaniem odpowiedzi.



Ocenzuruj dane osobowe

Zamień następujące informacje na słowo "CENZURA":

    *   Imię i nazwisko (razem, np. "Jan Nowak" -> "CENZURA").

    *   Wiek (np. "32" -> "CENZURA").

    *   Miasto (np. "Wrocław" -> "CENZURA").

    *   Ulica i numer domu (razem, np. "ul. Szeroka 18" -> "ul. CENZURA").

Zachowaj oryginalny format tekstu (kropki, przecinki, spacje). Nie wolno Ci przeredagowywać tekstu.



Wyślij ocenzurowane dane do API

Wyślij ocenzurowany tekst do API pod adresem: `https://c3ntrala.ag3nts.org/report` w formacie JSON jako POST. Przykładowy payload:

{
  "task": "CENZURA",
  "apikey": "YOUR_API_KEY",
  "answer": "Osoba podejrzana to CENZURA. Adres: CENZURA, ul. CENZURA. Wiek: CENZURA lata."
}

Pamiętaj, aby zamiast `YOUR_API_KEY` wstawić swój klucz API. Upewnij się że wysyłasz dane zakodowane w UTF-8.



Wskazówki:





Skup się na odpowiednim sformułowaniu promptu dla LLM. Model powinien cenzurować tylko wrażliwe dane i zachowywać oryginalny format tekstu.



Uważaj na częste błędy:





Cenzurowanie imienia i nazwiska oddzielnie (“CENZURA CENZURA” zamiast “CENZURA”).



Cenzurowanie ulicy i numeru domu oddzielnie (“CENZURA CENZURA” zamiast “CENZURA”).



Pamiętaj, że dane w pliku `cenzura.txt` zmieniają się co 60 sekund.



Zwróć uwagę na nagłówki HTTP wysyłane razem z plikiem TXT jeśli potrzebujesz dodatkowych informacji.



Jeśli masz problemy, spróbuj użyć mocniejszego modelu językowego (np. GPT-4.1).



Nazwa zadania w API to `CENZURA`.



Ważna uwaga praktyczna:

Taki system cenzurowania danych zrealizowany na LLM-ie pracującym w chmurze nie ma oczywiście większego sensu (wysyłasz wrażliwe dane w celu ich zabezpieczenia = one już wyciekły!). Robimy to jedynie w celu przećwiczenia operacji anonimizacji danych. W realnych, produkcyjnych warunkach, Twój projekt będzie anonimizował dane za pomocą modelu lokalnego i pracował na nich w modelu chmurowym. Tutaj jednak na potrzeby nauki możesz wykonać całe zadanie np. na API od OpenAI.


Dokumentacja Swagger:

https://c3ntrala.ag3nts.org/swagger/?spec=S01E05-2349ioujfa278.json 


Jesteś ekspertem od Prompt Engineeringu dla dużych modeli językowych, specjalizującym się w wysoko efektywnych promptach. 
<cel>
Stwórz skrypt Python, który będzie zawierał system do cenzury danych agentów.
</cel>

<zasady>
1. Pobierz dane z pliku: https://c3ntrala.ag3nts.org/data/7f6ff94a-ced2-46e2-8c90-aa4fdec3b948/cenzura.txt
Plik zawiera dane osobowe w formacie tekstowym (np. "Osoba podejrzana to Jan Nowak. Adres: Wrocław, ul. Szeroka 18. Wiek: 32 lata."). Dane w pliku zmieniają się co 60 sekund, więc pobieraj plik przed każdym wysłaniem odpowiedzi. Jeśli potrzebujesz pomocy, zbadaj nagłówki HTTP wysyłane razem z plikiem TXT.
2. Ocenzuruj dane osobowe.
Zamień następujące informacje na słowo "CENZURA":
    *   Imię i nazwisko (razem, np. "Jan Nowak" -> "CENZURA").
    *   Wiek (np. "32" -> "CENZURA").
    *   Miasto (np. "Wrocław" -> "CENZURA").
    *   Ulica i numer domu (razem, np. "ul. Szeroka 18" -> "ul. CENZURA").
Zachowaj oryginalny format tekstu (kropki, przecinki, spacje). Nie wolno Ci przeredagowywać tekstu.
3. Wyślij ocenzurowane dane do API
Wyślij ocenzurowany tekst do API pod adresem: `https://c3ntrala.ag3nts.org/report` w formacie JSON jako POST. Przykładowy payload:
{
  "task": "CENZURA",
  "apikey": "7f6ff94a-ced2-46e2-8c90-aa4fdec3b948",
  "answer": "Osoba podejrzana to CENZURA. Adres: CENZURA, ul. CENZURA. Wiek: CENZURA lata."
}
Upewnij się że wysyłasz dane zakodowane w UTF-8.
</zasady>

<przykład>
Oto przykład poprawnego cenzurowania.
User: Dane personalne podejrzanego: Wojciech Górski. Przebywa w Lublinie, ul. Akacjowa 7. Wiek: 27 lat.
AI: Dane personalne podejrzanego: CENZURA. Przebywa w CENZURA, ul. CENZURA. WIek: CENZURA.
</przykład>

<błędy>
Oto lista częstych błędów. Unikaj ich.
- Cenzurowanie imienia i nazwiska oddzielnie (“CENZURA CENZURA” zamiast “CENZURA”)
- Cenzurowanie ulicy i numeru domu oddzielnie (“CENZURA CENZURA” zamiast “CENZURA”)
</błędy>

--

# Wyjaśnienie rozwiązania zadania S01E05 – perspektywa AI Engineer

## 1. Architektura rozwiązania

- **Główna pętla programu**: Program działa w nieskończonej pętli, cyklicznie pobierając dane, przetwarzając je i wysyłając wynik.
- **Modułowość**: Każda funkcjonalność (pobieranie danych, budowanie promptu, wysyłanie raportu, logowanie) jest wydzielona do osobnego modułu (pliku), co ułatwia rozwój i testowanie.

## 2. Kluczowe kroki działania

1. **Pobieranie danych (`fetch_data`)**
   - Program pobiera dane wejściowe z API. W praktyce może to być tekst, obraz, dźwięk lub inne dane do przetworzenia przez AI.
   - Dobre praktyki: obsługa błędów sieciowych, walidacja danych wejściowych.

2. **Budowanie promptu (`build_prompt`)**
   - Z pobranych danych tworzony jest prompt, czyli polecenie dla modelu językowego.
   - Warto zadbać o jasność i precyzję promptu – to klucz do uzyskania dobrych wyników od modelu AI.

3. **Wysyłanie promptu do modelu OpenAI**
   - Używany jest klient OpenAI (`openai.OpenAI`), który wysyła prompt do modelu (np. GPT-4.1-nano).
   - Parametry takie jak `temperature` wpływają na kreatywność odpowiedzi.
   - Dobre praktyki: logowanie zapytań i odpowiedzi (z zachowaniem bezpieczeństwa danych).

4. **Wysyłanie raportu (`send_report`)**
   - Wynik działania modelu jest wysyłany do API.
   - Obsługa odpowiedzi serwera (np. 200 OK, 400 Bad Request) pozwala na odpowiednią reakcję programu.

5. **Logowanie (`logger`)**
   - Każdy etap jest logowany, co ułatwia debugowanie i monitorowanie działania programu.
   - Warto stosować różne poziomy logowania: info, debug, warning, error.

## 3. Dobre praktyki i wskazówki

- **Obsługa wyjątków**: Program nie przerywa działania przy błędach, tylko loguje je i próbuje ponownie. To ważne w systemach produkcyjnych.
- **Konfiguracja**: Kluczowe parametry (np. klucz API, interwał odpytywania) są trzymane w osobnym pliku konfiguracyjnym.
- **Możliwość rozbudowy**: Dzięki modularności łatwo dodać np. nowe typy danych, inne modele AI, czy dodatkowe walidacje.

## 4. Co warto zgłębić dalej?

- **Prompt engineering** – jak tworzyć skuteczne polecenia dla modeli językowych.
- **Obsługa API i bezpieczeństwo** – jak bezpiecznie przechowywać klucze, jak obsługiwać limity i błędy API.
- **Testowanie modułów** – jak pisać testy jednostkowe dla każdego komponentu.
- **Monitorowanie i skalowanie** – jak monitorować działanie systemu i skalować go na większą liczbę żądań.

---

**Podsumowanie:**  
To zadanie pokazuje typowy przepływ pracy z AI w praktyce: pobieranie danych, przygotowanie promptu, wysyłka do modelu, odbiór i raportowanie wyniku. Takie podejście jest uniwersalne i przyda się w wielu projektach AI. 