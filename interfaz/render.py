"""
render.py
"""
import pygame
from interfaz.config import (
    TAM_CELDA, ORIGEN_TABLERO, COLOR_BORDE, COLOR_TEXTO, COLOR_FONDO, color_por_id
)
from interfaz.eventos import calcular_rects_bandeja
from motor_matematico.tablero import BLOQUEADO


def dibujar_tablero(pantalla, tablero, origen=ORIGEN_TABLERO, tam_celda=TAM_CELDA):
    """
    Recorre la matriz fila por fila, columna por columna (doble for, típico
    de recorrer una matriz discreta) y dibuja un rectángulo por celda.

    La conversión clave es:
        x_pixel = origen_x + columna * tam_celda
        y_pixel = origen_y + fila    * tam_celda
    Es decir, cada "paso" en la matriz (una columna o fila más) equivale
    a desplazarse tam_celda píxeles en la pantalla.

    Las celdas BLOQUEADAS (fuera de la silueta jugable del nivel, ver
    motor_matematico.tablero.crear_tablero_con_forma) se pintan del mismo
    color que el fondo y sin borde: visualmente "no existen", que es
    justo el efecto de silueta irregular del Ubongo físico.
    """
    filas, columnas = tablero.shape
    for f in range(filas):
        for c in range(columnas):
            valor = int(tablero[f, c])
            x = origen[0] + c * tam_celda
            y = origen[1] + f * tam_celda
            rect = pygame.Rect(x, y, tam_celda, tam_celda)

            if valor == BLOQUEADO:
                pygame.draw.rect(pantalla, COLOR_FONDO, rect)
                continue

            color = color_por_id(valor)
            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, COLOR_BORDE, rect, width=2)


def dibujar_pieza_flotante(pantalla, pieza, pos_pixel, tam_celda=TAM_CELDA, color=(255, 255, 255, 150)):
    """
    Dibuja la pieza que el jugador está arrastrando actualmente, siguiendo
    al mouse, ANTES de que se confirme su colocación en el tablero.
    pos_pixel es la esquina superior izquierda en píxeles (ya calculada
    por eventos.py a partir de la posición del mouse).
    """
    filas_p, cols_p = pieza.shape
    for f in range(filas_p):
        for c in range(cols_p):
            if pieza[f, c] == 1:
                x = pos_pixel[0] + c * tam_celda
                y = pos_pixel[1] + f * tam_celda
                rect = pygame.Rect(x, y, tam_celda, tam_celda)
                pygame.draw.rect(pantalla, color, rect)
                pygame.draw.rect(pantalla, COLOR_BORDE, rect, width=1)


def dibujar_hud(pantalla, fuente, tiempo_restante, nivel, pistas_usadas, origen=(640, 20)):
    """
    HUD = Heads-Up Display, el panel de texto con info del estado actual
    (no del tablero, sino de la partida: tiempo, nivel, pistas).
    Todo esto son datos que vienen de temporizador.py y del control de
    flujo del juego, render.py solo los pinta.

    El texto se sobreponía porque el espacio vertical entre líneas (25px)
    era más chico que la altura real de una línea renderizada con
    fuente de tamaño 20 (fuente.get_linesize() ronda los 24-26px, y con
    el borde/antialiasing se nota el pisado). La solución es no usar un
    número mágico fijo: se pide a la propia fuente su alto de línea y se
    le suma un margen, así el espaciado siempre es correcto sin importar
    qué fuente o tamaño se use más adelante.
    """
    alto_linea = fuente.get_linesize() + 8
    x, y = origen

    color_tiempo = COLOR_TEXTO if tiempo_restante > 10 else (255, 80, 80)
    lineas = [
        (f"Tiempo: {int(tiempo_restante)}s", color_tiempo),
        (f"Nivel: {nivel}", COLOR_TEXTO),
        (f"Pistas usadas: {pistas_usadas}", COLOR_TEXTO),
    ]
    for i, (texto, color) in enumerate(lineas):
        superficie = fuente.render(texto, True, color)
        pantalla.blit(superficie, (x, y + i * alto_linea))


def dibujar_mensaje_centrado(pantalla, fuente, texto, ancho_ventana, alto_ventana, color=COLOR_TEXTO):
    superficie = fuente.render(texto, True, color)
    rect = superficie.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
    pantalla.blit(superficie, rect)


