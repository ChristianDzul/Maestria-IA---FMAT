"""Lectura y preparación de los datos de la selección de Amazon.
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
    """Producto del catálogo con campos a usar en la aplicación."""

    product_id: str
    title: str
    features: list[str]
    description: list[str]
    categories: list[str]
    family: str


def rows(path: Path) -> Iterator[tuple[int, dict[str, Any]]]:
    """Lee un .jsonl.gz línea por línea (bajo demanda).

    Devuelve (numero_de_linea, objeto_json) saltando líneas en blanco.
    """
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line_number, text in enumerate(stream, start=1):
            if text.strip(): # si la línea no está en blanco
                yield line_number, json.loads(text)
    


def load(directory: Path) -> tuple[list[ReviewRecord], dict[str, ProductRecord]]:
    """Lee productos y reseñas desde `directory` y los valida.
    """
    
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
    """

    title = product["title"]
    features = " ".join(product["features"])
    description = " ".join(product["description"])
    return f"{title} {features} {description}".strip()



def searchable_reviews(
    records: list[ReviewRecord],
) -> tuple[list[str], list[str], list[str]]:
    """Selecciona las reseñas con texto no vacío y devuelve tres listas alineadas.
    """
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
    """
    ratings: dict[str, list[float]] = {}
    for record in records:
        product_id = record["product_id"]
        rating = record["rating"]
        ratings.setdefault(product_id, []).append(rating)
    return ratings
