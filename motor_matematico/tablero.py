"""
tablero.py
"""
import numpy as np


def crear_tablero(filas, columnas):
    return np.zeros((filas, columnas), dtype=int)


def tablero_lleno(tablero):

    return not np.any(tablero == 0)


def copiar_tablero(tablero):

    return tablero.copy()
