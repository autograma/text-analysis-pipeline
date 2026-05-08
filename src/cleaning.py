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

def read_file(path: str) -> str:
    """Read a .txt file and return its content as a string.

    Args:
        path: Path to the .txt file to read.

    Returns:
        The file content as a single string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or contains only whitespace.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        raise ValueError(f"File is empty: {file_path}")

    return content

def clean_text(text: str) -> list[str]:
    """Lowercase, strip punctuation, remove stopwords, and discard pure-numeric tokens.

    Args:
        text: Raw text to clean.

    Returns:
        List of clean words. Empty if no token survives the filters.
    """
    tokens = text.lower().split()

    cleaned = []
    for token in tokens:
        word = token.strip(string.punctuation)
        if not word:
            continue
        if word in STOPWORDS:
            continue
        if word.isdigit():
            continue
        cleaned.append(word)

    return cleaned

def save_processed(words: list[str], output_path: str) -> None:
    """Write cleaned words to a file, one per line.

    Args:
        words: List of clean words.
        output_path: Path where the file will be written.
    """
    # TODO 1: asegurarse de que el directorio padre existe (Path(...).parent.mkdir(parents=True, exist_ok=True))
    # TODO 2: abrir output_path en modo 'w' con encoding='utf-8'
    # TODO 3: escribir cada palabra en una línea
