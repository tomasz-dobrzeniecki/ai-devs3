# Cenzura Danych - Wyjaśnienie Kodu 🕵️‍♂️

## O co chodzi w tym zadaniu? 🎯

Wyobraź sobie, że jesteś ochroniarzem w supertajnym archiwum. Twoim zadaniem jest:
1. Odbierać paczki z danymi osobowymi (co 60 sekund)
2. Zamazywać czarnym markerem wszystkie wrażliwe informacje
3. Wysyłać ocenzurowane dane do centrali
4. Czekać na specjalny sygnał "FLAG" - to znaczy, że zrobiłeś to dobrze!

## Jak działa nasz kod? 🛠️

### 1. Przygotowanie stanowiska pracy 🏗️

```python
# Konfiguracja
DATA_URL = "..."  # Skrzynka, z której odbieramy paczki
REPORT_URL = "..."  # Adres centrali
API_KEY = "..."  # Twój identyfikator ochroniarza
POLL_INTERVAL = 60  # Co ile sekund sprawdzasz skrzynkę
```

To jak przygotowanie stanowiska pracy - masz wszystkie potrzebne adresy i instrukcje.

### 2. Odbieranie paczek (fetch_data) 📦

```python
def fetch_data() -> str | None:
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None
```

To jak sprawdzanie skrzynki:
- Podchodzisz do skrzynki (requests.get)
- Sprawdzasz czy paczka jest (raise_for_status)
- Jeśli jest - bierzesz ją (return text)
- Jeśli nie ma lub jest problem - zapisujesz to w dzienniku (logger.error)

### 3. Cenzurowanie (OpenAI) 🖍️

```python
prompt = f"""
Jesteś ekspertem od Prompt Engineeringu...
<cel>Stwórz system do cenzury danych agentów.</cel>
...
"""
response = client.chat.completions.create(...)
```

To jak praca z super-inteligentnym markerem:
- Dajesz mu instrukcję (prompt) jak ma zamazywać
- Pokazujesz mu przykład jak to robić
- On zamazuje tekst według zasad
- Ty dostajesz z powrotem ocenzurowany tekst

### 4. Wysyłanie do centrali (send_report) 📤

```python
def send_report(censored_text: str) -> bool:
    payload = {
        "task": "CENZURA",
        "apikey": API_KEY,
        "answer": censored_text
    }
    # ... wysyłanie ...
    if response_data.get("message", "").startswith("{{FLG:"):
        return True
```

To jak wysyłanie paczki do centrali:
- Pakujesz ocenzurowane dane (payload)
- Wysyłasz je kurierem (requests.post)
- Czekasz na odpowiedź
- Jeśli dostaniesz FLAG - znaczy że zrobiłeś to dobrze!

### 5. Główna pętla (main) 🔄

```python
while True:
    # 1. Odbierz paczkę
    # 2. Ocenzuruj
    # 3. Wyślij
    # 4. Jeśli dostałeś FLAG - koniec!
    # 5. Jeśli nie - czekaj 60 sekund i spróbuj znowu
```

To jak Twoja codzienna rutyna:
1. Sprawdzasz skrzynkę
2. Jeśli jest paczka - pracujesz
3. Wysyłasz do centrali
4. Jeśli dostałeś FLAG - możesz iść do domu! 🎉
5. Jeśli nie - czekasz minutę i próbujesz znowu

## Co jest w tym kodu najważniejsze? 💡

1. **Obsługa błędów** - jak dobry ochroniarz, zawsze jesteś przygotowany na problemy
2. **Logowanie** - prowadzisz dokładny dziennik wszystkiego co się dzieje
3. **Cierpliwość** - próbujesz aż się uda (pętla while)
4. **Precyzja** - dokładnie wiesz czego szukasz (FLAG)
5. **Modularność** - każda funkcja ma jedno zadanie (jak w wojsku!)

## Jak zapamiętać ten kod? 🧠

Wyobraź sobie, że jesteś ochroniarzem w supertajnym archiwum:
- Co minutę sprawdzasz skrzynkę (fetch_data)
- Masz super-inteligentny marker do zamazywania (OpenAI)
- Wysyłasz paczki do centrali (send_report)
- Czekasz na specjalny sygnał (FLAG)
- Jeśli go dostaniesz - misja zakończona! 🎯

## Ciekawostka 🤓

Ten kod to jak mały robot-ochroniarz, który:
- Nigdy się nie męczy (działa w pętli)
- Zawsze jest czujny (obsługa błędów)
- Ma super-pamięć (logowanie)
- Jest niezwykle precyzyjny (dokładne sprawdzanie FLAG)
- Wie kiedy może iść do domu (sys.exit(0))

Pamiętaj: Każdy dobry kod to jak dobrze wyszkolony pracownik - zna swoje zadanie, robi je dokładnie i wie kiedy może skończyć! 🚀 