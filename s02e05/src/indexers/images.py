from loguru import logger
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
import base64
from io import BytesIO
from PIL import Image
from dataclasses import dataclass
from datetime import datetime
from openai import OpenAI
from .cache import cache_manager

@dataclass
class ImageContext:
    url: str
    alt_text: Optional[str] = None
    caption: Optional[str] = None
    figure_number: Optional[str] = None

class ImageIndexer:
    def __init__(self):
        self.client = OpenAI()
        
    def _get_cache_key(self, url: str, context: ImageContext) -> str:
        """Generuje klucz cache dla obrazu."""
        return f"{url}|{context.alt_text}|{context.caption}|{context.figure_number}"
            
    def _download_image(self, url: str) -> Optional[bytes]:
        """Pobiera obraz z URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Sprawdź czy to obraz
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                logger.warning("URL {} nie jest obrazem (content-type: {})", url, content_type)
                return None
                
            return response.content
            
        except Exception as e:
            logger.warning("Failed to download image {}: {}", url, e)
            return None
            
    def _prepare_image_context(self, context: ImageContext) -> str:
        """Przygotowuje tekst kontekstu dla modelu."""
        context_parts = []
        
        if context.figure_number:
            context_parts.append(f"Numer rysunku: {context.figure_number}")
        if context.alt_text:
            context_parts.append(f"Tekst alternatywny: {context.alt_text}")
        if context.caption:
            context_parts.append(f"Podpis: {context.caption}")
            
        return "\n".join(context_parts) if context_parts else "Brak dodatkowego kontekstu."
        
    def _analyze_image(self, image_data: bytes, context: ImageContext) -> Optional[Dict]:
        """Analizuje obraz używając GPT-4 Vision."""
        try:
            # Konwertuj obraz do base64
            image = Image.open(BytesIO(image_data))
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Przygotuj kontekst
            context_text = self._prepare_image_context(context)
            
            # Przygotuj wiadomość dla modelu
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert in analyzing scientific and technical images.
                    Your primary task is to accurately describe what you see in the image.
                    
                    PRIORITY: Describe the visual content in detail:
                    1. Main subject/object and its characteristics
                    2. All visible elements and their spatial relationships
                    3. Text, labels, or symbols visible in the image
                    4. Colors, shapes, patterns, and other visual features
                    
                    CONTEXT: Treat the provided context (caption, alt text, figure number) as supplementary:
                    - Use it only to better understand the image
                    - If context suggests something not visible in the image, focus on what you see
                    - If context contradicts what you see, describe what you see
                    
                    The description should be:
                    - Objective and based on visual facts
                    - Detailed but focused on visible elements
                    - In Polish language
                    - Without speculation about things not visible
                    """
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze the following image.
                            First, describe in detail what you see in the image.
                            Then, if relevant, consider the context:
                            {context_text}
                            
                            Remember: the most important is what you see in the image."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}"
                            }
                        }
                    ]
                }
            ]
            
            # Wywołaj model
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=messages,
                max_tokens=500,
                temperature=0.3
            )
            
            return {
                "description": response.choices[0].message.content,
                "context": {
                    "alt_text": context.alt_text,
                    "caption": context.caption,
                    "figure_number": context.figure_number
                }
            }
            
        except Exception as e:
            logger.exception("Error during image analysis")
            return None
            
    def extract_images(self, html_content: str) -> List[ImageContext]:
        """Wyciąga informacje o obrazach z HTML."""
        soup = BeautifulSoup(html_content, 'html.parser')
        images = []
        
        # Szukaj obrazów w figure
        for figure in soup.find_all('figure'):
            img = figure.find('img')
            if not img:
                continue
                
            # Pobierz URL obrazu
            url = img.get('src', '')
            if not url:
                continue
                
            # Popraw URL jeśli zaczyna się od //
            if url.startswith('//'):
                url = 'https:' + url
                
            # Popraw błąd w domenie
            url = url.replace('c3ntrala.ag3nts.orgi', 'c3ntrala.ag3nts.org')
            
            # Pobierz kontekst
            alt_text = img.get('alt', '')
            caption = figure.find('figcaption')
            caption_text = caption.get_text().strip() if caption else None
            
            # Spróbuj znaleźć numer rysunku w podpisie
            figure_number = None
            if caption_text:
                # Szukaj wzorców typu "Rysunek 1:", "Fig. 1:", itp.
                import re
                figure_match = re.search(r'(?:Rysunek|Fig\.?)\s*(\d+)', caption_text, re.IGNORECASE)
                if figure_match:
                    figure_number = figure_match.group(1)
            
            images.append(ImageContext(
                url=url,
                alt_text=alt_text,
                caption=caption_text,
                figure_number=figure_number
            ))
            
        return images
        
    def index_images(self, html_content: str) -> Dict[str, Dict]:
        """Indeksuje wszystkie obrazy z HTML."""
        images = self.extract_images(html_content)
        results = {}
        
        for img_context in images:
            # Generuj klucz cache
            cache_key = self._get_cache_key(img_context.url, img_context)
            
            # Sprawdź cache
            cached_result = cache_manager.get('images', cache_key)
            if cached_result:
                results[img_context.url] = cached_result
                continue
                
            # Pobierz obraz
            image_data = self._download_image(img_context.url)
            if not image_data:
                continue
                
            # Analizuj obraz
            analysis = self._analyze_image(image_data, img_context)
            if analysis:
                # Zapisz do cache
                cache_manager.set('images', cache_key, analysis)
                results[img_context.url] = analysis
                
        return results

def index_article_images(html_content: str) -> Dict[str, Dict]:
    """Funkcja pomocnicza do indeksowania obrazów artykułu."""
    indexer = ImageIndexer()
    return indexer.index_images(html_content) 