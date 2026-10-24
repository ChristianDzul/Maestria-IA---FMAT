# Amazon Products — Servidor MCP de búsqueda y análisis

Servidor **MCP (Model Context Protocol)** por **HTTP local** que busca y analiza
productos de **Amazon Reviews 2023 · Electronics** usando **embeddings** y
operaciones de **PyTorch**. Trabaja sobre una selección fija de **600 productos y
6 992 reseñas** (entre 5 y 30 reseñas por producto).

La idea central: representamos cada producto como un **vector de 384 dimensiones**
que combina lo que dice el *catálogo* (título + características + descripción) con
lo que dicen sus *reseñas*. Una consulta del usuario se convierte en otro vector y
buscamos los productos más parecidos por **similitud coseno**.

---

## Índice

- [Qué hace](#qué-hace)
- [Arquitectura y flujo](#arquitectura-y-flujo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Las tres herramientas MCP](#las-tres-herramientas-mcp)
- [Explicación por sección](#explicación-por-sección)
  - [Sección 1 · Entorno y estructura](#sección-1--entorno-y-estructura)
  - [Sección 2 · Configuración (`support/settings.py`)](#sección-2--configuración-supportsettingspy)
  - [Sección 3 · Lectura de datos (`support/data.py`)](#sección-3--lectura-de-datos-supportdatapy)
  - [Sección 4 · Embeddings (`support/encoder.py`)](#sección-4--embeddings-supportencoderpy)
- [Cómo recrearlo desde cero](#cómo-recrearlo-desde-cero)
- [Ejecución](#ejecución)
- [Verificación de tipos](#verificación-de-tipos)
- [Ejemplos de consultas e interpretación](#ejemplos-de-consultas-e-interpretación)
- [Limitaciones y alcance de los datos](#limitaciones-y-alcance-de-los-datos)

---

## Qué hace

Expone tres herramientas sobre un servidor MCP accesible en
`http://127.0.0.1:8000/mcp`:

| Herramienta | Qué hace |
|---|---|
| `search_products(query, top_k=5)` | Busca productos por similitud coseno con la consulta. |
| `analyze_product(product_id)` | Resume las valoraciones de un producto (conteos, proporciones, media, mediana). |
| `compare_products(product_ids)` | Compara dos o más productos y sus diferencias de media. |

> Las estadísticas describen **solo las reseñas seleccionadas**, no todas las de
> Amazon. La puntuación de similitud **no** es una probabilidad ni mide la calidad
> del producto.

## Arquitectura y flujo

```
            config.json
                 │
                 ▼
        support/settings.py  ──► valida modelo, batch_size, device
                 │
datasets/*.jsonl.gz          │
                 │           │
                 ▼           ▼
        support/data.py   support/encoder.py
        (lee y prepara    (carga el modelo, codifica catálogo
         textos e IDs)     y reseñas, combina 50/50 → matriz (600, 384))
                 │           │
                 └─────┬─────┘
                       ▼
                   server.py
         (3 herramientas MCP; usa los módulos de support/)
                       │
                       ▼  Streamable HTTP · 127.0.0.1:8000/mcp
                   client.py  ◄── main.py
                 (descubre e invoca las herramientas)
```

Todo se prepara **una sola vez al iniciar el servidor** (datos, modelo y matriz de
vectores) y se mantiene en memoria. El servidor no depende de ejecutar la notebook.

## Estructura del proyecto

```text
amazon-products/
├── README.md            ← este archivo
├── pyproject.toml       ← dependencias y metadatos del proyecto
├── uv.lock              ← versiones exactas (reproducibilidad)
├── .python-version      ← versión de Python (3.13)
├── config.json          ← configuración del modelo de embeddings
├── server.py            ← servidor MCP + las 3 herramientas
├── client.py            ← llamadas de demostración
├── main.py              ← ejecuta el cliente
├── support/
│   ├── __init__.py      ← vacío (marca el paquete)
│   ├── data.py          ← lectura y preparación de datos
│   ├── settings.py      ← carga y validación de configuración
│   └── encoder.py       ← modelo, codificación y vectores de producto
└── datasets/
    ├── products.jsonl.gz
    └── reviews.jsonl.gz
```

## Las tres herramientas MCP

_(Se documentarán en detalle en la Sección 5.)_

## Explicación por sección

### Sección 1 · Entorno y estructura

Creamos un proyecto reproducible con **`uv`** (gestor de entornos y dependencias).

**Dependencias de ejecución:**

- `numpy`, `torch` — operaciones vectoriales.
- `sentence-transformers` — el modelo de embeddings `all-MiniLM-L6-v2`.
- `mcp>=2,<3` — SDK oficial de MCP para Python (servidor y cliente).
- `pydantic` — validación de la configuración.

**Dependencias de desarrollo:** `mypy` (tipos), `pandas`, `matplotlib`,
`ipykernel` (para explorar la notebook).

Los archivos provistos (`config.json`, `datasets/`, la notebook) se copian dentro
de la carpeta del proyecto. La notebook es **solo de referencia**: la aplicación
debe correr sin ejecutarla.

> **Reproducibilidad:** `uv.lock` fija las versiones exactas. Cualquiera puede
> recrear el entorno idéntico con `uv sync --locked`. Al entregar se omiten
> `.venv`, cachés y los pesos del modelo (se descargan solos la primera vez).

### Sección 2 · Configuración (`support/settings.py`)

Lee y valida `config.json` **antes** de arrancar el servidor (principio
*fail-fast*: si la configuración está mal, ningún resultado posterior sería
confiable, así que fallamos de inmediato).

Usamos un modelo de **Pydantic** (`Settings`) que hace de *contrato*:

```python
class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)
    model_name: str = Field(min_length=1)
    batch_size: int = Field(gt=0, strict=True)
    device: Literal["cpu", "cuda", "mps"] = "cpu"
```

Decisiones de diseño y por qué:

| Elemento | Qué hace | Por qué |
|---|---|---|
| `extra="forbid"` | Rechaza claves desconocidas | Caza *typos* en `config.json` (p. ej. `btach_size`) en vez de ignorarlos. |
| `Field(min_length=1)` en `model_name` | Exige nombre no vacío | Requisito del enunciado. |
| `Field(gt=0, strict=True)` en `batch_size` | Entero positivo **real** | `strict` evita que un string `"32"` se convierta solo a int. |
| `Literal[...]` en `device` | Solo acepta `cpu`/`cuda`/`mps` | Evita dispositivos inexistentes. |
| `@field_validator` de `model_name` | `.strip()` + rechaza en blanco | Un nombre de solo espacios no es válido. |
| `@field_validator(..., mode="before")` de `batch_size` | Rechaza booleanos | En Python `True == 1`; sin este guardia un `bool` pasaría como entero. |

El **orden** de validación de `batch_size` es: valor crudo → validador *before*
(caza el `bool`) → conversión + `Field(strict, gt=0)` (caza strings y no positivos).

La función `load_settings(path)` lee el archivo, lo parsea con `json.loads` y
lo valida con `Settings.model_validate(...)`, devolviendo una instancia ya segura.

**Cómo probarlo** (desde `amazon-products/`):

```bash
uv run python -c "from pathlib import Path; from support.settings import load_settings; print(load_settings(Path('config.json')))"
uv run mypy --strict support/settings.py
```

### Sección 3 · Lectura de datos (`support/data.py`)

Adapta las celdas 7 y 19 de la notebook a funciones reutilizables, **sin pandas**
(más limpio y fácil de tipar; pandas queda solo para explorar la notebook). Usa
**generadores** e `Iterator` (lectura bajo demanda) y `with` para los recursos.

Estructuras de datos (reutilizadas de la notebook como `TypedDict`):

- `ReviewRecord`: `review_id`, `product_id`, `text`, `rating`.
- `ProductRecord`: `product_id`, `title`, `features`, `description`, `categories`, `family`.

Funciones del módulo:

| Función | Qué devuelve | Rol |
|---|---|---|
| `rows(path)` | Generador de `(nº_línea, objeto_json)` | Lee `.jsonl.gz` línea a línea, salta líneas en blanco. |
| `load(directory)` | `(records, products)` | Lee ambos archivos y **valida** cada campo (ids, rating en 1–5, no booleanos). |
| `catalog_text(product)` | `str` | Une título + features + description para representar el catálogo. |
| `searchable_reviews(records)` | `(texts, review_ids, review_product_ids)` | Quédate con reseñas de texto no vacío, en **tres listas alineadas**. |

**Invariante crítico:** las tres listas de `searchable_reviews` quedan alineadas
por posición — la fila `i` del embedding corresponde a `texts[i]`, `review_ids[i]`
y `review_product_ids[i]`. Nunca se ordena o filtra una sin las otras. Esto es lo
que, más adelante, permite agrupar los vectores de reseña por producto sin perder
la correspondencia.

**IDs estables:** `review_id = f"Electronics:{source_line}"`, donde `source_line`
es el número de línea en el archivo original de Electronics.

**Cómo probarlo** (desde `amazon-products/`):

```bash
uv run python -c "
from pathlib import Path
from support.data import load, searchable_reviews
records, products = load(Path('datasets'))
print('Reseñas:', len(records), '| Productos:', len(products))
texts, rids, pids = searchable_reviews(records)
print('Textos:', len(texts), '| alineadas:', len(texts)==len(rids)==len(pids))
"
uv run mypy --strict support/data.py
```

Salida esperada: `Reseñas: 6992 | Productos: 600` y `Textos: 6992 | alineadas: True`.

### Sección 4 · Embeddings (`support/encoder.py`)

El corazón del proyecto. Representa cada producto como un **vector de 384
dimensiones** que combina catálogo y reseñas, y lo guarda todo en memoria.

**Qué es un embedding:** un vector que resume el significado de un texto. Dos
textos con sentido parecido producen vectores que apuntan en direcciones
parecidas. Como los normalizamos a longitud 1, la **similitud coseno** se reduce a
un simple **producto escalar** (`a @ b`).

Contenedor en memoria (se construye una sola vez al iniciar el servidor):

```python
@dataclass
class ProductIndex:
    model: SentenceTransformer   # para codificar consultas en cada llamada
    product_ids: list[str]       # alineados con las filas de la matriz
    matrix: torch.Tensor         # (num_productos, 384), filas normalizadas
```

Funciones:

| Función | Rol |
|---|---|
| `load_model(settings)` | Carga `all-MiniLM-L6-v2` (descarga la 1ª vez, luego caché). |
| `encode_texts(model, texts, batch_size)` | Codifica textos → tensor `(N, 384)` **normalizado**. |
| `build_index(...)` | Construye la matriz `(600, 384)` y el `ProductIndex`. |
| `ProductIndex.encode_query(query)` | Codifica una consulta → vector `(384,)`. |

**El cálculo por producto (50 % catálogo + 50 % reseñas):**

1. Vector normalizado del **catálogo** (texto título+features+description).
2. **Promedio** de los vectores de las reseñas de ese producto (`mean(dim=0)`),
   luego **normalizar** ese promedio.
3. **Combinar**: `0.5 · catálogo + 0.5 · reseñas` y **normalizar** el resultado.

```python
review_mean    = review_matrix[idx].mean(dim=0)       # (384,)
review_summary = F.normalize(review_mean, dim=0)      # (384,)
combined       = 0.5 * catalog_matrix[i] + 0.5 * review_summary
product_vectors.append(F.normalize(combined, dim=0))
matrix = torch.stack(product_vectors)                 # (600, 384)
```

**Por qué se normaliza el promedio de reseñas *antes* de combinar:** así ambas
fuentes pesan 50/50 de verdad, sin importar cuántas reseñas tenga el producto ni
cuánto se "cancelen" entre sí. Cada reseña aporta lo mismo; no se pondera por
estrellas ni por cantidad.

**Alineación `positions`:** un dict `product_id → [índices de fila en
review_matrix]`, construido recorriendo `review_product_ids`. Es lo que permite
agrupar las reseñas de cada producto sin perder la correspondencia.

**Tipos:** `encode()` declara un tipo unión, pero con `convert_to_tensor=True` los
*overloads* de la librería ya garantizan `Tensor`, así que no hace falta `cast`.

**Cómo probarlo** (desde `amazon-products/`; la 1ª vez descarga el modelo ~90 MB):

```bash
uv run python -c "
from pathlib import Path
from support.settings import load_settings
from support.data import load, searchable_reviews
from support.encoder import load_model, build_index
import torch
settings = load_settings(Path('config.json'))
records, products = load(Path('datasets'))
texts, rids, pids = searchable_reviews(records)
index = build_index(load_model(settings), settings, products, texts, pids)
print('Matriz:', tuple(index.matrix.shape))
scores = index.matrix @ index.encode_query('A portable waterproof Bluetooth speaker')
for s, i in zip(*torch.topk(scores, 3)):
    print(f'{float(s):.3f}  {products[index.product_ids[int(i)]][\"title\"][:60]}')
"
uv run mypy --strict support/encoder.py
```

## Cómo recrearlo desde cero

```bash
# 1. Crear el proyecto
uv init amazon-products
cd amazon-products

# 2. Añadir dependencias de ejecución
uv add numpy torch sentence-transformers "mcp>=2,<3" pydantic

# 3. Añadir dependencias de desarrollo
uv add --dev mypy pandas matplotlib ipykernel

# 4. Copiar los archivos provistos al proyecto
#    config.json, datasets/, preparacion_datos.ipynb
```

_(Los comandos de ejecución y verificación se completan en secciones siguientes.)_

## Ejecución

_(Se completará en la Sección 6.)_

## Verificación de tipos

_(Se completará en la Sección 7.)_

## Ejemplos de consultas e interpretación

_(Se completará en la Sección 7.)_

## Limitaciones y alcance de los datos

- El modelo `all-MiniLM-L6-v2` está orientado a **inglés** y **trunca** textos de
  más de 256 tokens. Usa consultas en inglés.
- La selección es **por conveniencia, no aleatoria ni representativa**. El límite
  de 30 reseñas por producto impide leer el conteo como popularidad en Amazon.
- Las estrellas no son etiquetas de sentimiento verificadas.
