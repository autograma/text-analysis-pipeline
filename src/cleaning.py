"""Text cleaning module: read, clean, and save processed text."""

import logging
import string
from pathlib import Path

logger = logging.getLogger(__name__) 
#path = Path("data/raw/biotechnology-abolish.txt")

STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "of", "in", "to",
    "for", "on", "with", "at", "by", "from", "and", "or", "but",
    "not", "it", "this", "that",
}

def read_file(path: data/raw/biotechnology-abolish.txt) -> str:
    
    """Read a .txt file and return its content as a string."""    
    
    with open(path,'r',encoding='utf-8') as 'f':
    content = f.read()

    ""ValueError: If the file is empty."""
    if not content.strip():
        raise ValueError(f"File not found: {path}")
        return content
    ...
        FileNotFoundError: If the file does not exist.

    """
    # TODO 1: convertir path a Path y chequear que exista; si no, raise FileNotFoundError
    # TODO 2: abrir el archivo con encoding='utf-8' y leer su contenido
    # TODO 3: si el contenido (sin espacios) está vacío, raise ValueError
    # TODO 4: return contenido


def clean_text(text: str) -> list[str]:
        
    """Lowercase, strip punctuation, remove stopwords, return clean words.

    Args:
        text: Raw text to clean.

    Returns:
        List of clean words (lowercased, no punctuation, no stopwords, no pure-numeric tokens).
    """
    # TODO 1: pasar texto a minúsculas y dividir en tokens con .split()
    # TODO 2: para cada token, quitar puntuación con .strip(string.punctuation)
    # TODO 3: descartar el token si: queda vacío, está en STOPWORDS, o es .isdigit()
    # TODO 4: return la lista de tokens que sobrevivieron


def save_processed(words: list[str], output_path: str) -> None:
    """Write cleaned words to a file, one per line.

    Args:
        words: List of clean words.
        output_path: Path where the file will be written.
    """
    # TODO 1: asegurarse de que el directorio padre existe (Path(...).parent.mkdir(parents=True, exist_ok=True))
    # TODO 2: abrir output_path en modo 'w' con encoding='utf-8'
    # TODO 3: escribir cada palabra en una línea
