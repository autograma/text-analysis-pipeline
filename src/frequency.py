"""Word frequency analysis: count words and export tables"""

import logging
from turtle import pd

logger = logging.getLogger(__name__)

def count_frequency(words: list[str]) -> dict[str, int]:

    
    """Count how many times each word appears in the list
    
    Args:
    words: List of words to count.
    
    Returns
    Dictionatry mapping each unique word to its count.
    Empty if input list is empty
    """
    freq = {}
    for word in words:

        if word not in freq:
            freq[word]=1
        else:
            freq[word]+=1

    return freq

def frequency_dataframe(freq_dict_: dict) -> pd.DataFrame:
    freq = pd.DataFrame(list(freq_dict_.items()), columns=['Word', 'Frequency'])
    return freq



