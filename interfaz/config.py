"""
config.py
"""

ANCHO_VENTANA = 1000
ALTO_VENTANA = 700
TAM_CELDA = 50
ORIGEN_TABLERO = (50, 150)   # (x, y) en píxeles donde empieza a dibujarse el tablero
FPS = 60

# --- Geometría de la BANDEJA de piezas -------------------------------

ORIGEN_BANDEJA = (640, 190)
ANCHO_CAJA_BANDEJA = 140
ALTO_CAJA_BANDEJA = 140
ESPACIO_BANDEJA = 12
COLUMNAS_BANDEJA = 2
TAM_CELDA_BANDEJA = 22   # tamaño de cada celdita dentro de una casilla de la bandeja

# Mapa de dificultad -> banco de piezas y cantidad de piezas por nivel.
NIVELES = [
    {"nombre": "Fácil",   "banco": "tetrominos", "cantidad": 2},
    {"nombre": "Medio",   "banco": "tetrominos", "cantidad": 4},
    {"nombre": "Difícil", "banco": "pentominos", "cantidad": 3},
]

COLOR_FONDO = (24, 24, 28)
COLOR_VACIO = (45, 45, 50)
COLOR_BORDE = (10, 10, 10)
COLOR_TEXTO = (230, 230, 230)
COLOR_ALERTA = (220, 60, 60)

# Un color distinto por id de pieza
PALETA_PIEZAS = {
    1: (231, 76, 60),
    2: (46, 204, 113),
    3: (52, 152, 219),
    4: (241, 196, 15),
    5: (155, 89, 182),
    6: (26, 188, 156),
    7: (230, 126, 34),
    9: (236, 240, 241),  # color neutro reservado para la vista previa de "siguiente pieza"
}


def color_por_id(id_pieza):
    if id_pieza == 0:
        return COLOR_VACIO
    return PALETA_PIEZAS.get(id_pieza, (200, 200, 200))
