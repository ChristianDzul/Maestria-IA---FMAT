"""Select measurement rounds by the north-room temperature."""

import numpy as np

from measurements.processing import FloatArray, validate_shape

NORTH_COLUMN = 0


def select_warm_rounds(readings: FloatArray, threshold: float) -> FloatArray:
    """Return an independent copy of the rounds whose north temperature >= threshold."""
    validate_shape(
        readings
    )  # reutiliza la comprobación de matriz 2D no vacía con 3 columnas
    if not np.isfinite(readings).all():
        raise ValueError("Readings must be finite")
    if not np.isfinite(threshold):
        raise ValueError("Threshold must be finite")
    warm = (
        readings[:, NORTH_COLUMN] >= threshold
    )  # máscara: norte >= umbral (inclusivo)
    return readings[warm].copy()  # copia independiente: no modifica la entrada
