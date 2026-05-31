"""Word frequency analysis: count words and export tables"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

def count_frequency(words: list[str]) -> dict[str, int]:

    
    """Count how many times each word appears in the list
    
    Args:
    words: List of words to count.
    
    Returns:
    Dictionary mapping each unique word to its count.
    Empty if input list is empty
    """
    freq = {}
    for word in words:

        if word not in freq:
            freq[word]=1
        else:
            freq[word]+=1

    return freq


def frequency_to_dataframe(freq_dict: dict) -> pd.DataFrame:

    """Convert a {word: count} dict into a sorted DataFrame.
    Args:
        freq_dict: Dictionary mapping words to their frequencies

    Returns:
        DataFrame with columns ['word', 'frequency'], sorted by
        frequency descending. Returns an empty DataFrame with those
        columns if freq_dict is empty.
    """
    
    df = (
        pd.DataFrame(list(freq_dict.items()), columns=["word", "frequency"])
        .sort_values(by="frequency", ascending=False)
        .reset_index(drop=True)
    )
   
    return df 

def export_csv(df: pd.DataFrame, path: str) -> None:

    """Save a DataFrame to CSV. Creates parent directories if needed.
    
    Args:
        df: DataFrame to save.
        path: Path where the CSV file will be written.
    """

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
