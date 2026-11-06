"""Estadísticas de las valoraciones (ratings) de un producto.
"""

from dataclasses import dataclass

import torch

# Las cinco estrellas posibles, en orden. Para usar en conteos y proporciones.
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

    counts = {s: 0 for s in STARS}
    for rating in ratings:
        if rating in STARS:
            counts[int(rating)] += 1
            
    if review_count > 0:
        proportions = {s: counts[s] / review_count for s in STARS}
    else:
        proportions = {s: 0.0 for s in STARS}
        
    if review_count > 0:
        t = torch.tensor(ratings, dtype=torch.float32)
        mean = float(t.mean())
        median = float(t.quantile(0.5))
    else:
        mean = None
        median = None

    return Summary(
        review_count=review_count,
        counts=counts,
        proportions=proportions,
        mean=mean,
        median=median,
    )
