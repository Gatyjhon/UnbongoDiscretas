# DiscreteUbongo

Videojuego de rompecabezas 2D inspirado en Ubongo, desarrollado como proyecto
final del curso Matemáticas Discretas I (Universidad Nacional de Colombia).

## Requisitos

- Python 3.10+
- pip
-git

## Instalación

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Pruebas por consola (sin Pygame)

```bash
python tests/test_solver.py
python tests/test_temporizador.py
```

## Estructura del proyecto

```
motor_matematico/   Lógica pura (combinatoria, backtracking, recurrencias). No depende de Pygame.
interfaz/            Renderizado y manejo de eventos con Pygame.
tests/                Pruebas de consola de los módulos matemáticos.
docs/                 Documentación de soporte matemático (para el artículo técnico).
```

## Controles

- Click y arrastre: mover una pieza sobre el tablero.
- Soltar el click sobre una posición válida: coloca la pieza.
- Tecla `R`: rota/refleja la pieza activa a su siguiente configuración.
- Tecla `H`: pide una pista (usa el mismo backtracking del solver).

## Estado actual del proyecto

_(Se tiene una version ya terminada pulida del videojuego)_

## Integrantes y aportes

_(Proyecto individual por John Angel Novoa Martinez)_
