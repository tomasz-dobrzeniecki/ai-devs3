from loguru import logger
from pathlib import Path
import json
import hashlib
from typing import Dict, Optional, Any
from datetime import datetime

class CacheManager:
    def __init__(self, base_dir: str = "cache"):
        """Inicjalizuje menedżer cache.
        
        Args:
            base_dir: Główny katalog cache
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Podkatalogi dla różnych typów danych
        self.dirs = {
            'text': self.base_dir / 'text',
            'images': self.base_dir / 'images',
            'audio': self.base_dir / 'audio'
        }
        
        # Utwórz podkatalogi
        for dir_path in self.dirs.values():
            dir_path.mkdir(exist_ok=True)
            
    def _get_hash(self, content: str) -> str:
        """Generuje unikalny hash dla zawartości."""
        return hashlib.md5(content.encode()).hexdigest()
        
    def _get_cache_path(self, cache_type: str, content_hash: str) -> Path:
        """Zwraca ścieżkę do pliku cache."""
        if cache_type not in self.dirs:
            raise ValueError(f"Nieznany typ cache: {cache_type}")
        return self.dirs[cache_type] / f"{content_hash}.json"
        
    def get(self, cache_type: str, content: str) -> Optional[Dict]:
        """Pobiera dane z cache.
        
        Args:
            cache_type: Typ cache ('text', 'images', 'audio')
            content: Zawartość do zhashowania (np. URL + kontekst)
            
        Returns:
            Dane z cache lub None jeśli nie znaleziono
        """
        try:
            content_hash = self._get_hash(content)
            cache_path = self._get_cache_path(cache_type, content_hash)
            
            if cache_path.exists():
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.debug("Cache hit for {}: {}", cache_type, content_hash)
                    return data
                    
            logger.debug("Cache miss for {}: {}", cache_type, content_hash)
            return None
            
        except Exception as e:
            logger.warning("Failed to load from cache: {}", e)
            return None
            
    def set(self, cache_type: str, content: str, data: Dict):
        """Zapisuje dane do cache.
        
        Args:
            cache_type: Typ cache ('text', 'images', 'audio')
            content: Zawartość do zhashowania
            data: Dane do zapisania
        """
        try:
            content_hash = self._get_hash(content)
            cache_path = self._get_cache_path(cache_type, content_hash)
            
            # Dodaj timestamp jeśli go nie ma
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now().isoformat()
                
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                logger.debug("Saved to cache {}: {}", cache_type, content_hash)
                
        except Exception as e:
            logger.warning("Failed to save to cache: {}", e)
            
    def clear(self, cache_type: Optional[str] = None):
        """Czyści cache.
        
        Args:
            cache_type: Typ cache do wyczyszczenia (None = wszystkie)
        """
        try:
            if cache_type:
                if cache_type not in self.dirs:
                    raise ValueError(f"Nieznany typ cache: {cache_type}")
                dirs_to_clear = [self.dirs[cache_type]]
            else:
                dirs_to_clear = self.dirs.values()
                
            for dir_path in dirs_to_clear:
                for cache_file in dir_path.glob('*.json'):
                    cache_file.unlink()
                logger.info("Cleared cache: {}", dir_path)
                
        except Exception as e:
            logger.warning("Failed to clear cache: {}", e)
            
    def get_stats(self) -> Dict[str, int]:
        """Zwraca statystyki cache."""
        stats = {}
        for cache_type, dir_path in self.dirs.items():
            try:
                stats[cache_type] = len(list(dir_path.glob('*.json')))
            except Exception as e:
                logger.warning("Failed to get stats for {}: {}", cache_type, e)
                stats[cache_type] = 0
        return stats

# Singleton instance
cache_manager = CacheManager() 
 