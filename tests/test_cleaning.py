"""Tests for src/cleaning.py."""

import pytest

from src.cleaning import clean_text, read_file, save_processed


# ---- clean_text ----

def test_clean_text_basic():
    """Lowercased, stopwords removed, regular words kept."""
    result = clean_text("The cat sat on the mat.")
    assert result == ["cat", "sat", "mat"]


def test_clean_text_empty_string():
    """Empty input returns empty list, no error."""
    assert clean_text("") == []


def test_clean_text_only_punctuation():
    """Tokens that are pure punctuation produce empty list."""
    assert clean_text("... !!! ???") == []


def test_clean_text_only_stopwords():
    """A text made of only stopwords produces empty list."""
    assert clean_text("the a an is to of") == []


def test_clean_text_discards_numbers():
    """Tokens that are pure digits are filtered out."""
    result = clean_text("In 2024 there were 5 papers.")
    assert "2024" not in result
    assert "5" not in result
    assert "papers" in result


def test_clean_text_filters_roman_numerals():
    assert clean_text("chapter ii section iii of iv") == ["chapter", "section"]

def test_clean_text_strips_surrounding_punctuation():
    """Punctuation around a word is stripped, the word survives."""
    result = clean_text("hello, world!")
    assert "hello" in result
    assert "world" in result


def test_clean_text_preserves_internal_apostrophe():
    result = clean_text("don't worry")
    assert "don't" in result 


# ---- read_file ----

def test_read_file_not_found():
    """Missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_file("nonexistent_file.txt")


def test_read_file_empty(tmp_path):
    """Empty file raises ValueError."""
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        read_file(str(file_path))


def test_read_file_whitespace_only(tmp_path):
    """File with only whitespace also raises ValueError."""
    file_path = tmp_path / "whitespace.txt"
    file_path.write_text("   \n\n   ", encoding="utf-8")
    with pytest.raises(ValueError):
        read_file(str(file_path))


def test_read_file_valid(tmp_path):
    """Valid non-empty file returns its content as string."""
    file_path = tmp_path / "valid.txt"
    file_path.write_text("hello world", encoding="utf-8")
    assert read_file(str(file_path)) == "hello world"


# ---- save_processed ----

def test_save_processed_writes_words(tmp_path):
    """Words are written one per line."""
    output = tmp_path / "out.txt"
    save_processed(["cat", "sat", "mat"], str(output))
    content = output.read_text(encoding="utf-8")
    assert content == "cat\nsat\nmat\n"


def test_save_processed_creates_parent_dir(tmp_path):
    """Parent directories are created if they do not exist."""
    output = tmp_path / "nested" / "deep" / "out.txt"
    save_processed(["word"], str(output))
    assert output.exists()


def test_save_processed_empty_list(tmp_path):
    """Empty list creates an empty file (no error)."""
    output = tmp_path / "empty.txt"
    save_processed([], str(output))
    assert output.exists()
    assert output.read_text(encoding="utf-8") == ""