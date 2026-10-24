"""Lectura y preparación de los datos de la selección de Amazon.

Adapta las celdas 7 y 19 de la notebook preparacion_datos.ipynb a funciones
reutilizables por el servidor, sin depender de pandas ni de ejecutar la notebook.

Conceptos de clase usados aquí:
- Generadores / Iterator y lectura bajo demanda (u1_n4_iteracion).
- Manejo de recursos con `with` (gzip.open).
"""

import gzip
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any, TypedDict


class ReviewRecord(TypedDict):
    """Una reseña ya validada y lista para la aplicación."""

    review_id: str
    product_id: str
    text: str
    rating: float


class ProductRecord(TypedDict):
    """Un producto del catálogo con los campos que usaremos."""

    product_id: str
    title: str
    features: list[str]
    description: list[str]
    categories: list[str]
    family: str


def rows(path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    """Lee un .jsonl.gz línea por línea (bajo demanda).

    Devuelve (numero_de_linea, objeto_json) saltando líneas en blanco.
    Patrón de la celda 5 de la notebook.
    """
    # TODO (1):
    #   - Abre el archivo con: gzip.open(path, "rt", encoding="utf-8") dentro de `with`.
    #   - Enumera las líneas empezando en 1 (enumerate(stream, start=1)).
    #   - Si la línea no está en blanco (text.strip()), haz: yield line_number, json.loads(text)
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line_number, text in enumerate(stream, start=1):
            if text.strip(): # si la línea no está en blanco
                yield line_number, json.loads(text)
    


def load(directory: Path) -> tuple[list[ReviewRecord], dict[str, ProductRecord]]:
    """Lee productos y reseñas desde `directory` y los valida.

    Devuelve (lista_de_reseñas, dict_de_productos_por_id).
    Es una adaptación directa de la celda 7 de la notebook: cópiala y ajústala.

    Reglas clave que ya trae la notebook (consérvalas):
      - product_id debe ser str no vacío; título debe ser str.
      - rating debe estar en (1,2,3,4,5) y no ser bool.
      - review_id estable = f"Electronics:{source_line}".
      - features/description/categories: listas de str (vacías se permiten).
    """
    # TODO (2): Copia aquí el cuerpo de la función `load` de la celda 7 de la
    #           notebook (la que construye `products` y luego `records`).
    #           No cambies su lógica de validación ni el formato del review_id.
    products: dict[str, ProductRecord] = {}
    for line_number, product in rows(directory / "products.jsonl.gz"):
        product_id = product.get("parent_asin")
        title = product.get("title") or ""
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError(f"Invalid product ID at line {line_number}")
        if not isinstance(title, str):
            raise ValueError(f"Invalid product title at line {line_number}")
        if product_id in products:
            raise ValueError(f"Duplicate product ID at line {line_number}")
        features = product.get("features") or []
        if not isinstance(features, list) or any(not isinstance(item, str) for item in features):
            raise ValueError(f"Invalid features at line {line_number}")
        description = product.get("description") or []
        categories = product.get("categories") or []
        family = product.get("family")
        for values in (description, categories):
            if not isinstance(values, list) or any(not isinstance(item, str) for item in values):
                raise ValueError(f"Invalid catalog text at line {line_number}")
        if not isinstance(family, str) or not family:
            raise ValueError(f"Invalid family at line {line_number}")
        products[product_id] = {
            "product_id": product_id, "title": title, "features": features,
            "description": description, "categories": categories, "family": family,
        }

    records: list[ReviewRecord] = []
    for line_number, review in rows(directory / "reviews.jsonl.gz"):
        product_id = review.get("parent_asin")
        rating = review.get("rating")
        text = review.get("text") or ""
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError(f"Invalid product ID at review line {line_number}")
        if isinstance(rating, bool) or not isinstance(rating, (int, float)):
            raise ValueError(f"Invalid rating at review line {line_number}")
        if rating not in (1, 2, 3, 4, 5) or not isinstance(text, str):
            raise ValueError(f"Invalid review at line {line_number}")
        source_line = review.get("source_line")
        if isinstance(source_line, bool) or not isinstance(source_line, int) or source_line < 1:
            raise ValueError(f"Invalid original line at review line {line_number}")
        records.append({
            "review_id": f"Electronics:{source_line}",
            "product_id": product_id,
            "text": text,
            "rating": float(rating),
        })
    return records, products



def catalog_text(product: ProductRecord) -> str:
    """Construye el texto de catálogo de un producto: título + features + description.

    Une cada lista con ' '.join(...); una lista vacía aporta cadena vacía.
    Patrón de la celda 9 de la notebook (columna catalog_text), pero por producto.
    """
    # TODO (3):
    #   - Toma product["title"] (ya es str), y une features y description con " ".join(...).
    #   - Concaténalos con espacios y aplica .strip() al resultado final.
    #   - Devuelve ese string.
    title = product["title"]
    features = " ".join(product["features"])
    description = " ".join(product["description"])
    return f"{title} {features} {description}".strip()



def searchable_reviews(
    records: list[ReviewRecord],
) -> tuple[list[str], list[str], list[str]]:
    """Selecciona las reseñas con texto no vacío y devuelve TRES listas alineadas.

    Returns:
        (texts, review_ids, review_product_ids), donde la posición i de las tres
        corresponde a la misma reseña. Adaptación de la celda 19 de la notebook.
    """
    # TODO (4):
    #   - Recorre `records`.
    #   - Para cada reseña cuyo texto, tras .strip(), NO esté vacío:
    #       añade el texto limpio a `texts`,
    #       su review_id a `review_ids`,
    #       su product_id a `review_product_ids`.
    #   - Devuelve las tres listas EN EL MISMO ORDEN (alineadas por posición).
    selected_texts: list[str] = []
    selected_review_ids: list[str] = []
    selected_product_ids: list[str] = []
    for record in records:
        text = record["text"].strip()
        if text:  # si el texto no está vacío
            selected_texts.append(text)
            selected_review_ids.append(record["review_id"])
            selected_product_ids.append(record["product_id"])
    return selected_texts, selected_review_ids, selected_product_ids


def ratings_by_product(records: list[ReviewRecord]) -> dict[str, list[float]]:
    """Agrupa las valoraciones (rating) de cada producto.

    Returns:
        dict product_id -> lista de ratings (floats) de sus reseñas seleccionadas.
        Lo usarán analyze_product y compare_products para las estadísticas, y
        search_products para contar cuántas reseñas tiene cada producto.
    """
    # TODO (5):
    #   - Crea un dict vacío: ratings: dict[str, list[float]] = {}.
    #   - Recorre `records`; para cada uno añade su "rating" a la lista de su
    #     "product_id" usando ratings.setdefault(product_id, []).append(rating).
    #   - Devuelve el dict.
    ...  # TODO

