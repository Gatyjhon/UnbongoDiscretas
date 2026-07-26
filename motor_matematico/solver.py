"""
solver.py
"""
import numpy as np
from motor_matematico.piezas import generar_configuraciones


def cabe(tablero, pieza, fila, col):
    filas_p, cols_p = pieza.shape
    filas_t, cols_t = tablero.shape

    if fila < 0 or col < 0 or fila + filas_p > filas_t or col + cols_p > cols_t:
        return False

    region = tablero[fila:fila + filas_p, col:col + cols_p]
    # region > 0  -> celda ya ocupada por CUALQUIER pieza anterior (no solo id 1)
    # pieza == 1  -> celda que esta pieza quiere ocupar
    return not np.any((region > 0) & (pieza == 1))


def colocar(tablero, pieza, fila, col, valor):
    filas_p, cols_p = pieza.shape
    region = tablero[fila:fila + filas_p, col:col + cols_p]
    mascara = pieza == 1
    region[mascara] = valor


def resolver(tablero, piezas, indice=0):

    if indice == len(piezas):
        return True  # Hoja de éxito: no quedan piezas por colocar

    pieza_original = piezas[indice]
    configuraciones = generar_configuraciones(pieza_original)
    filas_t, cols_t = tablero.shape

    for config in configuraciones:
        filas_p, cols_p = config.shape
        # Solo tiene sentido probar posiciones donde la pieza podría caber
        for fila in range(filas_t - filas_p + 1):
            for col in range(cols_t - cols_p + 1):
                if cabe(tablero, config, fila, col):
                    colocar(tablero, config, fila, col, indice + 1)   # avanzar

                    if resolver(tablero, piezas, indice + 1):         # recursión
                        return True                                   # éxito, propagar hacia arriba

                    colocar(tablero, config, fila, col, 0)             # BACKTRACK: deshacer

    return False  # ninguna rama de este nodo funcionó -> el padre debe retroceder


def encontrar_siguiente_pista(tablero, piezas, indice_actual):

    copia = tablero.copy()
    pieza_original = piezas[indice_actual]
    configuraciones = generar_configuraciones(pieza_original)
    filas_t, cols_t = copia.shape

    for config in configuraciones:
        filas_p, cols_p = config.shape
        for fila in range(filas_t - filas_p + 1):
            for col in range(cols_t - cols_p + 1):
                if cabe(copia, config, fila, col):
                    colocar(copia, config, fila, col, indice_actual + 1)
                    if resolver(copia, piezas, indice_actual + 1):
                        return fila, col, config
                    colocar(copia, config, fila, col, 0)
    return None


def generar_nivel_valido(filas, columnas, banco_piezas, cantidad_piezas, intentos_maximos=500):

    import random
    from motor_matematico.tablero import crear_tablero

    for _ in range(intentos_maximos):
        piezas_elegidas = random.sample(list(banco_piezas.values()), cantidad_piezas)
        tablero_prueba = crear_tablero(filas, columnas)
        if resolver(tablero_prueba, piezas_elegidas):
            return piezas_elegidas, tablero_prueba  # tablero_prueba ya queda con la solución de referencia

    raise RuntimeError(
        "No se encontró una combinación solucionable en el número de intentos dado. "
        "Prueba con un tablero más grande o menos piezas."
    )
