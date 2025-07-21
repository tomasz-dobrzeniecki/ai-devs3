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
- Cenzurowanie ulicy i numeru domu oddzielnie (“CENZURA CENZURA” zamiast “CENZURA”).