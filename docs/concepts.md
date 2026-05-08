# Guía de conceptos — Text Analysis Pipeline

Resumen de toda la terminología y conceptos que vimos hasta ahora, agrupados por tema y con ejemplos cortos. Pensado como material de estudio y referencia rápida.

---

## 1. Estructura de proyecto y herramientas

### Virtual environment (`venv`)

Un entorno aislado de Python por proyecto. Las librerías que instalás con `pip` se guardan **adentro** del venv, no a nivel sistema. Así, dos proyectos distintos pueden usar versiones distintas de la misma librería sin pelearse.

```bash
python -m venv venv          # crea la carpeta venv/
source venv/bin/activate     # activa (Linux/Mac)
venv\Scripts\activate        # activa (Windows)
pip install -r requirements.txt
deactivate                   # salir del venv
```

### `requirements.txt`

Lista de dependencias del proyecto, una por línea. Permite que cualquier persona reproduzca tu entorno con `pip install -r requirements.txt`.

### `.gitignore`

Archivo con patrones de rutas que git **debe ignorar**. Sirve para no commitear: el venv, archivos cache (`__pycache__/`), datos crudos (`data/raw/`), salidas generadas (`results/`).

### `.gitkeep`

Convención: un archivo vacío llamado `.gitkeep` dentro de una carpeta vacía sirve para **forzar a git a trackear la carpeta**. Git por defecto no trackea carpetas vacías.

### `git mv`

Versión de `mv` que git "entiende": preserva el historial del archivo. Usalo siempre que renombres o muevas archivos versionados.

```bash
git mv resultados/ results/
```

---

## 2. Imports y organización del archivo

### Orden estándar de un módulo Python

```python
"""Module docstring describing what the module does."""

# 1. Imports — todos juntos, arriba
import logging
import string
from pathlib import Path

# 2. Logger del módulo (si se usa)
logger = logging.getLogger(__name__)

# 3. Constantes (mayúsculas)
STOPWORDS = {"the", "a", "an", ...}

# 4. Funciones / clases
def read_file(path: str) -> str:
    ...
```

### Tipos de import

```python
import logging              # importa el módulo entero, lo usás como logging.getLogger(...)
from pathlib import Path    # importa solo Path, lo usás como Path(...)
import numpy as np          # alias — útil para módulos con nombre largo
```

### Convención de orden de imports

1. **Stdlib** (Python core): `os`, `logging`, `pathlib`, etc.
2. **Third-party** (instalados con pip): `pandas`, `matplotlib`.
3. **Locales** (tu propio código): `from src.cleaning import read_file`.

Una línea en blanco entre cada grupo.

---

## 3. Type hints

Anotaciones que indican qué tipos espera y devuelve una función.

```python
def read_file(path: str) -> str:
    ...

def clean_text(text: str) -> list[str]:
    ...

def save_processed(words: list[str], output_path: str) -> None:
    ...
```

**Importante**: Python **no chequea** los tipos en runtime. Si pasás un `int` donde se espera `str`, no falla solo. Los type hints sirven para:

- Documentar la función (lector humano).
- Que tu IDE te avise (VS Code, PyCharm).
- Que linters como `mypy` los chequeen estáticamente.

### Tipos comunes

| Hint | Significa |
|---|---|
| `str` | string |
| `int` | entero |
| `float` | decimal |
| `bool` | True/False |
| `list[str]` | lista de strings |
| `dict[str, int]` | diccionario con claves string y valores int |
| `tuple[str, int]` | tupla fija (string, int) |
| `None` | nada (para funciones sin return útil) |
| `Path` | objeto pathlib.Path (hay que importarlo) |

---

## 4. Docstrings (estilo Google)

String entre `"""..."""` que describe la función. **Es la primera línea después del `def`**, sin nada en el medio.

```python
def read_file(path: str) -> str:
    """Read a .txt file and return its content as a string.

    Args:
        path: Path to the .txt file to read.

    Returns:
        The file content as a single string.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """
    ...
```

### Secciones del estilo Google

- `Args:` — qué recibe.
- `Returns:` — qué devuelve. Omitir si la función devuelve `None`.
- `Raises:` — qué excepciones puede lanzar.

Si una sección no aplica, **no la escribas vacía**. Solo las relevantes.

