from loguru import logger
import html2text
from bs4 import BeautifulSoup
from typing import Dict, Optional

class TextIndexer:
    def __init__(self):
        # Konfiguracja html2text
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.ignore_images = True  # Obrazy będą obsługiwane osobno
        self.converter.ignore_emphasis = False
        self.converter.body_width = 0  # Bez zawijania tekstu
        self.converter.protect_links = True
        self.converter.unicode_snob = True  # Zachowaj znaki Unicode
        
    def clean_html(self, html_content: str) -> str:
        """Czyści HTML z niepotrzebnych elementów przed konwersją."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Usuń skrypty i style
        for element in soup.find_all(['script', 'style']):
            element.decompose()
            
        # Usuń komentarze
        for comment in soup.find_all(text=lambda text: isinstance(text, str) and text.strip().startswith('<!--')):
            comment.extract()
            
        # Zachowaj tylko treść body
        body = soup.find('body')
        if body:
            return str(body)
        return str(soup)
    
    def index_text(self, html_content: str) -> Dict[str, str]:
        """Indeksuje tekst z HTML do czystego Markdown.
        
        Returns:
            Dict zawierający:
            - 'raw_markdown': surowy tekst w formacie Markdown
            - 'clean_markdown': oczyszczony tekst (bez nadmiarowych znaków nowej linii)
        """
        try:
            # Wyczyść HTML
            clean_html = self.clean_html(html_content)
            logger.debug("HTML cleaned, length: {}", len(clean_html))
            
            # Konwertuj do Markdown
            raw_markdown = self.converter.handle(clean_html)
            logger.debug("Converted to Markdown, length: {}", len(raw_markdown))
            
            # Oczyść Markdown
            clean_markdown = self._clean_markdown(raw_markdown)
            logger.debug("Markdown cleaned, length: {}", len(clean_markdown))
            
            return {
                'raw_markdown': raw_markdown,
                'clean_markdown': clean_markdown
            }
            
        except Exception as e:
            logger.exception("Error during text indexing")
            raise
    
    def _clean_markdown(self, markdown: str) -> str:
        """Czyści wygenerowany Markdown z nadmiarowych elementów."""
        lines = markdown.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Usuń puste linie na początku i końcu
            if not line.strip() and (not cleaned_lines or not cleaned_lines[-1].strip()):
                continue
                
            # Usuń nadmiarowe spacje
            line = ' '.join(line.split())
            
            cleaned_lines.append(line)
        
        # Połącz linie, zachowując podwójne znaki nowej linii dla paragrafów
        return '\n\n'.join(line for line in cleaned_lines if line.strip())

def index_article_text(html_content: str) -> Dict[str, str]:
    """Funkcja pomocnicza do indeksowania tekstu artykułu."""
    indexer = TextIndexer()
    return indexer.index_text(html_content)

def convert_html_to_markdown(html_content: str) -> str:
    """Konwertuje HTML do czystego Markdown.
    
    Args:
        html_content: Zawartość HTML do konwersji
        
    Returns:
        Tekst w formacie Markdown
    """
    indexer = TextIndexer()
    result = indexer.index_text(html_content)
    return result['clean_markdown'] 