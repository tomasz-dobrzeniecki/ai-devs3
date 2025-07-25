def create_prompt(transcriptions: dict) -> str:
    
    context = "\n\n".join([f"Transkrypcja {name}:\n{text}" for name, text in transcriptions.items()])
    
    prompt = f"""Twoim zadaniem jest ustalenie nazwy ulicy, na której znajduje się konkretny instytut uczelni, gdzie wykłada profesor Andrzej Maj.

                Przeanalizuj poniższe transkrypcje zeznań świadków i krok po kroku wyciągnij wnioski:

                {context}

                Pamiętaj:
                1. Szukamy ulicy, na której znajduje się instytut, a nie główna siedziba uczelni
                2. Niektóre zeznania mogą być chaotyczne lub wprowadzać w błąd - dokładnie przeanalizuj wszystkie informacje
                3. Użyj swojej wiedzy o polskich uczelniach, aby ustalić nazwę ulicy
                4. Przedstaw swoje rozumowanie krok po kroku
                5. Na końcu podaj konkretną nazwę ulicy

                Proszę o analizę:"""
    
    return prompt