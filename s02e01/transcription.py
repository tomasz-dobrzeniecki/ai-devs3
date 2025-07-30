from pathlib import Path
from openai import OpenAI
from config import OPENAI_API_KEY

def transcribe_audio(file_path: str, client, logger) -> str:
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pl"
            )
        return transcript.text
    except Exception as e:
        logger.error(f"Transcription failed for {file_path}: {e}")
        return ""

def get_all_transcriptions(audio_dir: str, logger) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    transcriptions = {}
    for audio_file in Path(audio_dir).glob("*.m4a"):
        logger.info(f"Transcribing {audio_file.name}...")
        transcriptions[audio_file.stem] = transcribe_audio(str(audio_file), client, logger)
    return transcriptions
