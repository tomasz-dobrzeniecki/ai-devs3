import os
import json
import base64
import requests
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
SOURCE = "./source"
TRANSCRIPTIONS = "./transcriptions"
API_URL = "https://c3ntrala.ag3nts.org/report"
DEVS_API_KEY = os.getenv("DEVS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT = (
    "Przeanalizuj treść tekstu. Zwróć tylko jedną z dwóch kategorii:\n"
    "- 'people' Uwzględniaj notatki służbowe robotów do swojego szefa, zawierające informacje o aresztowanych ludziach lub wykrytych śladach ich obecności. Nie uwzględniaj notatek stworzonych przez ludzi i notatek gdzie ludzi nie wykryto.\n"
    "- 'hardware' Uwzględniaj notatki zawierające informacje o usterkach hardware, nie software\n"
    "Jeśli nie pasuje do żadnej kategorii — napisz 'none'. Podaj tylko kategorię jako jedno słowo."
)

def classify_text(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś klasyfikatorem raportów patrolowych."},
            {"role": "user", "content": PROMPT},
            {"role": "user", "content": f"Oto treść: {text.strip()}"}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

def classify_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Jesteś klasyfikatorem raportów patrolowych."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{img_b64}"}
                    }
                ]
            }
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip().lower()

def transcribe_mp3(mp3_path: str) -> str:
    with open(mp3_path, "rb") as audio_file:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": (os.path.basename(mp3_path), audio_file, "audio/mpeg")},
            data={"model": "whisper-1", "language": "en"}
        )
    if response.status_code != 200:
        raise Exception(f"Transcription failed ({response.status_code}): {response.text}")
    return response.json()["text"]

def main():
    categories = {"people": [], "hardware": []}
    ignored = []

    for fname in sorted(os.listdir(SOURCE)):
        path = os.path.join(SOURCE, fname)
        if not os.path.isfile(path):
            continue

        if path.startswith(TRANSCRIPTIONS):
            continue

        ext = fname.lower().split(".")[-1]
        try:
            if ext == "txt":
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                result = classify_text(content)

            elif ext == "png":
                result = classify_image(path)

            elif ext == "mp3":
                txt_name = fname.replace(".mp3", ".txt")
                txt_path = os.path.join(TRANSCRIPTIONS, txt_name)

                if os.path.exists(txt_path):
                    with open(txt_path, "r", encoding="utf-8") as f:
                        text = f.read()
                else:
                    text = transcribe_mp3(path)
                    with open(txt_path, "w", encoding="utf-8") as f:
                        f.write(text)

                result = classify_text(text)

            else:
                continue

            if result in categories:
                categories[result].append(fname)
                print(f"{fname} → {result}")
            else:
                ignored.append(fname)

        except Exception as e:
            print(f"Error processing file {fname}: {e}")
            ignored.append(fname)

    payload = {
        "task": "kategorie",
        "apikey": DEVS_API_KEY,
        "answer": categories
    }

    try:
        r = requests.post(API_URL, json=payload)
        print(f"\nStatus: {r.status_code}")
        print(r.text)
    except Exception as e:
        print(f"\nSending error: {e}")

if __name__ == "__main__":
    main()
