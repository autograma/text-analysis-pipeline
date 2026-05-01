STOPWORDS = {"the", "a", "an", "is", "not", "but", "in", "on", "with", "it"}   # llaves = set

import string
string.punctuation


def read_file(path: str) -> str: ...
  

def clean_text(path: str) -> list[str]: ...
def save_processed(words: list[str], output_path: str) -> None: ...
