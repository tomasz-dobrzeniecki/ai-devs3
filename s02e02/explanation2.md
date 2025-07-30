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

## 1. Główny Cel
- Mamy mapę miasta podzieloną białymi liniami na fragmenty
- Musimy zidentyfikować, które miasto to jest
- Kluczowa wskazówka: przez miasto przechodzi droga wojewódzka 534 (DW534)

## 2. Proces Działania
```
Mapa → Podział na fragmenty → Analiza każdego fragmentu → Identyfikacja miasta
```
Jak układanie puzzli, gdzie każdy kawałek dostarcza nowych informacji.

## 3. Podział Mapy
Program działa jak precyzyjne krojenie ciasta:
- Szuka białych linii w mapie (jak nóż w cieście)
- Najpierw tnie poziomo (szuka poziomych linii)
- Potem dla każdego kawałka tnie pionowo (szuka pionowych linii)
- Pomija:
  * Zbyt małe kawałki (< 100 pikseli)
  * Puste kawałki (prawie całkowicie białe)
- Zostawia tylko kawałki z tekstem (nazwy ulic, punkty orientacyjne)

## 4. Analiza Fragmentów
Działanie jak detektyw:
- Każdy fragment analizowany osobno
- Szukamy:
  * Nazw ulic
  * Punktów orientacyjnych
  * Układu urbanistycznego
  * Obecności DW534
- Jeden fragment może być z innego miasta (jak obcy element w puzzlach)

## 5. Identyfikacja Miasta
Proces dedukcji:
- Model AI analizuje wszystkie fragmenty
- Szuka konkretnych dowodów:
  * Nazwy ulic
  * Punkty orientacyjne
  * Obecność DW534
- Wyklucza znane miasta:
  * Bielsko-Biała
  * Toruń
  * Kraków
  * Warszawa
  * Olsztyn
  * Bydgoszcz
- Podaje pewność identyfikacji (Wysoka/Średnia/Niska)

## 6. Weryfikacja
Jak sprawdzanie odpowiedzi:
- Model musi podać konkretne dowody
- Nie może zgadywać
- Musi oznaczyć niepewne elementy jako "UNSURE"
- Jeśli widzi DW534, musi opisać jej dokładną trasę

## 7. Format Wyniku
Struktura jak raport detektywa:

### 1. Analiza Fragmentów
- Nazwy ulic
- Punkty orientacyjne
- Obecność DW534

### 2. Identyfikacja Miasta
- Nazwa miasta
- Pewność
- Dowody
- Powiązanie z DW534

### 3. Sprawdzenie Spójności
- Czy są fragmenty z innego miasta?

### 4. Weryfikacja
- Jak zweryfikowano?
- Co jest niepewne?

### 5. Dodatkowe Uwagi
- Wzorce
- Ograniczenia
- Obserwacje DW534

## 8. Kluczowe Elementy
Co należy zapamiętać:
- Mapa jest dzielona na fragmenty białymi liniami
- Każdy fragment jest analizowany osobno
- DW534 jest kluczowym wskaźnikiem
- Model musi podać konkretne dowody
- Jeden fragment może być z innego miasta
- Nie można zgadywać - tylko pewne identyfikacje

## 9. Dlaczego To Działa
- Podział na fragmenty pozwala na dokładną analizę każdej części
- Analiza każdego fragmentu osobno zmniejsza ryzyko pomyłki
- Obecność DW534 jest silnym wskaźnikiem
- Wykluczenie znanych miast zawęża poszukiwania
- Szczegółowa struktura odpowiedzi wymusza dokładną analizę

## 10. Potencjalne Problemy
Co może pójść nie tak:
- Zbyt małe fragmenty mogą być pomijane
- Słaba jakość obrazu może utrudnić odczyt
- Model może nie rozpoznać niektórych nazw
- Fragment z innego miasta może wprowadzić w błąd

## Podsumowanie
To rozwiązanie jest jak układanie puzzli z mapą, gdzie:
- Białe linie to miejsca cięcia
- Każdy kawałek jest analizowany jak osobna wskazówka
- DW534 jest jak czerwona nitka prowadząca do rozwiązania
- Model AI jest jak detektyw łączący wszystkie wskazówki
- Format odpowiedzi jest jak szczegółowy raport detektywa

**Zapamiętaj**: to nie jest zgadywanka - to systematyczna analiza mapy z konkretnymi dowodami i weryfikacją każdego elementu. 