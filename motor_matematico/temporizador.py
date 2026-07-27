"""
temporizador.py
"""


class Temporizador:
    def __init__(self, tiempo_inicial=60, d=5, tiempo_minimo=15, tiempo_maximo=120):
        self.T = tiempo_inicial
        self.d = d
        self.tiempo_minimo = tiempo_minimo
        self.tiempo_maximo = tiempo_maximo
        self.historial = [tiempo_inicial]  # guardamos T_0, T_1, T_2... para poder graficarlo en el artículo

    def siguiente_tiempo(self, pistas_usadas):
        p = 4 - pistas_usadas
        nuevo_T = self.T - self.d * (4 - p)

        # Cota de diseño: nunca dejamos que el nivel sea injugable ni infinito
        nuevo_T = max(self.tiempo_minimo, min(nuevo_T, self.tiempo_maximo))

        self.T = nuevo_T
        self.historial.append(nuevo_T)
        return self.T

    def reiniciar(self, tiempo_inicial=None):
        """Vuelve a T_0, por ejemplo si el jugador empieza una partida nueva."""
        self.T = tiempo_inicial if tiempo_inicial is not None else self.historial[0]
        self.historial = [self.T]

