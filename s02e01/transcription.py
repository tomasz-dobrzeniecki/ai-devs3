from pathlib import Path
from loguru import logger

def transcribe_audio(file_path: str, client) -> str:
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

def get_all_transcriptions(audio_dir: str, client) -> dict:
    transcriptions = {}
    for audio_file in Path(audio_dir).glob("*.m4a"):
        logger.info(f"Transcribing {audio_file.name}...")
        transcriptions[audio_file.stem] = transcribe_audio(str(audio_file), client)
    return transcriptions
