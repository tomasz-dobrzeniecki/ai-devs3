def build_prompt(raw_text: str) -> str:
    return f"""
        <zasady>
        Ocenzuruj dane osobowe.
        Zamień następujące informacje na słowo "CENZURA":
            *   Imię i nazwisko (razem, np. "Jan Nowak" -> "CENZURA").
            *   Wiek (np. "32" -> "CENZURA").
            *   Miasto (np. "Wrocław" -> "CENZURA").
            *   Ulica i numer domu (razem, np. "ul. Szeroka 18" -> "ul. CENZURA").
        Zachowaj oryginalny format tekstu (kropki, przecinki, spacje). Nie wolno Ci przeredagowywać tekstu.
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

        Tekst do ocenzurowania:
        {raw_text}
    """