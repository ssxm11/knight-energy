# Knight Energy Design

## Objetivo

Construir el juego Knight Energy con Pygame, usando los assets del proyecto para representar el tablero, los caballos, las estrellas y las casillas de energia. La maquina juega siempre primero con el caballo blanco; el jugador humano usa el caballo negro.

## Reglas Del Juego

- El tablero es de 8 x 8.
- Las posiciones iniciales de los caballos, estrellas y energia se generan aleatoriamente sin solaparse.
- Cada jugador inicia con 7 unidades de energia y 0 puntos.
- En cada turno, el jugador activo mueve su caballo en L, siguiendo las reglas del ajedrez.
- Cada movimiento cuesta 1 unidad de energia.
- Si el caballo cae en una estrella, suma su valor a los puntos del jugador y la estrella se consume.
- Si el caballo cae en una casilla de energia, suma su valor a la energia del jugador y la casilla se consume.
- Las estrellas tienen valores 2, 3, 4, 5, 6, 8 y 9.
- Las casillas de energia tienen valores 2, 3, 4 y 5.
- Si un jugador no tiene energia suficiente para mover, pierde el turno y se le descuentan 3 puntos.
- El juego termina cuando no quedan estrellas o cuando ambos jugadores no pueden realizar movimientos.
- Gana quien tenga mas puntos al finalizar. Si los puntajes son iguales, hay empate.

## Arquitectura

La implementacion separara la logica del juego de la interfaz Pygame.

- `main.py`: punto de entrada de Pygame y ciclo principal.
- `knight_energy/game.py`: estado del juego, transiciones de turno, consumo de objetos y condiciones de fin.
- `knight_energy/models.py`: estructuras para jugadores, items del tablero, posiciones y niveles de dificultad.
- `knight_energy/rules.py`: movimientos validos del caballo y utilidades de tablero.
- `knight_energy/ai.py`: minimax con profundidad limitada y funcion heuristica.
- `knight_energy/ui.py`: renderizado del tablero, panel de estado, pantallas de seleccion y resultado.
- `tests/`: pruebas automatizadas de la logica pura.

Esta separacion permite probar las reglas y la IA sin abrir una ventana de Pygame.

## Flujo De Juego

Al iniciar, el usuario elige dificultad:

- Principiante: minimax a profundidad 2.
- Amateur: minimax a profundidad 4.
- Experto: minimax a profundidad 6.

Luego se crea una partida aleatoria. La maquina calcula su movimiento con minimax y lo ejecuta. El jugador humano selecciona un movimiento valido para su caballo. El juego alterna turnos hasta cumplir una condicion de fin y muestra el ganador o empate.

## Interfaz Visual

El tablero seguira el estilo de `tablero-ejemplo.png`: una grilla de ajedrez clara, caballos mediante assets, estrellas con `assets/star.png` y energia con `assets/lighting.png`.

Cada estrella y cada energia mostrara su valor numerico al lado del icono dentro de la casilla. En todo momento se mostraran los puntos y energia disponibles de cada jugador, el turno actual y mensajes relevantes como perdida de turno o fin de juego.

## Inteligencia Artificial

La IA usara minimax con decisiones imperfectas por limite de profundidad. La maquina maximiza su utilidad y el humano minimiza la utilidad de la maquina.

La heuristica combinara:

- Diferencia de puntos entre maquina y humano.
- Diferencia de energia.
- Valor potencial de estrellas cercanas.
- Valor potencial de energia cercana si el jugador tiene energia baja.
- Penalizacion por estados sin energia o sin movimientos utiles.

El informe explicara la funcion heuristica, sus componentes y por que esos factores aproximan una buena posicion.

## Pruebas

Las pruebas cubraran:

- Generacion de movimientos validos de caballo.
- Rechazo de movimientos fuera del tablero.
- Inicializacion aleatoria sin posiciones repetidas.
- Consumo de estrellas y energia.
- Costo de energia por movimiento.
- Penalizacion por turno sin energia.
- Condiciones de fin del juego.
- Profundidad de minimax segun dificultad.
- Eleccion de un movimiento basico favorable para la maquina.

## Commits Planeados

- `docs: add knight energy design spec`
- `feat: add game domain and rules`
- `feat: add minimax ai`
- `feat: add pygame board ui`
- `feat: integrate gameplay loop`
- `docs: add heuristic report`

