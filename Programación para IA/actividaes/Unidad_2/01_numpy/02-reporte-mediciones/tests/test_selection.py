import numpy as np
import pytest

from measurements.selection import select_warm_rounds

BASE = np.array(
    [
        [26.0, 28.0, 24.0],
        [27.0, 29.0, 25.0],
        [28.0, 30.0, 26.0],
    ]
)


def test_exact_threshold_is_included():
    # el umbral es inclusivo (>=): la fila con norte == 27 sí entra
    result = select_warm_rounds(BASE, 27)
    np.testing.assert_array_equal(result, [[27, 29, 25], [28, 30, 26]])
    assert result.shape == (2, 3)


def test_no_matches_returns_empty_three_columns():
    result = select_warm_rounds(BASE, 100)
    assert result.shape == (0, 3)


def test_nonfinite_data_or_threshold_are_rejected():
    with pytest.raises(ValueError):
        select_warm_rounds(np.array([[np.nan, 1.0, 2.0], [3.0, 4.0, 5.0]]), 0)
    with pytest.raises(ValueError):
        select_warm_rounds(BASE, np.inf)


def test_selection_is_independent_from_input():
    original = BASE.copy()
    result = select_warm_rounds(BASE, 27)
    result[0, 0] = -100
    np.testing.assert_array_equal(BASE, original)  # la entrada no cambió
