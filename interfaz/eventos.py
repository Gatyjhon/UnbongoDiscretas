"""
eventos.py
"""
import pygame

from interfaz.config import TAM_CELDA, ORIGEN_TABLERO


def pixel_a_celda(pos_mouse, origen=ORIGEN_TABLERO, tam_celda=TAM_CELDA):
    
    x, y = pos_mouse
    col = (x - origen[0]) // tam_celda
    fila = (y - origen[1]) // tam_celda
    return int(fila), int(col)


def celda_dentro_de_rango(fila, col, filas_totales, columnas_totales):
    return 0 <= fila < filas_totales and 0 <= col < columnas_totales


def calcular_rects_bandeja(piezas_info, origen, ancho_caja, alto_caja, espacio, columnas):
    rects = {}
    x0, y0 = origen
    for posicion, (indice_original, _matriz) in enumerate(piezas_info):
        fila_grid = posicion // columnas
        columna_grid = posicion % columnas
        x = x0 + columna_grid * (ancho_caja + espacio)
        y = y0 + fila_grid * (alto_caja + espacio)
        rects[indice_original] = pygame.Rect(x, y, ancho_caja, alto_caja)
    return rects


def pieza_bajo_click(pos_mouse, rects_bandeja):
    for indice, rect in rects_bandeja.items():
        if rect.collidepoint(pos_mouse):
            return indice
    return None


class GestorPiezaActiva:


    def __init__(self, piezas):
        self.piezas = list(piezas)                 # piezas del nivel, identidad fija por índice
        self.colocada = [False] * len(self.piezas)  # bandera por pieza
        self.indice_seleccionada = self._primera_pendiente()
        self.indice_configuracion = 0
        self.configuraciones_actuales = []
        self._recalcular_configuraciones()

    def _primera_pendiente(self):
        for indice, esta_colocada in enumerate(self.colocada):
            if not esta_colocada:
                return indice
        return None

    def _recalcular_configuraciones(self):
        from motor_matematico.piezas import generar_configuraciones
        if self.indice_seleccionada is not None:
            self.configuraciones_actuales = generar_configuraciones(self.piezas[self.indice_seleccionada])
        else:
            self.configuraciones_actuales = []

    @property
    def pieza_actual(self):
        if not self.configuraciones_actuales:
            return None
        return self.configuraciones_actuales[self.indice_configuracion]

    @property
    def id_pieza_actual(self):
        if self.indice_seleccionada is None:
            return None
        return self.indice_seleccionada + 1

    def piezas_pendientes_info(self):
        return [(i, p) for i, p in enumerate(self.piezas) if not self.colocada[i]]

    def seleccionar(self, indice_original):
        if 0 <= indice_original < len(self.piezas) and not self.colocada[indice_original]:
            self.indice_seleccionada = indice_original
            self.indice_configuracion = 0
            self._recalcular_configuraciones()

    def rotar(self):
        if self.configuraciones_actuales:
            self.indice_configuracion = (self.indice_configuracion + 1) % len(self.configuraciones_actuales)

    def confirmar_colocacion(self):
        if self.indice_seleccionada is not None:
            self.colocada[self.indice_seleccionada] = True
        self.indice_seleccionada = self._primera_pendiente()
        self.indice_configuracion = 0
        self._recalcular_configuraciones()

    def quedan_piezas(self):
        return any(not esta_colocada for esta_colocada in self.colocada)
