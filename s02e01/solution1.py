import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import requests
from typing import List, Dict

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path: str) -> str:
    """Transcribe a single audio file using Whisper."""
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pl"  # Polish language
            )
        return transcript.text
    except Exception as e:
        print(f"Error transcribing {file_path}: {str(e)}")
        return ""

def get_all_transcriptions(audio_dir: str) -> Dict[str, str]:
    """Get transcriptions for all audio files in the directory."""
    transcriptions = {}
    audio_path = Path(audio_dir)
    
    for audio_file in audio_path.glob("*.m4a"):
        print(f"Transcribing {audio_file.name}...")
        transcription = transcribe_audio(str(audio_file))
        transcriptions[audio_file.stem] = transcription
    
    return transcriptions

def create_prompt(transcriptions: Dict[str, str]) -> str:
    """Create a prompt for the LLM using all transcriptions."""
    combined_context = "\n\n".join([
        f"Transkrypcja {name}:\n{text}"
        for name, text in transcriptions.items()
    ])
    
    prompt = f"""Twoim zadaniem jest ustalenie nazwy ulicy, na której znajduje się konkretny instytut uczelni, gdzie wykłada profesor Andrzej Maj.

Przeanalizuj poniższe transkrypcje zeznań świadków i krok po kroku wyciągnij wnioski:

{combined_context}

Pamiętaj:
1. Szukamy ulicy, na której znajduje się instytut, a nie główna siedziba uczelni
2. Niektóre zeznania mogą być chaotyczne lub wprowadzać w błąd - dokładnie przeanalizuj wszystkie informacje
3. Użyj swojej wiedzy o polskich uczelniach, aby ustalić nazwę ulicy
4. Przedstaw swoje rozumowanie krok po kroku
5. Na końcu podaj konkretną nazwę ulicy

Proszę o analizę:"""
    
    return prompt

def get_llm_answer(prompt: str) -> str:
    """Get answer from GPT-4 using the prompt."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś asystentem, który analizuje transkrypcje i ustala fakty. Odpowiadaj po polsku."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting LLM answer: {str(e)}")
        return ""

def submit_answer(street_name: str) -> None:
    """Submit the answer to Centrala."""
    url = "https://c3ntrala.ag3nts.org/report"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json"
    }
    payload = {
        "task": "mp3",
        "apikey": "7f6ff94a-ced2-46e2-8c90-aa4fdec3b948",
        "answer": street_name
    }
    
    try:
        # Ensure the payload is properly encoded in UTF-8
        payload_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        print(f"Sending payload (UTF-8): {payload_bytes.decode('utf-8')}")
        
        response = requests.post(
            url, 
            data=payload_bytes,  # Send as bytes instead of json parameter
            headers=headers,
            verify=True
        )
        response.raise_for_status()
        print("Response from Centrala:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error submitting answer: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response text: {e.response.text}")

def extract_street_name(llm_response: str) -> str:
    """Extract the street name from LLM response."""
    import re
    
    # First try to find explicit street name mentions
    explicit_patterns = [
        r"ulic[ay]\s+([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\.]+)(?=\s+w\s+Krakowie|\s+w\s+Krakowa|\.|$)",
        r"na\s+ulic[yi]\s+([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\.]+)(?=\s+w\s+Krakowie|\s+w\s+Krakowa|\.|$)",
        r"znajduje\s+się\s+na\s+ulic[yi]\s+([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\.]+)(?=\s+w\s+Krakowie|\s+w\s+Krakowa|\.|$)",
        r"mieszczący\s+się\s+na\s+ulic[yi]\s+([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ\s\.]+)(?=\s+w\s+Krakowie|\s+w\s+Krakowa|\.|$)"
    ]
    
    for pattern in explicit_patterns:
        match = re.search(pattern, llm_response, re.IGNORECASE)
        if match:
            street_name = match.group(1).strip()
            # Remove any existing "ulica" or "ul." prefix
            street_name = re.sub(r'^(ulica|ul\.)\s+', '', street_name, flags=re.IGNORECASE)
            return f"ul. {street_name}"
    
    # If no explicit mention found, try to find the final answer marked with **
    final_answer = re.search(r"\*\*(.*?)\*\*", llm_response)
    if final_answer:
        street_name = final_answer.group(1).strip()
        # Look for street name in the final answer
        for pattern in explicit_patterns:
            match = re.search(pattern, street_name, re.IGNORECASE)
            if match:
                street_name = match.group(1).strip()
                street_name = re.sub(r'^(ulica|ul\.)\s+', '', street_name, flags=re.IGNORECASE)
                return f"ul. {street_name}"
    
    # If still no match, try to find any sentence containing both "ulica" and "Kraków"
    sentences = llm_response.split('.')
    for sentence in sentences:
        if 'ulic' in sentence.lower() and 'kraków' in sentence.lower():
            for pattern in explicit_patterns:
                match = re.search(pattern, sentence, re.IGNORECASE)
                if match:
                    street_name = match.group(1).strip()
                    street_name = re.sub(r'^(ulica|ul\.)\s+', '', street_name, flags=re.IGNORECASE)
                    return f"ul. {street_name}"
    
    print("Warning: Could not extract street name from LLM response")
    print("Full response for debugging:")
    print(llm_response)
    return ""

def main():
    # Get transcriptions
    audio_dir = "audio"
    print("Starting transcription process...")
    transcriptions = get_all_transcriptions(audio_dir)
    
    # Create and execute prompt
    print("\nCreating prompt and getting LLM analysis...")
    prompt = create_prompt(transcriptions)
    llm_response = get_llm_answer(prompt)
    
    print("\nLLM Response:")
    print(llm_response)
    
    # Extract and submit street name
    street_name = extract_street_name(llm_response)
    if not street_name:
        print("Error: Could not extract street name from LLM response")
        return
        
    print(f"\nExtracted street name: {street_name}")
    
    print("\nSubmitting answer to Centrala...")
    submit_answer(street_name)

if __name__ == "__main__":
    main() 