"""
eventos.py
"""
from interfaz.config import TAM_CELDA, ORIGEN_TABLERO


def pixel_a_celda(pos_mouse, origen=ORIGEN_TABLERO, tam_celda=TAM_CELDA):

    x, y = pos_mouse
    col = (x - origen[0]) // tam_celda
    fila = (y - origen[1]) // tam_celda
    return int(fila), int(col)


def celda_dentro_de_rango(fila, col, filas_totales, columnas_totales):
    return 0 <= fila < filas_totales and 0 <= col < columnas_totales


class GestorPiezaActiva:


    def __init__(self, piezas_pendientes):
        self.piezas_pendientes = list(piezas_pendientes)  # piezas que faltan por colocar
        self.indice_configuracion = 0
        self.configuraciones_actuales = []
        self._recalcular_configuraciones()

    def _recalcular_configuraciones(self):
        from motor_matematico.piezas import generar_configuraciones
        if self.piezas_pendientes:
            self.configuraciones_actuales = generar_configuraciones(self.piezas_pendientes[0])
        else:
            self.configuraciones_actuales = []

    @property
    def pieza_actual(self):
        if not self.configuraciones_actuales:
            return None
        return self.configuraciones_actuales[self.indice_configuracion]

    def rotar(self):
        if self.configuraciones_actuales:
            self.indice_configuracion = (self.indice_configuracion + 1) % len(self.configuraciones_actuales)

    def confirmar_colocacion(self):

        if self.piezas_pendientes:
            self.piezas_pendientes.pop(0)
        self.indice_configuracion = 0
        self._recalcular_configuraciones()

    def quedan_piezas(self):
        return len(self.piezas_pendientes) > 0
