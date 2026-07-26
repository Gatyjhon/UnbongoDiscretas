"""
piezas.py
"""
import numpy as np

TETROMINOS = {
    "I": np.array([[1, 1, 1, 1]]),
    "O": np.array([[1, 1],
                    [1, 1]]),
    "T": np.array([[1, 1, 1],
                    [0, 1, 0]]),
    "S": np.array([[0, 1, 1],
                    [1, 1, 0]]),
    "L": np.array([[1, 0],
                    [1, 0],
                    [1, 1]]),
}

PENTOMINOS = {
    "F": np.array([[0, 1, 1],
                    [1, 1, 0],
                    [0, 1, 0]]),
    "P": np.array([[1, 1],
                    [1, 1],
                    [1, 0]]),
    "N": np.array([[0, 1],
                    [0, 1],
                    [1, 1],
                    [1, 0]]),
    "L": np.array([[1, 0],
                    [1, 0],
                    [1, 0],
                    [1, 1]]),
    "I": np.array([[1, 1, 1, 1, 1]]),
}


def generar_configuraciones(matriz):
    """Genera las hasta 8 configuraciones únicas de una pieza (4 rotaciones x 2 reflejos)."""
    configuraciones = set()
    base = matriz.copy()

    for reflejo in [base, np.fliplr(base)]:
        actual = reflejo
        for _ in range(4):
            actual = np.rot90(actual)
            clave = tuple(map(tuple, actual))
            configuraciones.add(clave)

    return [np.array(c) for c in configuraciones]

