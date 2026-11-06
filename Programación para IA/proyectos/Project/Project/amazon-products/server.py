"""Servidor MCP (Streamable HTTP) con tres herramientas sobre la selección de Amazon.

Al iniciar prepara una vez los datos, el modelo y la matriz de embeddings, y los
deja en memoria. Las herramientas usan los módulos de support/.
"""

from pathlib import Path
from typing import Any

import torch
from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from support.data import load, ratings_by_product, searchable_reviews
from support.encoder import build_index, load_model
from support.settings import load_settings
from support.stats import Summary, summarize

#Preparación al arranque 
CONFIG_PATH = Path("config.json")
DATA_DIR = Path("datasets")

_settings = load_settings(CONFIG_PATH)
_records, _products = load(DATA_DIR)
_texts, _review_ids, _review_product_ids = searchable_reviews(_records)
_model = load_model(_settings)
_index = build_index(_model, _settings, _products, _texts, _review_product_ids)
_ratings = ratings_by_product(_records)  # product_id -> [ratings]

mcp = MCPServer("Amazon reviews")


def _summary_payload(product_id: str, summary: Summary) -> dict[str, Any]:
    """Convierte un Summary en un dict serializable (resuelto, para reutilizar)."""
    return {
        "product_id": product_id,
        "review_count": summary.review_count,
        "counts": summary.counts,
        "proportions": summary.proportions,
        "mean": summary.mean,
        "median": summary.median,
    }


@mcp.tool()
def search_products(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Busca productos por similitud coseno con la consulta.

    Devuelve hasta top_k resultados (id, título, similitud, nº de reseñas),
    en orden descendente de similitud.
    """

    if query.strip() == "":
        raise ToolError("query must not be empty") 
    if not (1 <= top_k <= 20):
        raise ToolError("top_k must be between 1 and 20")
    
    query_vector = _index.encode_query(query)
    scores = _index.matrix @ query_vector

    k = min(top_k, len(_index.product_ids))
    top = torch.topk(scores, k)
    
    results: list[dict[str, Any]] = []
    for score, position in zip(top.values, top.indices):
        product_id = _index.product_ids[int(position)]
        results.append({
            "product_id": product_id,
            "title": _products[product_id]["title"],
            "similarity": float(score),
            "review_count": len(_ratings.get(product_id, [])),
        })
    return results


@mcp.tool()
def analyze_product(product_id: str) -> dict[str, Any]:
    """Resume las valoraciones de un producto.
    """

    if product_id.strip() == "":
        raise ToolError("product_id must not be empty")
    summary = summarize(_ratings.get(product_id, []))

    return _summary_payload(product_id, summary)
    


@mcp.tool()
def compare_products(product_ids: list[str]) -> dict[str, Any]:
    """Compara dos o más productos distintos.

    Devuelve el resumen de cada uno y la diferencia de media respecto al primero.
    Si una media es null, su diferencia también es null.
    """
    #Comprobaciones de validez de la entrada
    
    if len(product_ids) < 2:
        raise ToolError("provide at least two product_ids")

    if any(not pid.strip() for pid in product_ids):
        raise ToolError("product_ids must not be empty")

    if len(set(product_ids)) != len(product_ids):
        raise ToolError("product_ids must be distinct")

    summaries = [summarize(_ratings.get(pid, [])) for pid in product_ids]

    differences: list[dict[str, Any]] = []
    reference_mean = summaries[0].mean
    for pid, s in zip(product_ids, summaries):
        if s.mean is None or reference_mean is None:
            diff = None
        else:
            diff = s.mean - reference_mean
        differences.append({"product_id": pid, "mean_difference": diff})

    return {
        "reference": product_ids[0],
        "products": [_summary_payload(pid, s) for pid, s in zip(product_ids, summaries)],
        "mean_differences": differences,
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
