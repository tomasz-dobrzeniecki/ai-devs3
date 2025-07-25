from config import client, CENTRALA_KEY
from transcription import get_all_transcriptions
from prompt_builder import create_prompt
from llm_client import get_llm_answer
from extract import extract_street_name
from submitter import submit_answer

def main():
    transcriptions = get_all_transcriptions("audio", client)
    prompt = create_prompt(transcriptions)
    response = get_llm_answer(prompt, client)
    print(response)

    street = extract_street_name(response)
    if street:
        submit_answer(street, CENTRALA_KEY)

if __name__ == "__main__":
    main()