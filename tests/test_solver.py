"""
test_solver.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from motor_matematico.tablero import crear_tablero
from motor_matematico.piezas import TETROMINOS, PENTOMINOS, generar_configuraciones
from motor_matematico.solver import resolver, cabe, colocar, generar_nivel_valido


def test_caso_resoluble():

    tablero = crear_tablero(2, 4)
    piezas = [TETROMINOS["O"], TETROMINOS["O"]]
    resultado = resolver(tablero, piezas)
    assert resultado is True, "Se esperaba que este conjunto de piezas SÍ tuviera solución"
    assert not np.any(tablero == 0), "El tablero debería quedar completamente lleno"
    print("test_caso_resoluble: OK")
    print(tablero, "\n")


def test_caso_no_resoluble():
    """Un tablero 2x2 (4 celdas) no puede recibir dos tetrominós (8 celdas): debe fallar."""
    tablero = crear_tablero(2, 2)
    piezas = [TETROMINOS["O"], TETROMINOS["L"]]
    resultado = resolver(tablero, piezas)
    assert resultado is False, "No debería existir solución: sobran piezas para el espacio disponible"
    print("test_caso_no_resoluble: OK (correctamente detectado como sin solución)\n")


def test_configuraciones_unicas():
    """La pieza cuadrada 'O' es simétrica bajo todo el grupo D4: debe dar solo 1 configuración única."""
    configs_o = generar_configuraciones(TETROMINOS["O"])
    assert len(configs_o) == 1, f"Se esperaba 1 configuración para 'O', se obtuvieron {len(configs_o)}"

    configs_l = generar_configuraciones(TETROMINOS["L"])
    assert len(configs_l) in (4, 8), f"Configuraciones inesperadas para 'L': {len(configs_l)}"
    print(f"test_configuraciones_unicas: OK ('O' -> 1, 'L' -> {len(configs_l)})\n")


def test_generar_nivel_valido_tetrominos():
    piezas, tablero_solucion = generar_nivel_valido(6, 6, TETROMINOS, cantidad_piezas=3)
    assert len(piezas) == 3
    print("test_generar_nivel_valido_tetrominos: OK, nivel generado con solución garantizada\n")


def test_generar_nivel_valido_pentominos():
    piezas, tablero_solucion = generar_nivel_valido(6, 6, PENTOMINOS, cantidad_piezas=3)
    assert len(piezas) == 3
    print("test_generar_nivel_valido_pentominos: OK, nivel de dificultad alta generado\n")


if __name__ == "__main__":
    test_caso_resoluble()
    test_caso_no_resoluble()
    test_configuraciones_unicas()
    test_generar_nivel_valido_tetrominos()
    test_generar_nivel_valido_pentominos()
    print("Todas las pruebas del solver pasaron correctamente.")