def dibujar_bandeja_piezas(pantalla, fuente, fuente_pequena, piezas_info, indice_seleccionada,
                            origen, ancho_caja, alto_caja, espacio, columnas, tam_celda_bandeja):
    """
    Dibuja TODAS las piezas pendientes del nivel a la vez (a diferencia
    del panel anterior, que solo mostraba "la siguiente"). Cada pieza
    vive en su propia casilla de una cuadrícula; la casilla de la pieza
    seleccionada se resalta con un borde verde para que el jugador sepa
    cuál está a punto de arrastrar.

    La posición de cada casilla la calcula eventos.calcular_rects_bandeja
    (la MISMA función que usa juego.py para detectar el click), así el
    dibujo y la zona clickeable siempre coinciden.
    """
    titulo = fuente.render("Tus piezas (click para elegir):", True, COLOR_TEXTO)
    pantalla.blit(titulo, (origen[0], origen[1] - 35))

    rects = calcular_rects_bandeja(piezas_info, origen, ancho_caja, alto_caja, espacio, columnas)

    for indice_original, matriz in piezas_info:
        caja = rects[indice_original]
        es_seleccionada = indice_original == indice_seleccionada

        color_caja = (50, 65, 55) if es_seleccionada else (35, 35, 40)
        color_borde_caja = (120, 220, 140) if es_seleccionada else COLOR_BORDE
        pygame.draw.rect(pantalla, color_caja, caja, border_radius=6)
        pygame.draw.rect(pantalla, color_borde_caja, caja, width=2, border_radius=6)

        filas_p, cols_p = matriz.shape
        ancho_pieza = cols_p * tam_celda_bandeja
        alto_pieza = filas_p * tam_celda_bandeja
        # Centrar la miniatura dentro de la casilla para que tetrominós (más
        # pequeños) y pentominós (más grandes) queden prolijos por igual.
        offset_x = caja.x + (caja.width - ancho_pieza) // 2
        offset_y = caja.y + (caja.height - alto_pieza) // 2

        for f in range(filas_p):
            for c in range(cols_p):
                if matriz[f, c] == 1:
                    x = offset_x + c * tam_celda_bandeja
                    y = offset_y + f * tam_celda_bandeja
                    rect = pygame.Rect(x, y, tam_celda_bandeja, tam_celda_bandeja)
                    pygame.draw.rect(pantalla, color_por_id(indice_original + 1), rect)
                    pygame.draw.rect(pantalla, COLOR_BORDE, rect, width=1)

        etiqueta = fuente_pequena.render(str(indice_original + 1), True, (170, 170, 175))
        pantalla.blit(etiqueta, (caja.x + 6, caja.y + 4))


def dibujar_controles(pantalla, fuente_pequena, origen=(20, 20)):
    """
    Recordatorio permanente de controles. No es lógica del juego, es
    simplemente información para el jugador; por eso vive en render.py
    y no en ningún otro módulo.
    """
    lineas = [
        "Click en una pieza (o teclas 1-9): elegir cuál mover   |   R: rotar/reflejar",
        "Arrastra y suelta sobre el tablero: colocarla   |   H: pista",
        "N: reiniciar nivel   |   ESC: reiniciar partida",
    ]
    for i, linea in enumerate(lineas):
        superficie = fuente_pequena.render(linea, True, (170, 170, 175))
        pantalla.blit(superficie, (origen[0], origen[1] + i * 18))


def dibujar_resumen_nivel(pantalla, fuente, fuente_grande, ancho_ventana, alto_ventana,
                           nombre_nivel, tiempo_usado, pistas_usadas, tiempo_siguiente_nivel,
                           es_ultimo_nivel):
    """
    Pantalla de estadísticas mostrada justo al completar un nivel.
    Se queda visible hasta que el jugador presiona una tecla para avanzar
    (ver juego.py, estado 'nivel_completado').
    """
    overlay = pygame.Surface((ancho_ventana, alto_ventana))
    overlay.set_alpha(230)
    overlay.fill((15, 15, 18))
    pantalla.blit(overlay, (0, 0))

    titulo = fuente_grande.render(f"¡Nivel {nombre_nivel} completado!", True, (120, 220, 140))
    pantalla.blit(titulo, titulo.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 - 90)))

    lineas = [
        f"Tiempo usado: {tiempo_usado:.1f} s",
        f"Pistas utilizadas: {pistas_usadas}",
    ]
    if es_ultimo_nivel:
        lineas.append("¡Completaste el último nivel disponible!")
    else:
        lineas.append(f"Tiempo del siguiente nivel: {int(tiempo_siguiente_nivel)} s")
        lineas.append("Presiona ENTER o ESPACIO para continuar")

    for i, linea in enumerate(lineas):
        superficie = fuente.render(linea, True, COLOR_TEXTO)
        pantalla.blit(superficie, superficie.get_rect(
            center=(ancho_ventana // 2, alto_ventana // 2 - 30 + i * 30)
        ))
