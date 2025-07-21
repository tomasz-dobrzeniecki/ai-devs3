from loguru import logger
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import tempfile
import os
from urllib.parse import urljoin
from .cache import cache_manager
from pydub import AudioSegment
from faster_whisper import WhisperModel

@dataclass
class AudioContext:
    """Kontekst pliku audio."""
    url: str
    title: Optional[str] = None
    description: Optional[str] = None

class AudioIndexer:
    """Indekser plików audio z artykułu."""
    
    def __init__(self, model_size: str = "base"):
        """Inicjalizacja indeksera audio.
        
        Args:
            model_size: Rozmiar modelu Whisper ('tiny', 'base', 'small', 'medium', 'large')
        """
        logger.info(f"Ładowanie modelu Whisper: {model_size}")
        # Używamy CPU dla lepszej kompatybilności
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        logger.info("Model Whisper załadowany")
        
    def _get_cache_key(self, audio_url: str, context: AudioContext) -> str:
        """Generuje unikalny klucz cache dla pliku audio."""
        # Używamy URL i kontekstu do generowania klucza
        context_str = f"{context.title or ''}{context.description or ''}"
        key_data = f"{audio_url}:{context_str}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def _download_audio(self, url: str) -> Path:
        """Pobiera plik audio do tymczasowego katalogu."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Tworzymy tymczasowy plik
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = Path(temp_file.name)
            
            # Zapisujemy plik
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return temp_path
            
        except Exception as e:
            logger.error(f"Błąd podczas pobierania pliku audio {url}: {e}")
            raise
    
    def _transcribe_audio(self, audio_path: Path) -> Dict:
        """Transkrybuje plik audio używając Faster Whisper."""
        try:
            # Konwertujemy MP3 do WAV (lepsza jakość dla Whisper)
            audio = AudioSegment.from_mp3(str(audio_path))
            wav_path = audio_path.with_suffix('.wav')
            audio.export(str(wav_path), format="wav", parameters=["-ar", "16000"])  # 16kHz dla Whisper
            
            # Transkrybujemy audio
            segments, info = self.model.transcribe(
                str(wav_path),
                language="pl",
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Zbieramy segmenty
            segments_list = []
            full_text = []
            
            for segment in segments:
                segments_list.append({
                    "text": segment.text.strip(),
                    "start": segment.start,
                    "end": segment.end,
                    "confidence": segment.confidence
                })
                full_text.append(segment.text.strip())
            
            # Czyszczenie tymczasowych plików
            wav_path.unlink()
            audio_path.unlink()
            
            return {
                "text": " ".join(full_text),
                "segments": segments_list,
                "language": info.language,
                "language_probability": info.language_probability
            }
            
        except Exception as e:
            logger.error(f"Nieoczekiwany błąd podczas transkrypcji {audio_path}: {e}")
            return {
                "text": "",
                "segments": [],
                "language": "pl",
                "error": f"Nieoczekiwany błąd: {str(e)}"
            }
    
    def _extract_audio_info(self, html_content: str, base_url: str) -> List[AudioContext]:
        """Wyciąga informacje o plikach audio z HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        audio_contexts = []
        
        # Szukamy elementów audio
        for audio in soup.find_all('audio'):
            src = audio.get('src')
            if not src:
                continue
                
            # Budujemy pełny URL
            audio_url = urljoin(base_url, src)
            
            # Szukamy kontekstu (tytuł, opis)
            title = audio.get('title')
            description = None
            
            # Szukamy opisu w otaczających elementach
            parent = audio.find_parent(['figure', 'div', 'p'])
            if parent:
                # Szukamy tekstu przed lub po audio
                caption = parent.find(['figcaption', 'p'])
                if caption:
                    description = caption.get_text(strip=True)
            
            audio_contexts.append(AudioContext(
                url=audio_url,
                title=title,
                description=description
            ))
        
        return audio_contexts
    
    def index_audio(self, html_content: str, base_url: str) -> Dict[str, Dict]:
        """Indeksuje pliki audio z artykułu."""
        try:
            # Wyciągamy informacje o plikach audio
            audio_contexts = self._extract_audio_info(html_content, base_url)
            if not audio_contexts:
                logger.info("Nie znaleziono plików audio w artykule")
                return {}
            
            indexed_audio = {}
            
            # Przetwarzamy każdy plik audio
            for context in audio_contexts:
                cache_key = self._get_cache_key(context.url, context)
                
                # Sprawdzamy cache
                cached_result = cache_manager.get('audio', cache_key)
                if cached_result:
                    logger.debug(f"Użyto transkrypcji z cache dla {context.url}")
                    indexed_audio[context.url] = cached_result
                    continue
                
                # Pobieramy i transkrybujemy audio
                logger.info(f"Transkrybuję audio: {context.url}")
                audio_path = self._download_audio(context.url)
                transcription = self._transcribe_audio(audio_path)
                
                # Dodajemy kontekst do wyniku
                result = {
                    "transcription": transcription,
                    "context": {
                        "title": context.title,
                        "description": context.description
                    }
                }
                
                # Zapisujemy do cache
                cache_manager.save('audio', cache_key, result)
                indexed_audio[context.url] = result
            
            return indexed_audio
            
        except Exception as e:
            logger.error(f"Błąd podczas indeksowania audio: {e}")
            return {}

def index_article_audio(html_content: str, base_url: str = "https://c3ntrala.ag3nts.org/dane/arxiv-draft.html") -> Dict[str, Dict]:
    """Funkcja pomocnicza do indeksowania audio z artykułu."""
    indexer = AudioIndexer()
    return indexer.index_audio(html_content, base_url) 