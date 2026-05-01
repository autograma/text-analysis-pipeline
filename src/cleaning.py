STOPWORDS = {"the", "a", "an", "is", "not", "but", "in", "on", "with", "it"}   # llaves = set
logger = logging.getLogger(__name__) 

import string
string.punctuation


def read_file(path: str) -> str: ...
  archive = open("biotechnology-abolish","r",encoding:'utf-8')

def clean_text(path: str) -> list[str]:
  
En limpiar_texto: texto.lower().split() → recorré, limpiá puntuación con strip, descartá vacíos, descartá stopwords, descartá si palabra.isdigit().

def save_processed(words: list[str], output_path: str) -> None: ...
