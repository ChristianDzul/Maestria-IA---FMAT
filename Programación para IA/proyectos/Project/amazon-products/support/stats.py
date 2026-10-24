"""Estadísticas de las valoraciones (ratings) de un producto, con PyTorch.

Describe SOLO las reseñas seleccionadas de la muestra, no todas las de Amazon.
Reutilizado por analyze_product y compare_products en server.py.
"""

from dataclasses import dataclass

import torch

# Las cinco estrellas posibles, en orden. Las usamos para conteos y proporciones.
STARS: tuple[int, int, int, int, int] = (1, 2, 3, 4, 5)


@dataclass
class Summary:
    """Resumen de las valoraciones de un producto.

    - review_count: cuántas reseñas (seleccionadas) tiene.
    - counts: conteo por estrella {1: n1, ..., 5: n5}.
    - proportions: proporción por estrella {1: p1, ..., 5: p5} (suman ~1 si hay reseñas).
    - mean / median: media y mediana; None si no hay reseñas.
    """

    review_count: int
    counts: dict[int, int]
    proportions: dict[int, float]
    mean: float | None
    median: float | None


def summarize(ratings: list[float]) -> Summary:
    """Calcula el resumen estadístico de una lista de ratings.

    Si la lista está vacía (p. ej. producto desconocido): review_count 0,
    conteos y proporciones en 0, y mean/median None.

    Todos los valores devueltos deben ser tipos de Python (int, float, None),
    no tensores: usa int(...) y float(...) al final.
    """
    review_count = len(ratings)

    # TODO (1): conteo por estrella.
    #   counts[s] = cuántos ratings son iguales a s, para cada s en STARS.
    #   Pista: counts = {s: 0 for s in STARS}; luego recorre ratings y suma,
    #   o usa ratings.count(float(s)). Deben ser ints de Python.
    counts: dict[int, int] = ...  # TODO

    # TODO (2): proporción por estrella.
    #   Si review_count > 0: proportions[s] = counts[s] / review_count.
    #   Si no hay reseñas: proportions[s] = 0.0 para cada s.
    proportions: dict[int, float] = ...  # TODO

    # TODO (3): media y mediana con PyTorch.
    #   - Si no hay ratings: mean = None y median = None.
    #   - Si hay: crea un tensor float: t = torch.tensor(ratings, dtype=torch.float32)
    #       mean   = float(t.mean())
    #       median = float(t.quantile(0.5))   # 0.5 = mediana (promedia los dos centrales)
    #   Usamos quantile(0.5) para que coincida con la mediana de pandas/numpy.
    mean: float | None = ...  # TODO
    median: float | None = ...  # TODO

    return Summary(
        review_count=review_count,
        counts=counts,
        proportions=proportions,
        mean=mean,
        median=median,
    )
