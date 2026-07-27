"""
juego.py
"""
import sys
import pygame

from motor_matematico.tablero import crear_tablero
from motor_matematico.solver import cabe, colocar, generar_nivel_valido, encontrar_siguiente_pista
from motor_matematico.temporizador import Temporizador
from motor_matematico.piezas import TETROMINOS, PENTOMINOS

from interfaz.config import (
    ANCHO_VENTANA, ALTO_VENTANA, TAM_CELDA, ORIGEN_TABLERO, FPS, COLOR_FONDO
)
from interfaz.render import dibujar_tablero, dibujar_pieza_flotante, dibujar_hud, dibujar_mensaje_centrado
from interfaz.eventos import pixel_a_celda, GestorPiezaActiva


FILAS_TABLERO = 6
COLUMNAS_TABLERO = 6


def construir_nivel(dificultad):

    banco = TETROMINOS if dificultad in ("facil", "medio") else PENTOMINOS
    cantidad = {"facil": 3, "medio": 4, "dificil": 3}.get(dificultad, 3)
    piezas, tablero_solucion = generar_nivel_valido(
        FILAS_TABLERO, COLUMNAS_TABLERO, banco, cantidad
    )
    return piezas, tablero_solucion


def iniciar(dificultad="facil"):
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("DiscreteUbongo")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("consolas", 22)

    # --- Estado inicial del nivel (usa el motor matemático, no Pygame) ---
    tablero = crear_tablero(FILAS_TABLERO, COLUMNAS_TABLERO)
    piezas_nivel, _ = construir_nivel(dificultad)
    gestor = GestorPiezaActiva(piezas_nivel)

    temporizador = Temporizador(tiempo_inicial=60, d=5)
    tiempo_restante = temporizador.T
    pistas_usadas = 0
    nivel_actual = 1

    arrastrando = False
    juego_terminado = False
    mensaje_final = ""

    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS) / 1000.0  # segundos transcurridos desde el frame anterior

        # ---------- 1) ENTRADA ----------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN and not juego_terminado:
                if evento.key == pygame.K_r:
                    gestor.rotar()  # cambia a la siguiente configuración (rotación/reflejo)
                elif evento.key == pygame.K_h:
                    # --- Sistema de pistas: reutiliza el backtracking ---
                    indice_pieza = len(piezas_nivel) - len(gestor.piezas_pendientes)
                    resultado = encontrar_siguiente_pista(tablero, piezas_nivel, indice_pieza)
                    pistas_usadas += 1
                    if resultado:
                        fila, col, config = resultado
                        colocar(tablero, config, fila, col, indice_pieza + 1)
                        gestor.confirmar_colocacion()
                    else:
                        mensaje_final = "El solver indica que ya no hay solución posible desde aquí."

            elif evento.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
                arrastrando = True

            elif evento.type == pygame.MOUSEBUTTONUP and not juego_terminado:
                arrastrando = False
                if gestor.pieza_actual is not None:
                    fila, col = pixel_a_celda(evento.pos)
                    pieza = gestor.pieza_actual
                    if cabe(tablero, pieza, fila, col):
                        indice_pieza = len(piezas_nivel) - len(gestor.piezas_pendientes)
                        colocar(tablero, pieza, fila, col, indice_pieza + 1)
                        gestor.confirmar_colocacion()

        # ---------- 2) ACTUALIZAR ESTADO ----------
        if not juego_terminado:
            tiempo_restante -= dt
            if tiempo_restante <= 0:
                juego_terminado = True
                mensaje_final = "¡Se acabó el tiempo!"
            elif not gestor.quedan_piezas():
                juego_terminado = True
                # Aplicamos la recurrencia para saber el tiempo del siguiente nivel
                nuevo_tiempo = temporizador.siguiente_tiempo(pistas_usadas)
                mensaje_final = f"¡Nivel completado! Siguiente nivel: {int(nuevo_tiempo)}s"

        # ---------- 3) DIBUJAR ----------
        pantalla.fill(COLOR_FONDO)
        dibujar_tablero(pantalla, tablero)
        dibujar_hud(pantalla, fuente, tiempo_restante, nivel_actual, pistas_usadas)

        if arrastrando and gestor.pieza_actual is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dibujar_pieza_flotante(pantalla, gestor.pieza_actual, (mouse_x, mouse_y))

        if juego_terminado:
            dibujar_mensaje_centrado(pantalla, fuente, mensaje_final, ANCHO_VENTANA, ALTO_VENTANA)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    iniciar(dificultad="facil")
