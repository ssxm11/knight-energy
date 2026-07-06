# Knight Energy

Juego en Pygame para el proyecto de Inteligencia Artificial. La maquina juega primero con el caballo blanco y usa minimax con profundidad segun dificultad.

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
python main.py
```

Selecciona una dificultad en la pantalla inicial:

- Principiante: profundidad 2.
- Amateur: profundidad 4.
- Experto: profundidad 6.

Durante la partida, haz clic en una casilla resaltada para mover el caballo negro. Presiona `R` para volver al menu despues de terminar una partida.

## Pruebas

```bash
python -m pytest -v
```

## Informe

La explicacion de la funcion heuristica usada por minimax esta en `informe.md`.
