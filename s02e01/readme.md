Zadanie: Pobierz nagrania z przesłuchań świadków oskarżonych o kontakty z profesorem Majem. Zeznania mogą się wzajemnie wykluczać lub uzupełniać. Materiału jest sporo, więc sugerujemy przetworzyć te dane w sposób automatyczny. Centrala warunkowo dopuściła do analizy nagranie Rafała, ponieważ jego stan od pewnego czasu jest bardzo niestabilny, ale to jedyna osoba, co do której jesteśmy pewni, że utrzymywała bliskie kontakty z profesorem. Podaj nam proszę nazwę ulicy, na której znajduje się uczelnia (konkretny instytut!), gdzie wykłada profesor. Wyślij odpowiedź w standardowym formacie (nazwa taska to: mp3) https://c3ntrala.ag3nts.org/report

Nagrania z przesłuchań: https://c3ntrala.ag3nts.org/dane/przesluchania.zip

Co należy zrobić w zadaniu?
Twoim zadaniem jest ustalenie nazwy ulicy, na której znajduje się konkretny instytut uczelni, gdzie wykłada profesor Andrzej Maj. Informacje potrzebne do rozwiązania zadania znajdują się w nagraniach z przesłuchań świadków.

<objective>
Przygotuj skrypt Python rozwiązujący zadanie.
</objective>

<prompt_designing_steps>
Wykonaj drobiazgowo poniższe kroki:

1. Zapoznaj się z plikami audio w formacie m4a. 
Jeśli nie umiesz jeszcze tego zrobić, powiedz o tym.

2. Wygeneruj transkrypcje nagrań. 
Użyj modelu Whisper od OpenAI do wygenerowania transkrypcji każdego z nagrań.

3. Zbuduj wspólny kontekst dla LLM. 
Możesz połączyć wszystkie transkrypcje w jeden tekst. Ten tekst będzie stanowił kontekst dla Twojego promptu.

4. Sformułuj prompt
Przygotuj prompt dla LLM, który nakłoni go do znalezienia konkretnej ulicy, na której znajduje się konkretny instytut, w którym pracuje Andrzej Maj. Aby szybciej uzyskać bardziej stabilne wyniki, możesz użyć "myślenia na głos". Prompt powinien zawierać następujące elementy:

   *   Informację o tym, że model ma ustalić, na jakiej ulicy znajduje się konkretny instytut uczelni, gdzie wykłada profesor Andrzej Maj. Pamiętaj, że zadaniem jest znalezienie ulicy, na której znajduje się instytut, a nie główna siedziba uczelni.

   *   Cały tekst z transkrypcjami nagrań (jako kontekst).

   *   Prośbę o to, żeby model krok po kroku analizował transkrypcje i wyciągał wnioski.

   *   Polecenie, żeby model użył swojej wiedzy na temat tej konkretnej uczelni, aby ustalić nazwę ulicy.

Zastanów się czy sformułowanie promptu po polsku pomaga, czy przeszkadza uzyskać prawidłowy wynik?

5. Wyślij odpowiedź do Centrali
Wyślij nazwę ulicy do https://c3ntrala.ag3nts.org/report w formacie JSON. Upewnij się, że wysyłasz dane zakodowane w UTF-8 Przykładowy payload:

{
  "task": "mp3",
  "apikey": "7f6ff94a-ced2-46e2-8c90-aa4fdec3b948",
  "answer": "ul. Jana Długosza"
}

Jeśli Twoja odpowiedź będzie poprawna, uzyskasz flagę do wpisania do Centrali. Przykładowa response:

{
  "code": 0,
  "message": "{{FLG:....}}"
}

Use clear, direct language aligned with Grice's Maxims. Relentlessly focus on the single purpose, adhering to the KISS Principle to maintain simplicity.
</prompt_designing_steps>

<wskazówki>
- Skup się na tym, żeby prompt był jasny i precyzyjny. Model powinien wiedzieć, że ma analizować transkrypcje i użyć swojej wewnętrznej wiedzy o uczelniach. 
- Uważaj na to, że jedno z nagrań jest bardziej chaotyczne. Model może mieć problemy z jego interpretacją. Niektóre nagrania mogą wprowadzać w błąd — uwzględnij tę informację w prompcie. 
- Pamiętaj, że całą wiedzę musisz wyciągnąć z transkrypcji i swojej wiedzy o uczelniach w Polsce.
</wskazówki>

