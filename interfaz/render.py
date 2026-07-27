"""
render.py
"""
import pygame
from interfaz.config import (
    TAM_CELDA, ORIGEN_TABLERO, COLOR_BORDE, COLOR_TEXTO, color_por_id
)


def dibujar_tablero(pantalla, tablero, origen=ORIGEN_TABLERO, tam_celda=TAM_CELDA):

    filas, columnas = tablero.shape
    for f in range(filas):
        for c in range(columnas):
            valor = int(tablero[f, c])
            color = color_por_id(valor)
            x = origen[0] + c * tam_celda
            y = origen[1] + f * tam_celda
            rect = pygame.Rect(x, y, tam_celda, tam_celda)
            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, COLOR_BORDE, rect, width=2)


def dibujar_pieza_flotante(pantalla, pieza, pos_pixel, tam_celda=TAM_CELDA, color=(255, 255, 255, 150)):

    filas_p, cols_p = pieza.shape
    for f in range(filas_p):
        for c in range(cols_p):
            if pieza[f, c] == 1:
                x = pos_pixel[0] + c * tam_celda
                y = pos_pixel[1] + f * tam_celda
                rect = pygame.Rect(x, y, tam_celda, tam_celda)
                pygame.draw.rect(pantalla, color, rect)
                pygame.draw.rect(pantalla, COLOR_BORDE, rect, width=1)


def dibujar_hud(pantalla, fuente, tiempo_restante, nivel, pistas_usadas):

    color_tiempo = COLOR_TEXTO if tiempo_restante > 10 else (255, 80, 80)
    texto_tiempo = fuente.render(f"Tiempo: {int(tiempo_restante)}s", True, color_tiempo)
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, COLOR_TEXTO)
    texto_pistas = fuente.render(f"Pistas usadas: {pistas_usadas}", True, COLOR_TEXTO)

    pantalla.blit(texto_tiempo, (500, 20))
    pantalla.blit(texto_nivel, (500, 45))
    pantalla.blit(texto_pistas, (500, 70))


def dibujar_mensaje_centrado(pantalla, fuente, texto, ancho_ventana, alto_ventana, color=COLOR_TEXTO):
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
    pantalla.blit(superficie, rect)