---

## 5. Strings y manipulación de texto

### Inmutabilidad

Los strings en Python son **inmutables**: ningún método los modifica, todos devuelven uno nuevo.

```python
text = "Hello"
text.lower()             # devuelve "hello"
print(text)              # sigue siendo "Hello"
text = text.lower()      # ahora sí, reasigno
```

### Métodos clave

```python
"HELLO".lower()                  # "hello"
"hello".upper()                  # "HELLO"
"hello world".split()            # ["hello", "world"]
"a,b,c".split(",")               # ["a", "b", "c"]
"  hello  ".strip()              # "hello"
"...word!!!".strip(".!")         # "word"
"hello, world".replace(",", "")  # "hello world"
"42".isdigit()                   # True
"42.5".isdigit()                 # False
"".strip()                       # ""
not ""                           # True (string vacío es falsy)
```

### `.split()` sin argumentos

Comportamiento especial: divide por **cualquier whitespace** y descarta los strings vacíos.

```python
"hello   world\n\nbye".split()   # ["hello", "world", "bye"]
"".split()                        # [] — no falla, devuelve lista vacía
```

### Method chaining

Encadenar métodos: cada uno opera sobre el resultado del anterior.

```python
text.lower().split()             # primero lower, después split sobre el lower
```

### `string.punctuation`

Constante de la stdlib con todos los signos de puntuación ASCII.

```python
import string
string.punctuation   # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

"hello,!!".strip(string.punctuation)   # "hello"
```

`.strip(chars)` quita los caracteres listados **solo de los extremos**, no del medio. Por eso `"don't"` queda `"don't"`.

---

## 6. Estructuras de datos: list vs set vs dict

| Estructura | Sintaxis | Acceso | Orden | Duplicados |
|---|---|---|---|---|
| `list` | `[1, 2, 3]` | por índice `lista[0]` | preserva | sí |
| `set` | `{1, 2, 3}` | por contenido `1 in s` | no | no |
| `dict` | `{"a": 1, "b": 2}` | por clave `d["a"]` | preserva (3.7+) | claves únicas |

### Por qué `STOPWORDS` es un `set`

La operación más frecuente es **chequear si una palabra está en stopwords**. Eso se llama **lookup** (búsqueda). Importan los costos:

| Estructura | Costo de `x in coleccion` |
|---|---|
| `list` | O(n) — recorre uno por uno |
| `set` | O(1) — busca por hash, instantáneo |

Para 50.000 palabras, la diferencia es enorme.

### Truthiness

Python evalúa como `False` (en contextos booleanos):

- `False`, `None`, `0`, `0.0`
- `""` (string vacío)
- `[]` (lista vacía), `{}` (dict vacío), `set()` (set vacío)

Por eso `if not word:` funciona para detectar string vacío, y `if not words:` para lista vacía.

---

## 7. Archivos: leer y escribir

### `open()` y modos

```python
open(path, "r", encoding="utf-8")    # leer
open(path, "w", encoding="utf-8")    # escribir (SOBREESCRIBE)
open(path, "a", encoding="utf-8")    # append (agrega al final)
```

`encoding="utf-8"` es **obligatorio** en este proyecto: garantiza manejo correcto de acentos, ñ, etc.

### Context manager: `with ... as ...`

Forma idiomática de manejar archivos. Garantiza que el archivo se cierre, **incluso si hay una excepción**.

```python
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
# f ya está cerrado acá
```

Equivalente sin `with`, pero peor (si `read()` falla, el archivo queda abierto):

```python
f = open(path, "r", encoding="utf-8")
content = f.read()
f.close()
```

### Métodos de lectura

```python
f.read()         # devuelve TODO el contenido como un string
f.readlines()    # devuelve una LISTA, una entrada por línea
f.readline()     # devuelve UNA línea por llamada
```

Para textos cortos, `read()` es lo más simple.

### Escribir

```python
f.write("hello")           # escribe sin salto de línea
f.write("hello\n")         # escribe con salto explícito
```

A diferencia de `print()`, `f.write()` **no** agrega `\n` automático.

### `pathlib.Path`

Forma moderna de manejar rutas. Ventajas sobre strings:

```python
from pathlib import Path

p = Path("data/raw/file.txt")
p.exists()                    # True/False
p.is_file()                   # True/False
p.parent                      # Path("data/raw")
p.name                        # "file.txt"
p.stem                        # "file"
p.suffix                      # ".txt"
p.parent.mkdir(parents=True, exist_ok=True)   # crea carpetas
```

Maneja diferencias entre Windows (`\`) y Unix (`/`) automáticamente.

---

## 8. Validación e excepciones

### `raise` vs `try/except`

- **`raise`** — **emitís** una excepción. Va en el código que detecta el problema.
- **`try/except`** — **capturás** una excepción. Va en el código que sabe cómo reaccionar.

```python
# Productor: src/cleaning.py
def read_file(path: str) -> str:
    if not Path(path).exists():
        raise FileNotFoundError(f"File not found: {path}")
    ...

# Consumidor: main.py
try:
    content = read_file("foo.txt")
except FileNotFoundError:
    logger.warning("Archivo no encontrado, salteo")
    content = ""
```

### Excepciones built-in útiles

| Excepción | Cuándo usarla |
|---|---|
| `FileNotFoundError` | archivo/directorio que debería existir, no existe |
| `ValueError` | valor de tipo correcto pero inválido (ej: archivo vacío) |
| `TypeError` | tipo incorrecto (ej: pasaste lista donde se esperaba string) |
| `KeyError` | clave que no existe en un dict |
| `PermissionError` | sin permisos de lectura/escritura |

### Sintaxis de `raise`

```python
raise FileNotFoundError(f"File not found: {path}")   # ✓
raise FileNotFoundError: (f"...")                     # ✗ no va el dos puntos
raise FileNotFoundError "..."                         # ✗ van los paréntesis
```

### Cuándo NO validar

No agregues validaciones "por las dudas". Si un caso raro produce un resultado válido (ej: lista vacía → archivo vacío), eso **no es un error**.

```python
# ❌ innecesario
def save_processed(words: list[str], output_path: str) -> None:
    if not words:
        raise ValueError("No words to save")
    ...

# ✓ deja que el caso natural simplemente pase
def save_processed(words: list[str], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for word in words:
            f.write(word + "\n")
```

### Anti-patrón: silenciar excepciones

```python
try:
    content = read_file(path)
except FileNotFoundError:
    pass   # ❌ se traga el error, después no entendés por qué nada funciona
```

Si no sabés qué hacer con una excepción, **no la captures**.

---

## 9. Control de flujo

### Indentación define bloques

Python usa **indentación** (no llaves) para definir qué código está adentro de qué. Convención: **4 espacios** por nivel.

```python
if condicion:
    hago_esto()       # adentro del if
    y_esto()          # adentro del if
ya_no                 # afuera del if
```

### `if`, `elif`, `else`

```python
if word in STOPWORDS:
    continue
elif word.isdigit():
    continue
else:
    cleaned.append(word)
```

### `for` loop

```python
for token in tokens:
    word = token.strip(string.punctuation)
    cleaned.append(word)
```

### `continue` y `break`

- `continue` → salta a la **siguiente iteración** del loop.
- `break` → **termina** el loop por completo.

### Patrón "filter loop"

```python
result = []
for item in collection:
    if condicion_descartar_1:
        continue
    if condicion_descartar_2:
        continue
    result.append(item)
return result
```

Más legible que anidar varios `if` profundos.

### Posición del `return`

- Una vez ejecutado, la función termina.
- **Cualquier código después de un `return` ejecutado es código muerto**.
- Patrón general:
  1. Validar inputs (raise si fallan).
  2. Hacer el trabajo.
  3. Validar output si corresponde.
  4. `return`.

### Funciones que no devuelven nada

```python
def save_processed(words: list[str], path: str) -> None:
    ...
    # sin return al final
```

`-> None` significa "no hay valor útil que devolver". Python implícitamente devuelve `None`.

---

## 10. Logging

Usar `logging` en vez de `print()` para mensajes de estado. Ventajas: niveles de severidad, configurable globalmente, no se mezcla con la salida real del programa.

### Setup

```python
# main.py — setup global, una sola vez
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# cleaning.py — logger por módulo
import logging
logger = logging.getLogger(__name__)   # __name__ es "src.cleaning"
```

### Niveles

| Nivel | Cuándo usarlo |
|---|---|
| `logger.debug(...)` | información detallada para debug |
| `logger.info(...)` | progreso normal ("Procesando archivo X") |
| `logger.warning(...)` | algo raro pero no fatal ("archivo vacío, salteo") |
| `logger.error(...)` | algo falló ("no se pudo escribir CSV") |
| `logger.critical(...)` | el programa no puede continuar |

---

## 11. Testing con pytest

### Convenciones

- Archivos en carpeta `tests/`, nombre `test_*.py` (literal: empieza con `test_`).
- Funciones de test: `def test_*():`.
- Aserciones con `assert`.

### Estructura básica

```python
# tests/test_cleaning.py
import pytest
from src.cleaning import clean_text, read_file


def test_clean_text_basic():
    result = clean_text("The cat sat on the mat.")
    assert "cat" in result
    assert "the" not in result


def test_clean_text_empty():
    assert clean_text("") == []


def test_read_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_file("nonexistent.txt")
```

### `pytest.raises`

Verifica que un bloque de código lanza una excepción específica.

```python
with pytest.raises(ValueError):
    funcion_que_debe_fallar()
```

Si **no lanza** la excepción esperada, el test falla.

### Ejecutar

```bash
pytest tests/ -v       # -v = verbose, muestra cada test por nombre
pytest tests/test_cleaning.py   # solo un archivo
pytest -k "empty"      # solo los tests cuyo nombre contiene "empty"
```

### Producción vs test

- **Producción** (`src/`): implementa lógica, valida con `raise`.
- **Tests** (`tests/`): llama a la lógica con inputs conocidos y verifica resultados.
- Los `raise` viven en producción, no en tests. Los tests **provocan** las condiciones de error y verifican que el `raise` ocurra.

---

## 12. Feedback loops (cómo saber si tu código funciona)

De más rápido a más completo:

### a. Resaltado del editor

VS Code subraya errores en rojo **mientras tipeás**. Hovereá con el mouse para ver el mensaje. Los subrayados rojos casi siempre son bugs reales.

### b. Chequeo de sintaxis

```bash
python -c "import src.cleaning"
```

Importa el módulo. Si hay error de sintaxis, lo dice con número de línea. Sin output = OK sintácticamente. Es un comando de **terminal**, no código.

### c. Tests de comportamiento

```bash
pytest tests/ -v
```

Verifica que el código hace lo que debe.

### d. Linting

```bash
flake8 src/ tests/ main.py --max-line-length 88
```

Encuentra problemas de estilo (líneas largas, imports sin usar, etc.).

### e. Formateo automático

```bash
black src/ tests/ main.py
```

Reformatea el código a un estilo consistente. No cambia comportamiento.

---

## 13. Git workflow

### Comandos básicos

```bash
git status                    # qué cambió
git diff                      # qué cambió, en detalle
git diff --staged             # qué hay en staged
git add archivo.py            # marca para commitear
git commit -m "mensaje"       # crea el commit
git log --oneline             # historial reciente
git push -u origin <branch>   # subir al remoto
git fetch origin              # bajar cambios del remoto sin mergear
git pull origin <branch>      # bajar y mergear
```

### Mensajes de commit

- Modo imperativo presente: "add X", "fix Y", no "added" ni "adding".
- Concisos pero descriptivos.
- Si hace falta más contexto, agregá un párrafo después de una línea en blanco.

```
add text cleaning module with stopword removal

Implements read_file, clean_text, save_processed.
Includes input validation and unit tests.
```

### Branches

- Una branch por feature/módulo.
- No comitear directo a `main` en proyectos compartidos.
- Renombrar archivos: usar `git mv` para preservar historial.

---

## 14. Convenciones generales del proyecto

- **Identificadores en inglés**: archivos, funciones, parámetros, variables, columnas de DataFrame. Conversación en español, código en inglés.
- **`encoding="utf-8"`** en todas las operaciones de archivo.
- **Type hints** en todas las firmas de funciones.
- **Docstrings Google** en todas las funciones.
- **`logging`** en vez de `print` para mensajes de estado.
- **`pathlib.Path`** en vez de strings crudos para rutas.
- **PEP 8** + `black` (max-line-length 88).
- **Sin estado global mutable** — todo pasa por argumentos.

---

## 15. Cómo se conectan las piezas

```
┌──────────────────────────────────────────────────────────┐
│                       main.py                            │
│  argparse + logging.basicConfig                          │
│  try/except (consume excepciones de los módulos)         │
└──────────────────────────────────────────────────────────┘
                   │ llama a
                   ▼
┌──────────────────────────────────────────────────────────┐
│  src/cleaning.py    src/frequency.py    src/concepts.py  │
│  ─ funciones puras                                       │
│  ─ raise excepciones cuando algo es inválido             │
│  ─ usan pathlib, logging, type hints, docstrings         │
└──────────────────────────────────────────────────────────┘
                   ▲ verifica
                   │
┌──────────────────────────────────────────────────────────┐
│  tests/test_cleaning.py    tests/test_frequency.py ...   │
│  ─ importan funciones de src/                            │
│  ─ assert sobre outputs esperados                        │
│  ─ pytest.raises para verificar excepciones              │
└──────────────────────────────────────────────────────────┘
```

El **flujo de datos** del proyecto:

```
data/raw/*.txt
   │
   ▼  read_file()
texto crudo (str)
   │
   ▼  clean_text()
list[str] de palabras limpias
   │
   ├──▶ save_processed() ──▶ data/processed/
   │
   ├──▶ count_frequency() ──▶ dict ──▶ frequency_to_dataframe() ──▶ DataFrame ──▶ export_csv() ──▶ results/tables/
   │
   ├──▶ count_by_category(words, concepts) ──▶ dict ──▶ plot_categories() ──▶ results/charts/
   │
   └──▶ find_context(words, term) ──▶ list[str] ──▶ kwic_to_dataframe() ──▶ DataFrame
```

---

## Glosario rápido

| Término | Significado |
|---|---|
| **Argument / parameter** | valor que recibe una función |
| **Built-in** | algo incluido en Python sin imports (`len`, `print`, `str`, etc.) |
| **Callable** | algo que se puede llamar con `()` (función, clase, etc.) |
| **CLI** | Command-Line Interface, programa que se usa por terminal |
| **Context manager** | objeto usable con `with`, gestiona setup/teardown |
| **Docstring** | string de documentación al inicio de una función/clase/módulo |
| **Edge case** | caso límite/inusual que un test debe cubrir |
| **Encoding** | cómo se codifican los caracteres en bytes (UTF-8 estándar) |
| **Exception** | objeto que representa un error, se lanza con `raise` |
| **Falsy / Truthy** | valor que se evalúa como False/True en contextos booleanos |
| **Filter loop** | patrón `for + continue + append` para filtrar |
| **Glob pattern** | patrón con comodines como `test_*.py` |
| **Hashable** | objeto cuyo hash es estable (clave de dict, elemento de set) |
| **Idempotente** | operación que repetida da el mismo resultado |
| **Immutable** | que no se puede modificar después de creado (str, tuple, frozenset) |
| **KWIC** | Key Word In Context, técnica de lingüística de corpus |
| **Lookup** | búsqueda de un valor en una colección |
| **Method chaining** | encadenar llamadas: `a.b().c().d()` |
| **Module** | un archivo `.py` |
| **Mutable** | que se puede modificar (list, dict, set) |
| **PEP 8** | guía oficial de estilo para Python |
| **Refactor** | cambiar la estructura sin cambiar el comportamiento |
| **Scope** | región donde una variable es accesible |
| **Stdlib** | standard library, módulos incluidos con Python |
| **Stopword** | palabra muy común que se filtra en NLP (the, of, a, ...) |
| **Tokenizar** | dividir texto en unidades (típicamente palabras) |
| **Type hint** | anotación del tipo esperado en una firma |
| **Whitespace** | espacios, tabs, saltos de línea |

---

## Próximos conceptos (los vamos a ver pronto)

- **`pandas.DataFrame`**: tabla 2D con columnas tipadas. Step 2.
- **`json` module**: leer/escribir archivos JSON. Step 3.
- **`argparse`**: parsear argumentos de línea de comandos. Step 6.
- **`matplotlib`**: graficar. Step 5.
- **List/dict comprehensions**: alternativa compacta a los for loops.
- **f-strings con formato**: `f"{valor:.2f}"`, `f"{valor:>10}"`.
