"""
juego.py
"""
import sys
import pygame

from motor_matematico.tablero import crear_tablero_con_forma
from motor_matematico.solver import cabe, colocar, generar_nivel_valido, encontrar_siguiente_pista
from motor_matematico.temporizador import Temporizador
from motor_matematico.piezas import TETROMINOS, PENTOMINOS

from interfaz.config import (
    ANCHO_VENTANA, ALTO_VENTANA, TAM_CELDA, ORIGEN_TABLERO, FPS, COLOR_FONDO,
    ORIGEN_BANDEJA, ANCHO_CAJA_BANDEJA, ALTO_CAJA_BANDEJA, ESPACIO_BANDEJA,
    COLUMNAS_BANDEJA, TAM_CELDA_BANDEJA, NIVELES
)
from interfaz.render import (
    dibujar_tablero, dibujar_pieza_flotante, dibujar_hud, dibujar_mensaje_centrado,
    dibujar_bandeja_piezas, dibujar_controles, dibujar_resumen_nivel
)
from interfaz.eventos import pixel_a_celda, calcular_rects_bandeja, pieza_bajo_click, GestorPiezaActiva

# Teclas 1-9 para seleccionar directamente la pieza en esa posición de la
# bandeja, sin necesidad de hacer click
TECLAS_NUMERICAS = [
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
]


FILAS_TABLERO = 6
COLUMNAS_TABLERO = 6


JUGANDO = "jugando"
NIVEL_COMPLETADO = "nivel_completado"
TIEMPO_AGOTADO = "tiempo_agotado"


def banco_de_piezas(nombre_banco):
    return TETROMINOS if nombre_banco == "tetrominos" else PENTOMINOS


def construir_nivel(indice_nivel):
    definicion = NIVELES[min(indice_nivel, len(NIVELES) - 1)]
    banco = banco_de_piezas(definicion["banco"])
    piezas, mascara_forma = generar_nivel_valido(
        FILAS_TABLERO, COLUMNAS_TABLERO, banco, definicion["cantidad"]
    )
    return piezas, mascara_forma, definicion["nombre"]


class EstadoPartida:

    def __init__(self):
        self.indice_nivel = 0
        self.tablero = None
        self.gestor = None
        self.temporizador = Temporizador(tiempo_inicial=60, d=5)
        self.tiempo_restante = 0.0
        self.tiempo_inicial_nivel = 0.0
        self.pistas_usadas = 0
        self.nombre_nivel_actual = ""
        self.estado = JUGANDO
        self.cargar_nivel(0, tiempo=self.temporizador.T)

    def cargar_nivel(self, indice_nivel, tiempo):
        """Prepara un nivel nuevo: piezas garantizadas solucionables (backtracking) + tablero con su silueta."""
        piezas, mascara_forma, nombre = construir_nivel(indice_nivel)
        self.indice_nivel = indice_nivel
        self.tablero = crear_tablero_con_forma(mascara_forma)
        self.gestor = GestorPiezaActiva(piezas)
        self.nombre_nivel_actual = nombre
        self.tiempo_restante = tiempo
        self.tiempo_inicial_nivel = tiempo
        self.pistas_usadas = 0
        self.estado = JUGANDO

    def registrar_pieza_colocada(self):
        self.gestor.confirmar_colocacion()

    def reiniciar_nivel_actual(self):
        """Tecla N: regenera el MISMO nivel (misma dificultad), con el tiempo con el que había entrado."""
        self.cargar_nivel(self.indice_nivel, tiempo=self.tiempo_inicial_nivel)

    def reiniciar_partida_completa(self):
        """Tecla ESC: vuelve al nivel 1 y también reinicia la recurrencia del tiempo desde T0."""
        self.temporizador = Temporizador(tiempo_inicial=60, d=5)
        self.cargar_nivel(0, tiempo=self.temporizador.T)

    def es_ultimo_nivel(self):
        return self.indice_nivel >= len(NIVELES) - 1

    def avanzar_siguiente_nivel(self):
        """Se llama tras la pantalla de estadísticas, al presionar ENTER/ESPACIO."""
        if self.es_ultimo_nivel():
            return  # ya no hay más niveles; se queda mostrando el resumen final
        # self.temporizador.T ya fue actualizado por la recurrencia al completar el nivel anterior
        self.cargar_nivel(self.indice_nivel + 1, tiempo=self.temporizador.T)


def pedir_pista(partida):
    gestor = partida.gestor
    if gestor.indice_seleccionada is None:
        return None

    pendientes = gestor.piezas_pendientes_info()  # [(indice_original, matriz), ...]
    seleccionada = gestor.piezas[gestor.indice_seleccionada]
    resto = [matriz for indice, matriz in pendientes if indice != gestor.indice_seleccionada]
    lista_para_resolver = [seleccionada] + resto

    return encontrar_siguiente_pista(partida.tablero, lista_para_resolver, 0)


