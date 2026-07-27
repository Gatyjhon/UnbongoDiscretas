"""
tablero.py
"""
import numpy as np


BLOQUEADO = -1


def crear_tablero(filas, columnas):
    
    return np.zeros((filas, columnas), dtype=int)


def crear_tablero_con_forma(mascara):
    return np.where(mascara, 0, BLOQUEADO).astype(int)


def tablero_lleno(tablero):
   
    return not np.any(tablero == 0)


def copiar_tablero(tablero):
    return tablero.copy()
