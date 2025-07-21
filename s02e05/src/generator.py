from loguru import logger
from bs4 import BeautifulSoup
from typing import Dict, Optional, List, Tuple
from pathlib import Path
from datetime import datetime
import tiktoken
from .indexers.text import convert_html_to_markdown
from .indexers.images import index_article_images
from .indexers.audio import index_article_audio

class ArticleGenerator:
    def __init__(self, output_dir: str = "output", max_tokens: int = 100_000):
        """Inicjalizuje generator artykułu.
        
        Args:
            output_dir: Katalog do zapisywania wygenerowanych plików
            max_tokens: Maksymalna liczba tokenów w wygenerowanym pliku
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")  # Tokenizer używany przez GPT-4
        
    def _count_tokens(self, text: str) -> int:
        """Liczy liczbę tokenów w tekście."""
        return len(self.tokenizer.encode(text))
        
    def _truncate_text(self, text: str, max_tokens: int) -> Tuple[str, int]:
        """Skraca tekst do określonej liczby tokenów."""
        tokens = self.tokenizer.encode(text)
        if len(tokens) <= max_tokens:
            return text, len(tokens)
            
        # Skróć tekst zachowując pełne zdania
        truncated_tokens = tokens[:max_tokens]
        # Znajdź ostatni znak końca zdania
        last_period = max(
            text[:self.tokenizer.decode(truncated_tokens).rfind('.') + 1].rfind('.'),
            text[:self.tokenizer.decode(truncated_tokens).rfind('!') + 1].rfind('!'),
            text[:self.tokenizer.decode(truncated_tokens).rfind('?') + 1].rfind('?')
        )
        if last_period > 0:
            truncated_text = text[:last_period + 1]
        else:
            truncated_text = self.tokenizer.decode(truncated_tokens)
            
        return truncated_text, len(truncated_tokens)
        
    def _truncate_audio_transcription(self, transcription: Dict, max_tokens: int) -> Dict:
        """Skraca transkrypcję audio zachowując najważniejsze informacje."""
        # Najpierw spróbuj skrócić segmenty
        if len(transcription["segments"]) > 1:
            # Zostaw tylko co drugi segment
            transcription["segments"] = transcription["segments"][::2]
            
        # Jeśli nadal za dużo tokenów, skróć pełną transkrypcję
        text_tokens = self._count_tokens(transcription["text"])
        if text_tokens > max_tokens:
            truncated_text, _ = self._truncate_text(transcription["text"], max_tokens)
            transcription["text"] = truncated_text + "\n\n[Transkrypcja została skrócona]"
            
        return transcription
        
    def _truncate_image_description(self, analysis: Dict, max_tokens: int) -> Dict:
        """Skraca opis obrazu zachowując najważniejsze informacje."""
        desc_tokens = self._count_tokens(analysis["description"])
        if desc_tokens > max_tokens:
            truncated_desc, _ = self._truncate_text(analysis["description"], max_tokens)
            analysis["description"] = truncated_desc + "\n\n[Opis został skrócony]"
        return analysis
        
    def _format_image_section(self, image_url: str, analysis: Dict) -> str:
        """Formatuje sekcję z opisem obrazu."""
        sections = []
        
        # Dodaj nagłówek z numerem rysunku jeśli dostępny
        if analysis["context"].get("figure_number"):
            sections.append(f"### Rysunek {analysis['context']['figure_number']}")
        else:
            sections.append("### Obraz")
            
        # Dodaj podpis jeśli dostępny
        if analysis["context"].get("caption"):
            sections.append(f"*{analysis['context']['caption']}*")
            
        # Dodaj tekst alternatywny jeśli dostępny
        if analysis["context"].get("alt_text"):
            sections.append(f"*Tekst alternatywny: {analysis['context']['alt_text']}*")
            
        # Dodaj opis obrazu
        sections.append("\n" + analysis["description"])
        
        # Dodaj link do oryginalnego obrazu
        sections.append(f"\n[Link do oryginalnego obrazu]({image_url})")
        
        return "\n\n".join(sections)
        
    def _format_audio_section(self, audio_url: str, transcription: Dict) -> str:
        """Formatuje sekcję z transkrypcją audio."""
        sections = []
        
        # Dodaj nagłówek
        sections.append("### Nagranie audio")
        
        # Dodaj tytuł jeśli dostępny
        if transcription["context"].get("title"):
            sections.append(f"*{transcription['context']['title']}*")
            
        # Dodaj opis jeśli dostępny
        if transcription["context"].get("description"):
            sections.append(f"*{transcription['context']['description']}*")
            
        # Dodaj pełną transkrypcję
        sections.append("\n**Transkrypcja:**")
        sections.append(transcription["text"])
        
        # Dodaj segmenty z timestampami tylko jeśli są dostępne i nie zostały skrócone
        if transcription["segments"] and len(transcription["segments"]) > 1:
            sections.append("\n**Szczegółowa transkrypcja z czasem:**")
            for segment in transcription["segments"]:
                start = int(segment["start"])
                end = int(segment["end"])
                sections.append(f"\n[{start:02d}:{end:02d}] {segment['text']}")
                
        # Dodaj link do oryginalnego pliku audio
        sections.append(f"\n[Link do oryginalnego nagrania]({audio_url})")
        
        return "\n\n".join(sections)
        
    def _split_content(self, sections: List[str], current_tokens: int) -> List[List[str]]:
        """Dzieli zawartość na części, jeśli przekracza limit tokenów."""
        if current_tokens <= self.max_tokens:
            return [sections]
            
        parts = []
        current_part = []
        current_part_tokens = 0
        
        for section in sections:
            section_tokens = self._count_tokens(section)
            
            # Jeśli pojedyncza sekcja przekracza limit, musimy ją skrócić
            if section_tokens > self.max_tokens:
                if current_part:
                    parts.append(current_part)
                    current_part = []
                    current_part_tokens = 0
                    
                # Skróć sekcję i dodaj jako nową część
                if "### Rysunek" in section:
                    # Dla obrazów zostaw tylko podstawowe informacje
                    lines = section.split('\n')
                    shortened = [lines[0]]  # Nagłówek
                    if len(lines) > 1:
                        shortened.append(lines[1])  # Podpis
                    shortened.append("[Opis został przeniesiony do osobnej części]")
                    shortened.append(lines[-1])  # Link
                    parts.append(['\n'.join(shortened)])
                elif "### Nagranie audio" in section:
                    # Dla audio zostaw tylko tytuł i link
                    lines = section.split('\n')
                    shortened = [lines[0]]  # Nagłówek
                    if len(lines) > 1:
                        shortened.append(lines[1])  # Tytuł
                    shortened.append("[Transkrypcja została przeniesiona do osobnej części]")
                    shortened.append(lines[-1])  # Link
                    parts.append(['\n'.join(shortened)])
                else:
                    # Dla tekstu skróć do limitu
                    shortened, _ = self._truncate_text(section, self.max_tokens)
                    parts.append([shortened])
                continue
                
            # Jeśli dodanie sekcji przekroczy limit, zacznij nową część
            if current_part_tokens + section_tokens > self.max_tokens:
                parts.append(current_part)
                current_part = [section]
                current_part_tokens = section_tokens
            else:
                current_part.append(section)
                current_part_tokens += section_tokens
                
        if current_part:
            parts.append(current_part)
            
        return parts
        
    def generate_article(self, html_content: str, title: Optional[str] = None) -> List[Path]:
        """Generuje pliki Markdown z przetworzonym artykułem.
        
        Args:
            html_content: Zawartość HTML artykułu
            title: Opcjonalny tytuł artykułu (jeśli nie podany, zostanie wyciągnięty z HTML)
            
        Returns:
            Lista ścieżek do wygenerowanych plików
        """
        # Przetwórz tekst
        markdown_content = convert_html_to_markdown(html_content)
        
        # Pobierz tytuł jeśli nie podany
        if not title:
            soup = BeautifulSoup(html_content, 'html.parser')
            title_elem = soup.find('title')
            title = title_elem.get_text().strip() if title_elem else "Artykuł"
            
        # Indeksuj obrazy i audio
        logger.info("Indexing images...")
        images = index_article_images(html_content)
        logger.info("Indexing audio...")
        audio_files = index_article_audio(html_content)
        
        # Przygotuj zawartość pliku
        sections = []
        
        # Dodaj nagłówek
        header = f"# {title}\n\n*Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        sections.append(header)
        
        # Dodaj tekst artykułu
        sections.append("\n## Treść artykułu")
        sections.append(markdown_content)
        
        # Dodaj sekcję z obrazami
        if images:
            sections.append("\n## Obrazy")
            for url, analysis in images.items():
                # Skróć opis obrazu jeśli potrzeba
                analysis = self._truncate_image_description(analysis, self.max_tokens // 10)  # 10% limitu na obraz
                sections.append(self._format_image_section(url, analysis))
                
        # Dodaj sekcję z nagraniami
        if audio_files:
            sections.append("\n## Nagrania audio")
            for url, transcription in audio_files.items():
                # Skróć transkrypcję jeśli potrzeba
                transcription = self._truncate_audio_transcription(transcription, self.max_tokens // 5)  # 20% limitu na audio
                sections.append(self._format_audio_section(url, transcription))
                
        # Policz tokeny i podziel na części jeśli potrzeba
        total_tokens = sum(self._count_tokens(section) for section in sections)
        logger.info("Total tokens in content: {}", total_tokens)
        
        content_parts = self._split_content(sections, total_tokens)
        output_paths = []
        
        # Wygeneruj pliki dla każdej części
        for i, part in enumerate(content_parts):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"article_{timestamp}_part{i+1}.md" if len(content_parts) > 1 else f"article_{timestamp}.md"
            output_path = self.output_dir / filename
            
            # Zapisz plik
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n\n".join(part))
                
            output_paths.append(output_path)
            logger.success("Generated article part {}: {}", i+1, output_path)
            
        return output_paths

def generate_article_markdown(html_content: str, title: Optional[str] = None) -> List[Path]:
    """Funkcja pomocnicza do generowania pliku Markdown z artykułem."""
    generator = ArticleGenerator()
    return generator.generate_article(html_content, title) 