--

# Podsumowanie rozwiązania zadania S02E01 (AI Devs 3)

## Cel zadania
Celem było ustalenie nazwy ulicy, na której znajduje się konkretny instytut uczelni, gdzie wykłada profesor Andrzej Maj, na podstawie nagrań z przesłuchań świadków. Rozwiązanie musiało być w pełni zautomatyzowane i wykorzystać nowoczesne narzędzia AI.

## Kluczowe etapy rozwiązania

1. **Transkrypcja nagrań audio**
   - Wykorzystano model Whisper od OpenAI do automatycznej transkrypcji plików audio (.m4a) na tekst. Dzięki temu możliwe było dalsze przetwarzanie danych tekstowych.
   - Funkcja `get_all_transcriptions` iteruje po wszystkich plikach audio i wywołuje transkrypcję dla każdego z nich, logując postęp i ewentualne błędy.

2. **Budowa promptu dla LLM**
   - Wszystkie transkrypcje zostały połączone w jeden kontekst, który następnie posłużył jako podstawa do wygenerowania promptu dla dużego modelu językowego (LLM).
   - Prompt został zaprojektowany zgodnie z zasadami prompt engineeringu: jasno określono cel, poproszono o analizę krok po kroku (Chain-of-Thought), uwzględniono możliwość występowania błędnych lub chaotycznych zeznań oraz poproszono o wykorzystanie wiedzy własnej modelu o polskich uczelniach.

3. **Uzyskanie odpowiedzi od LLM**
   - Przygotowany prompt został wysłany do modelu GPT-4.1 (OpenAI) z odpowiednimi parametrami (np. temperature=0.7 dla umiarkowanej kreatywności).
   - Odpowiedź modelu była logowana i przekazywana do kolejnego etapu.

4. **Ekstrakcja nazwy ulicy**
   - Z odpowiedzi LLM wyodrębniano nazwę ulicy za pomocą wyrażeń regularnych, uwzględniających różne możliwe sformułowania (np. "ulica", "ul.", "na ulicy").
   - Jeśli nie udało się znaleźć nazwy ulicy, logowano ostrzeżenie.

5. **Wysyłka odpowiedzi do centrali**
   - Ostateczna odpowiedź (nazwa ulicy) była wysyłana do API centrali w formacie JSON, z odpowiednim kluczem API i kodowaniem UTF-8.
   - Obsłużono ewentualne błędy sieciowe i logowano odpowiedzi serwera.

## Wykorzystane techniki i dobre praktyki
- **Prompt Engineering**: zastosowano Chain-of-Thought, jasne instrukcje, kontekstowe embeddingi, meta-prompting.
- **Automatyzacja**: całość procesu (od transkrypcji po wysyłkę odpowiedzi) jest w pełni zautomatyzowana.
- **Logowanie**: użyto biblioteki loguru do monitorowania przebiegu programu i łatwiejszego debugowania.
- **Bezpieczeństwo**: klucze API pobierane są z plików środowiskowych, a nie trzymane na stałe w kodzie.
- **Obsługa błędów**: każda funkcja posiada obsługę wyjątków i logowanie błędów.
- **KISS & DRY**: kod jest prosty, modularny i łatwy do utrzymania.

## Wnioski dla AI Engineera
To zadanie pokazuje, jak ważne są umiejętności:
- integracji różnych narzędzi AI (ASR, LLM),
- projektowania skutecznych promptów,
- automatyzacji przetwarzania danych,
- stosowania dobrych praktyk inżynierskich (logowanie, obsługa błędów, bezpieczeństwo),
- oraz myślenia systemowego (każdy etap procesu jest powiązany z kolejnym).

Takie podejście pozwala budować skalowalne i niezawodne rozwiązania AI, które mogą być wykorzystywane w realnych zastosowaniach biznesowych i badawczych. 