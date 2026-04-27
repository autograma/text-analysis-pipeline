# CLAUDE.md — Text Analysis Pipeline

## Collaboration mode

The developer is a junior Python programmer building their first portfolio project. They have solid fundamentals (functions, dictionaries, lists, files, Pandas, basic matplotlib) but many professional tools and patterns will be new to them (pytest, argparse, logging, virtual environments, linting, etc.).

**How to work together:**

- Do NOT silently generate code the developer won't understand. When introducing a new concept, tool, or pattern for the first time, explain *what* it does and *why* it's used — briefly, not a lecture.
- Prefer guiding over doing. When possible, describe the approach and let the developer attempt it. Offer to write it if they ask.
- If the developer's code works but isn't idiomatic, show the improvement and explain the difference.
- One module at a time. Don't build ahead; follow the development order below.

---

## Project overview

Python CLI tool that analyzes a corpus of `.txt` files to extract word frequencies, track thematic concepts, show keyword-in-context (KWIC), and visualize results. Initially applied to philosophical texts (David Pearce's abolitionist project), but designed to work with **any** text corpus.

## Tech stack

- Python 3.10+
- pandas (DataFrames, CSV/Excel export)
- matplotlib (charts)
- pytest (testing)
- json (config loading)
- argparse (CLI interface)
- logging (status messages)
- No external NLP libraries (no NLTK, no spaCy). All text processing is manual.

## Repository structure

```
text-analysis-pipeline/
├── CLAUDE.md                  # these instructions
├── README.md
├── requirements.txt           # pandas, matplotlib, pytest
├── .gitignore
├── config/
│   └── conceptos_clave.json   # concept categories + terms (editable by user)
├── data/
│   ├── raw/                   # input .txt files
│   └── processed/             # cleaned text output
├── src/
│   ├── __init__.py
│   ├── limpieza.py            # text cleaning
│   ├── frecuencia.py          # word frequency analysis
│   ├── conceptos.py           # concept tracking by category
│   ├── kwic.py                # Key Word In Context extraction
│   └── visualizacion.py       # matplotlib charts
├── tests/
│   ├── __init__.py
│   ├── test_limpieza.py
│   ├── test_frecuencia.py
│   ├── test_conceptos.py
│   └── test_kwic.py
├── resultados/
│   ├── tablas/                # exported CSVs
│   └── graficos/              # exported PNGs
└── main.py                    # CLI entry point, orchestrates full pipeline
```

## Setup

### Virtual environment

The project uses a virtual environment to isolate dependencies:

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### requirements.txt

```
pandas>=2.0
matplotlib>=3.7
pytest>=7.0
```

### .gitignore

```
venv/
__pycache__/
*.pyc
data/raw/*
!data/raw/.gitkeep
resultados/tablas/*
!resultados/tablas/.gitkeep
resultados/graficos/*
!resultados/graficos/.gitkeep
.pytest_cache/
```

Keep `.gitkeep` files in empty directories so Git preserves the folder structure.

---

## Module specifications

### 1. `src/limpieza.py`

Functions:

- `leer_archivo(ruta: str) -> str` — reads a .txt file, returns content as string
- `limpiar_texto(texto: str) -> list[str]` — lowercases, strips punctuation, removes stopwords, returns list of clean words
- `guardar_procesado(palabras: list[str], ruta_salida: str) -> None` — writes cleaned words to file

Stopwords: define a `STOPWORDS` set at module level with common English stopwords (the, a, an, is, are, was, were, of, in, to, for, on, with, at, by, from, and, or, but, not, it, this, that, etc.). No external dependency.

Punctuation removal: strip characters in `string.punctuation` from each word. Discard empty strings and tokens that are purely numeric.

**Input validation:**

- `leer_archivo` must raise `FileNotFoundError` with a clear message if the file doesn't exist
- `leer_archivo` must raise `ValueError` if the file is empty
- `limpiar_texto` must handle edge cases: empty string input, strings with only punctuation, strings with only stopwords

### 2. `src/frecuencia.py`

Functions:

- `contar_frecuencia(palabras: list[str]) -> dict[str, int]` — builds {word: count} dictionary using the `if key not in dict` / `+= 1` pattern
- `frecuencia_a_dataframe(freq_dict: dict) -> pd.DataFrame` — converts to DataFrame with columns ['palabra', 'frecuencia'], sorted descending
- `exportar_csv(df: pd.DataFrame, ruta: str) -> None` — saves DataFrame to CSV

**Input validation:**

- `contar_frecuencia` must return empty dict for empty list input
- `exportar_csv` must create parent directories if they don't exist

### 3. `src/conceptos.py`

Functions:

- `cargar_conceptos(ruta_json: str) -> dict[str, list[str]]` — loads concept categories from JSON config
- `contar_por_categoria(palabras: list[str], conceptos: dict) -> dict[str, int]` — total count per category
- `detalle_por_termino(palabras: list[str], conceptos: dict) -> dict[str, dict[str, int]]` — count per term within each category

Config format (`config/conceptos_clave.json`):

```json
{
    "hedonic": ["hedonic", "well-being", "happiness", "pleasure", "bliss"],
    "suffering": ["suffering", "pain", "malaise", "agony", "distress"],
    "biotech": ["biotechnology", "genetic", "crispr", "genome", "engineering"],
    "ethics": ["ethics", "moral", "utilitarian", "consequentialism", "rights"],
    "consciousness": ["consciousness", "qualia", "sentience", "awareness", "phenomenal"]
}
```

Ship this default config file with the project.

**Input validation:**

- `cargar_conceptos` must raise `FileNotFoundError` if JSON doesn't exist
- `cargar_conceptos` must raise `ValueError` if JSON is malformed (wrap `json.load` in try/except for `json.JSONDecodeError`)
- `cargar_conceptos` must validate that every value is a list of strings

### 4. `src/kwic.py`

Functions:

- `buscar_contexto(palabras: list[str], termino: str, ventana: int = 5) -> list[str]` — finds all occurrences of `termino`, returns list of context strings (N words before + highlighted term + N words after)
- `kwic_a_dataframe(contextos: list[str], termino: str) -> pd.DataFrame` — DataFrame with columns ['termino', 'contexto', 'aparicion_num']

Context format: `"...the abolition of | suffering | in all sentient..."` (pipe-separated highlighting)

**Input validation:**

- Return empty list if term is not found (not an error)
- Handle edge cases: term at very beginning or very end of text (window is truncated, not errored)

### 5. `src/visualizacion.py`

Functions:

- `graficar_top_palabras(df_freq: pd.DataFrame, n: int = 20, ruta_salida: str = None) -> None` — horizontal bar chart, top N words
- `graficar_categorias(dict_categorias: dict, titulo: str = '', ruta_salida: str = None) -> None` — bar chart of concept category frequencies
- `graficar_comparacion(datos_por_texto: dict[str, dict], categoria: str, ruta_salida: str = None) -> None` — grouped bar chart comparing one category across multiple texts

All charts: save to `resultados/graficos/` as PNG. Use `plt.tight_layout()`. Close figure after saving with `plt.close()`.

**Input validation:**

- If DataFrame is empty or dict has no data, log a warning and skip chart generation (don't crash)

### 6. `main.py` — CLI entry point

Use `argparse` to accept command-line arguments:

```
python main.py --input data/raw/ --config config/conceptos_clave.json --top 20 --kwic-terms suffering,hedonic --output resultados/
```

Arguments:

- `--input` (required): path to directory with .txt files
- `--config` (optional, default: `config/conceptos_clave.json`): path to concepts JSON
- `--top` (optional, default: 20): how many top words to display/chart
- `--kwic-terms` (optional): comma-separated terms for KWIC analysis
- `--output` (optional, default: `resultados/`): output directory

Pipeline steps:

1. Validate inputs (directory exists, has .txt files, config is valid)
2. For each .txt file: clean → frequency → concepts → KWIC
3. Aggregate results across files
4. Generate visualizations
5. Export tables to CSV
6. Print summary to console

Include `if __name__ == '__main__':` guard.

---

## Logging

Use Python's `logging` module instead of `print()` for all status messages.

Setup in `main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

In each module, create a module-level logger:

```python
import logging
logger = logging.getLogger(__name__)
```

Use `logger.info()` for progress updates, `logger.warning()` for non-fatal issues (e.g., empty file skipped), and `logger.error()` for failures.

---

## Testing

Use pytest. Each module gets a corresponding test file in `tests/`.

### Test strategy

- Test with small, predictable inputs where the expected output can be verified manually
- Test edge cases: empty inputs, missing files, malformed data
- Test that validation errors raise the correct exceptions

### Example test structure (`tests/test_limpieza.py`):

```python
import pytest
from src.limpieza import limpiar_texto, leer_archivo


def test_limpiar_texto_basico():
    resultado = limpiar_texto("The cat sat on the mat.")
    assert "cat" in resultado
    assert "sat" in resultado
    assert "the" not in resultado  # stopword removed


def test_limpiar_texto_vacio():
    resultado = limpiar_texto("")
    assert resultado == []


def test_limpiar_texto_solo_puntuacion():
    resultado = limpiar_texto("... !!! ???")
    assert resultado == []


def test_leer_archivo_no_existe():
    with pytest.raises(FileNotFoundError):
        leer_archivo("archivo_que_no_existe.txt")
```

### Running tests:

```bash
pytest tests/ -v
```

---

## Code standards

- All functions must have docstrings (Google style)
- Type hints on all function signatures
- PEP 8 compliant
- Descriptive variable names (no single letters except loop counters)
- Use `encoding='utf-8'` on all file operations
- No global mutable state; pass data through function arguments
- Use `logging` for status messages, never bare `print()` (except in final console summary)
- Validate inputs at function boundaries: check types, check file existence, check for empty data
- Use `pathlib.Path` for file path manipulation when practical

## Linting

Format code with `black` before committing:

```bash
pip install black
black src/ tests/ main.py
```

Check style with `flake8`:

```bash
pip install flake8
flake8 src/ tests/ main.py --max-line-length 88
```

The `--max-line-length 88` matches black's default.

---

## README.md requirements

Include:

1. Project title and one-line description
2. What it does (3-4 bullet points)
3. Installation instructions (venv + pip install)
4. Usage: CLI arguments with examples
5. How to customize `conceptos_clave.json`
6. Example output: paste a sample frequency table and a chart screenshot
7. Project structure (tree view)
8. How to run tests (`pytest tests/ -v`)
9. License (MIT)

---

## Development order

Build and test each module independently before integrating in main.py:

| Step | Task                                                        | Test                  |
| ---- | ----------------------------------------------------------- | --------------------- |
| 0    | Setup: venv, .gitignore, requirements.txt, folder structure | manual                |
| 1    | limpieza.py                                                 | test_limpieza.py      |
| 2    | frecuencia.py                                               | test_frecuencia.py    |
| 3    | conceptos.py + conceptos_clave.json                         | test_conceptos.py     |
| 4    | kwic.py                                                     | test_kwic.py          |
| 5    | visualizacion.py                                            | manual (visual check) |
| 6    | main.py with argparse + logging                             | manual (end-to-end)   |
| 7    | README.md                                                   | —                     |
| 8    | Final: black + flake8 pass, all tests green                 | `pytest tests/ -v`    |

---

## Git workflow

- One commit per module with descriptive message (e.g., "add text cleaning module with stopword removal")
- Do not commit data/raw/ contents (add to .gitignore)
- Do commit config/conceptos_clave.json and one sample output
- Run `black` and `pytest` before each commit
- Use present tense imperative in commit messages ("add", "fix", "update", not "added" or "adding")
