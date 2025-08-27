from pathlib import Path
from typing import Dict, List
from openai import OpenAI

def transcribe_audios(audios: List[dict], model: str) -> Dict[str, str]:
    """
    audios: [{url, path}]
    Returns {filename: transcript_text}
    """
    client = OpenAI()
    out: Dict[str, str] = {}
    cache_dir = Path("cache/audio")
    cache_dir.mkdir(parents=True, exist_ok=True)

    for item in audios:
        path = Path(item["path"])
        cache_file = cache_dir / f"{path.stem}.txt"
        if cache_file.exists():
            txt = cache_file.read_text(encoding="utf-8")
            out[path.name] = txt
            continue

        with open(path, "rb") as f:
            # Official STT endpoint (Python SDK)
            # See: Speech-to-text docs (gpt-4o-mini-transcribe) 
            transcript = client.audio.transcriptions.create(
                model=model,
                file=f,
                response_format="text",
                temperature=0.0,
            )
        text = transcript.strip()
        cache_file.write_text(text, encoding="utf-8")
        out[path.name] = text
    return out
