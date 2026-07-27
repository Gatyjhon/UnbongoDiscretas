"""
config.py
"""

ANCHO_VENTANA = 900
ALTO_VENTANA = 650
TAM_CELDA = 50
ORIGEN_TABLERO = (50, 80)   # (x, y) en píxeles donde empieza a dibujarse el tablero
FPS = 60

COLOR_FONDO = (24, 24, 28)
COLOR_VACIO = (45, 45, 50)
COLOR_BORDE = (10, 10, 10)
COLOR_TEXTO = (230, 230, 230)
COLOR_ALERTA = (220, 60, 60)

# Un color distinto por id de pieza (id 0 = vacío, no se usa aquí)
PALETA_PIEZAS = {
    1: (231, 76, 60),
    2: (46, 204, 113),
    3: (52, 152, 219),
    4: (241, 196, 15),
    5: (155, 89, 182),
    6: (26, 188, 156),
    7: (230, 126, 34),
}


def color_por_id(id_pieza):
    if id_pieza == 0:
        return COLOR_VACIO
    return PALETA_PIEZAS.get(id_pieza, (200, 200, 200))