def iniciar():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("DiscreteUbongo")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 20)
    fuente_pequena = pygame.font.SysFont("consolas", 15)
    fuente_grande = pygame.font.SysFont("consolas", 28, bold=True)

    partida = EstadoPartida()
    arrastrando = False

    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS) / 1000.0

        # ---------- 1) ENTRADA ----------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:
                # Los reinicios funcionan en CUALQUIER estado (jugando, completado, tiempo agotado)
                if evento.key == pygame.K_n:
                    partida.reiniciar_nivel_actual()
                elif evento.key == pygame.K_ESCAPE:
                    partida.reiniciar_partida_completa()

                elif partida.estado == JUGANDO:
                    if evento.key == pygame.K_r:
                        partida.gestor.rotar()
                    elif evento.key == pygame.K_h:
                        resultado = pedir_pista(partida)
                        partida.pistas_usadas += 1
                        if resultado:
                            fila, col, config = resultado
                            colocar(partida.tablero, config, fila, col, partida.gestor.id_pieza_actual)
                            partida.registrar_pieza_colocada()
                    elif evento.key in TECLAS_NUMERICAS:
                        # Tecla '1' selecciona la pieza en la 1ra casilla visible
                        # de la bandeja, '2' la segunda, etc. (índice de POSICIÓN
                        # en pantalla, no el id fijo de la pieza).
                        posicion = TECLAS_NUMERICAS.index(evento.key)
                        pendientes = partida.gestor.piezas_pendientes_info()
                        if posicion < len(pendientes):
                            indice_original, _ = pendientes[posicion]
                            partida.gestor.seleccionar(indice_original)

                elif partida.estado == NIVEL_COMPLETADO:
                    if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        partida.avanzar_siguiente_nivel()

            elif evento.type == pygame.MOUSEBUTTONDOWN and partida.estado == JUGANDO:
                # Si el click cayó sobre una casilla de la bandeja, esa pieza
                # pasa a ser la seleccionada 
                pendientes = partida.gestor.piezas_pendientes_info()
                rects_bandeja = calcular_rects_bandeja(
                    pendientes, ORIGEN_BANDEJA, ANCHO_CAJA_BANDEJA,
                    ALTO_CAJA_BANDEJA, ESPACIO_BANDEJA, COLUMNAS_BANDEJA
                )
                indice_click = pieza_bajo_click(evento.pos, rects_bandeja)
                if indice_click is not None:
                    partida.gestor.seleccionar(indice_click)

                if partida.gestor.pieza_actual is not None:
                    arrastrando = True

            elif evento.type == pygame.MOUSEBUTTONUP and partida.estado == JUGANDO:
                arrastrando = False
                pieza = partida.gestor.pieza_actual
                if pieza is not None:
                    fila, col = pixel_a_celda(evento.pos)
                    if cabe(partida.tablero, pieza, fila, col):
                        colocar(partida.tablero, pieza, fila, col, partida.gestor.id_pieza_actual)
                        partida.registrar_pieza_colocada()

        # ---------- 2) ACTUALIZAR ESTADO ----------
        if partida.estado == JUGANDO:
            partida.tiempo_restante -= dt

            if partida.tiempo_restante <= 0:
                partida.tiempo_restante = 0
                partida.estado = TIEMPO_AGOTADO

            elif not partida.gestor.quedan_piezas():
                # Nivel resuelto: se aplica la recurrencia para calcular el tiempo del siguiente nivel
                partida.temporizador.siguiente_tiempo(partida.pistas_usadas)
                partida.estado = NIVEL_COMPLETADO

        # ---------- 3) DIBUJAR ----------
        pantalla.fill(COLOR_FONDO)
        dibujar_controles(pantalla, fuente_pequena)
        dibujar_tablero(pantalla, partida.tablero)
        dibujar_hud(
            pantalla, fuente, partida.tiempo_restante,
            f"{partida.indice_nivel + 1}/{len(NIVELES)} - {partida.nombre_nivel_actual}",
            partida.pistas_usadas
        )
        dibujar_bandeja_piezas(
            pantalla, fuente, fuente_pequena,
            partida.gestor.piezas_pendientes_info(), partida.gestor.indice_seleccionada,
            ORIGEN_BANDEJA, ANCHO_CAJA_BANDEJA, ALTO_CAJA_BANDEJA,
            ESPACIO_BANDEJA, COLUMNAS_BANDEJA, TAM_CELDA_BANDEJA
        )

        if arrastrando and partida.estado == JUGANDO and partida.gestor.pieza_actual is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dibujar_pieza_flotante(pantalla, partida.gestor.pieza_actual, (mouse_x, mouse_y))

        if partida.estado == TIEMPO_AGOTADO:
            dibujar_mensaje_centrado(
                pantalla, fuente_grande,
                "¡Se acabó el tiempo!  N: reintentar nivel   ESC: reiniciar partida",
                ANCHO_VENTANA, ALTO_VENTANA, color=(230, 90, 90)
            )

        elif partida.estado == NIVEL_COMPLETADO:
            tiempo_usado = partida.tiempo_inicial_nivel - partida.tiempo_restante
            dibujar_resumen_nivel(
                pantalla, fuente, fuente_grande, ANCHO_VENTANA, ALTO_VENTANA,
                nombre_nivel=partida.nombre_nivel_actual,
                tiempo_usado=tiempo_usado,
                pistas_usadas=partida.pistas_usadas,
                tiempo_siguiente_nivel=partida.temporizador.T,
                es_ultimo_nivel=partida.es_ultimo_nivel(),
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    iniciar()

