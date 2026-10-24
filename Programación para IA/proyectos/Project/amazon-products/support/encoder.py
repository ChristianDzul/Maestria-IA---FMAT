"""Modelo de embeddings y construcción de los vectores de producto.

Combina catálogo y reseñas en un vector por producto (50 % de cada fuente) y
los reúne en una matriz (num_productos, 384). Operaciones de PyTorch como en la
notebook u2_n4 (sección 6): F.normalize, mean(dim=0), producto escalar.

El modelo y la matriz se construyen UNA vez al iniciar el servidor y se mantienen
en memoria (ProductIndex).
"""

from dataclasses import dataclass

import torch
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer

from support.data import ProductRecord, catalog_text
from support.settings import Settings


@dataclass
class ProductIndex:
    """Todo lo que el servidor necesita en memoria para buscar.

    - model: para codificar las consultas en cada llamada.
    - product_ids: IDs en el MISMO orden que las filas de `matrix`.
    - matrix: vectores de producto normalizados, forma (num_productos, 384).
    """

    model: SentenceTransformer
    product_ids: list[str]
    matrix: torch.Tensor

    def encode_query(self, query: str) -> torch.Tensor:
        """Codifica una consulta y devuelve su vector normalizado de forma (384,)."""
        # TODO (4): usa encode_texts(self.model, [query], batch_size=1) para obtener
        #           un tensor (1, 384) y devuelve la fila 0 → [0] → forma (384,).
        encoded = encode_texts(self.model, [query], batch_size=1)  # (1, 384)
        return encoded[0]
        ...  # TODO


def load_model(settings: Settings) -> SentenceTransformer:
    """Carga el modelo de sentence-transformers indicado en la configuración.

    La primera vez descarga el modelo; luego usa la caché local.
    (Resuelto: es boilerplate.)
    """
    return SentenceTransformer(settings.model_name, device=settings.device)


def encode_texts(
    model: SentenceTransformer, texts: list[str], batch_size: int
) -> torch.Tensor:
    """Codifica una lista de textos a un tensor (N, 384) ya normalizado.

    (Resuelto: muestra el patrón de encode + el cast que mypy necesita.)
    normalize_embeddings=True deja cada vector de longitud 1, lo que permite
    calcular la similitud coseno con un simple producto escalar.
    """
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    # encode() declara un tipo unión; con convert_to_tensor=True siempre es Tensor.
    return embeddings

def build_index(
    model: SentenceTransformer,
    settings: Settings,
    products: dict[str, ProductRecord],
    review_texts: list[str],
    review_product_ids: list[str],
) -> ProductIndex:
    """Construye la matriz de productos combinando catálogo y reseñas (50/50).

    Pasos (GUIA §3):
      1. Vector normalizado del catálogo (por producto).
      2. Promedio de los vectores de reseña de ese producto, luego normalizar.
      3. Combinar 0.5*catálogo + 0.5*reseñas y normalizar el resultado.
    """
    # product_ids define el ORDEN de las filas de la matriz. Lo fijamos una vez.
    product_ids = list(products.keys())

    # --- Catálogo: un texto por producto, en el orden de product_ids ---
    catalog_texts = [catalog_text(products[pid]) for pid in product_ids]
    catalog_matrix = encode_texts(model, catalog_texts, settings.batch_size)  # (P, 384)

    # --- Reseñas: todas de golpe, alineadas con review_product_ids ---
    review_matrix = encode_texts(model, review_texts, settings.batch_size)  # (R, 384)

    # TODO (1): construye `positions`, un dict product_id -> lista de índices de fila
    #           en review_matrix que pertenecen a ese producto.
    #   Recorre review_product_ids con enumerate y usa positions.setdefault(pid, []).append(i).
    positions: dict[str, list[int]] = {}
    for i, product_id in enumerate(review_product_ids):
        positions.setdefault(product_id, []).append(i)
    # ...  # TODO

    # TODO (2): recorre product_ids (con enumerate para tener i = fila del catálogo)
    #           y por cada producto:
    #   a) idx = positions[pid]                      (índices de sus reseñas)
    #   b) review_mean = review_matrix[idx].mean(dim=0)       -> (384,)
    #   c) review_summary = F.normalize(review_mean, dim=0)   -> (384,)
    #   d) combined = 0.5 * catalog_matrix[i] + 0.5 * review_summary
    #   e) añade F.normalize(combined, dim=0) a la lista product_vectors
    product_vectors: list[torch.Tensor] = []
    for i, product_id in enumerate(product_ids):
        idx = positions.get(product_id, [])
        if idx:
            review_mean = review_matrix[idx].mean(dim=0)
            review_summary = F.normalize(review_mean, dim=0)
        else:
            review_summary = torch.zeros(384, device=settings.device)  # Si no hay reseñas
        combined = 0.5 * catalog_matrix[i] + 0.5 * review_summary
        product_vectors.append(F.normalize(combined, dim=0))
        
    # ...  # TODO

    # TODO (3): apila la lista en un solo tensor (P, 384) con torch.stack(product_vectors)
    matrix = torch.stack(product_vectors)  # (P, 384)
    
    return ProductIndex(model=model, product_ids=product_ids, matrix=matrix)
