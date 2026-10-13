# Course Catalog · catálogo de cursos con MCP

**Unidad 1 · Sesión 4 — Organización y reproducibilidad con `uv` y un servidor MCP local.**

Una pequeña aplicación que busca cursos en un catálogo JSON, primero como función
de consola (`main.py`) y luego como **herramienta MCP** (`server.py` + `client.py`).
El objetivo de la práctica es trabajar módulos, dependencias, logging y
reproducción del entorno con `uv`.

---

## Requisitos y ejecución

- [uv](https://docs.astral.sh/uv/) instalado.
- Python 3.13 (lo fija `.python-version`; `uv` lo descarga si hace falta).

```bash
uv sync --locked                       # reconstruye .venv desde uv.lock
uv run --locked python main.py python  # consulta por consola
uv run --locked python client.py python  # consulta vía MCP
```

Atajos del `Makefile`:

```bash
make run        # consulta sin MCP
make client     # llamada MCP
make check      # lint + formato + tipos + pruebas
```

Equivalentes directos de `make check`:

```bash
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy --strict main.py server.py client.py catalog
uv run --locked python -m pytest
```

---

## Estructura

| Ruta | Función |
|---|---|
| `main.py` | App de consola (argparse + logging). |
| `server.py` | Servidor MCP local (expone `find_courses`). |
| `client.py` | Cliente MCP que lanza el servidor y llama la herramienta. |
| `catalog/search.py` | Modelo `Course` (Pydantic) y `search_courses`. |
| `catalog/logging_config.py` | Configura logs a stderr (y archivo opcional). |
| `data/courses.json` | Catálogo de ejemplo (PY01, PY02, ML01). |
| `data/extra_courses.json` | Copia con un curso Python extra (Ejercicio 2). |
| `tests/` | Pruebas existentes (`test_catalog.py`, `test_mcp.py`). |
| `pyproject.toml`, `uv.lock`, `.python-version` | Proyecto, versiones fijadas e intérprete. |
| `Makefile` | Recetas de calidad y ejecución. |

---

## Reproducibilidad

- **`pyproject.toml`**: declara el proyecto, sus dependencias directas (`mcp`, `pydantic`), `requires-python` y la configuración de herramientas (Ruff, pytest).
- **`uv.lock`**: fija las versiones exactas (directas y transitivas) → instalación reproducible.
- **`.python-version`**: intérprete (3.13) con el que `uv` crea el entorno.
- **No se entrega `.venv`**: es local y reconstruible desde el lockfile (`uv sync`); es pesado y específico del sistema operativo.

Comprobación desde cero:

```bash
rm -rf .venv                 # el entorno se regenera
uv sync --locked
uv run --locked python client.py python
```

---

## Ejercicios

### Ejercicio 1 · Punto de entrada  *(PRACTICA.md)*

```bash
uv run python -c "import main"     # no imprime nada (exit=0)
uv run python -c "import server"   # no inicia nada (exit=0)
```

- `import main` **no consulta** el catálogo: importar un módulo ejecuta sus
  definiciones, pero `main()` solo corre bajo `if __name__ == "__main__"`; al
  importar, `__name__ == "main"`, no `"__main__"`.
- En `server.py`, ese **mismo guard** envuelve `mcp.run(transport="stdio")`, así
  que importar el módulo **no inicia** el transporte.
- **Registrar ≠ iniciar**: el decorador `@mcp.tool()` *registra* `find_courses`
  al importar; *iniciar* es `mcp.run(...)`, solo con `python server.py`. Por eso
  pruebas y cliente pueden importar `server` sin levantar un servidor.

### Ejercicio 2 · Datos y argumentos  *(PRACTICA.md)*

```bash
uv run --locked python main.py python --catalog data/extra_courses.json
```
```
INFO | catalog.search | Search completed: 3 matches out of 4 courses
[
  { "code": "PY01", "title": "Python foundations", "hours": 12 },
  { "code": "PY02", "title": "Python for data analysis", "hours": 16 },
  { "code": "PY03", "title": "Python for machine learning", "hours": 18 }
]
```

Ruta inexistente → error controlado con **código 1**:
```
ERROR | __main__ | Catalog search failed
...
FileNotFoundError: [Errno 2] No such file or directory: 'data/nope.json'
exit=1
```

La herramienta MCP **no** usa `--catalog`: `find_courses` llama `search_courses(query)`
con el catálogo predeterminado, por eso `client.py python` sigue devolviendo PY01/PY02.
Un archivo ausente es un **error**, distinto de una búsqueda **sin coincidencias**
(lista vacía, código 0).

### Ejercicio 3 · Niveles y destinos  *(PRACTICA.md)*

```bash
uv run --locked python main.py python --log-level DEBUG
```
```
DEBUG | catalog.search | Reading catalog: .../data/courses.json
INFO  | catalog.search | Search completed: 2 matches out of 3 courses
[ ... PY01, PY02 ... ]
```

Con `--log-level ERROR` la consola no muestra INFO/DEBUG, pero
`--log-file logs/app.log` **sí** los guarda. Motivo: el logger raíz acepta desde
DEBUG; el **handler de consola** filtra por `--log-level`, mientras que el
**handler de archivo** está fijo en DEBUG. Además, `stdout` se reserva al
**protocolo MCP** (stdio): por eso los logs van a **stderr** y el diagnóstico se
hace ahí, nunca con `print` (así `main.py python > result.json` deja el JSON limpio).

### Ejercicio 4 · Mejorar el diagnóstico  *(PRACTICA.md)*

En `catalog/search.py`, el log INFO ahora incluye el total de cursos leídos,
usando **argumentos de logging** (no f-string):
```python
logger.info(
    "Search completed: %d matches out of %d courses",
    len(matches),
    len(courses),
)
```
```
INFO | catalog.search | Search completed: 2 matches out of 3 courses
```

Como el módulo lo usan la consola y la herramienta MCP, el mejor diagnóstico
aplica a ambos caminos y los resultados no cambian (siguen PY01/PY02).

### Ejercicio 5 · Reproducción y llamada MCP  *(PRACTICA.md)*

Desde el entorno reconstruido (`uv sync --locked`):

```bash
uv run --locked python client.py python      # Tools: ['find_courses'] | PY01, PY02 | is_error:false | exit=0
uv run --locked python client.py astronomy   # content: [] | is_error:false | exit=0
uv run --locked python client.py " "         # is_error:true | exit=1
```

`python` (fragmento del sobre MCP):
```json
{
  "content": [
    { "type": "text", "text": "{ \"code\": \"PY01\", ... }" },
    { "type": "text", "text": "{ \"code\": \"PY02\", ... }" }
  ],
  "structured_content": { "result": [ {PY01}, {PY02} ] },
  "is_error": false
}
```

`astronomy` → `"content": []`, `"is_error": false` (éxito, sin coincidencias).
`" "` → `"is_error": true` y código 1 (consulta en blanco → `ValueError` →
`ToolError` en el servidor). Se distingue **respuesta vacía** (válida) de **error**.
La herramienta disponible es **`find_courses`**. El sobre JSON de MCP (con
`content`, `structured_content`, `is_error`) **no** es idéntico al JSON de la app
de consola. Qué aportan `pyproject.toml` / `uv.lock` / `.python-version` y por qué
no se entrega `.venv`: ver la sección **Reproducibilidad**.

### Ejercicio 6 · Corregir un aviso de Ruff  *(CALIDAD.md · calidad #1)*

Al introducir `import os` sin usar en `main.py`, Ruff falla con **F401**:
```
F401 [*] `os` imported but unused
 --> main.py:6:8
  |
5 | import logging
6 | import os
  |        ^^
7 | from pathlib import Path
help: Remove unused import: `os`
Found 1 error.
[*] 1 fixable with `--fix`.
```

Corrección y verificación:
```bash
uv run --locked ruff check --fix .   # elimina el import muerto
uv run --locked ruff check .         # -> All checks passed!
```

La regla `F401` está activa porque `pyproject.toml` incluye `"F"` en el `select`
de Ruff. El linter detecta y elimina imports sin usar automáticamente.

### Ejercicio 7 · Comprobaciones desde una copia limpia  *(CALIDAD.md · calidad #2)*

Tras `uv sync --locked`, las comprobaciones de calidad sobre las **pruebas
existentes**:

```
$ uv run --locked ruff check .
All checks passed!

$ uv run --locked ruff format --check .
11 files already formatted

$ uv run --locked mypy --strict main.py server.py client.py catalog
Success: no issues found in 6 source files

$ uv run --locked python -m pytest
......                                                                   [100%]
6 passed in 6.79s
```

Las 6 pruebas son las existentes (5 de `test_catalog.py` + 1 de `test_mcp.py`,
que arranca un servidor MCP real). `make check` reúne lint, formato, tipos y
pruebas; `.PHONY` evita confundir las tareas con archivos.
