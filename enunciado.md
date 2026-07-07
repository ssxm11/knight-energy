

Universidad del Valle
Facultad de Ingeniería
Escuela de Ingeniería de Sistemas y Computación
## Inteligencia Artificial
## Proyecto 2

Knight  energy es  un  juego  entre  dos  adversarios  en  el  que  cada  uno  controla  un  caballo
sobre un tablero de ajedrez. En el tablero hay siete casillas con puntos, representadas por el
símbolo  , y cuatro casillas especiales que permiten recuperar energía, representadas por el
símbolo  . Cada jugador inicia con una cantidad limitada de energía que se consume a medida
que realiza movimientos. Las casillas con puntos tienen los siguientes valores: 2, 3, 4, 5, 6, 8, y
-  Cada  valor  aparece  exactamente  una  vez  en  el  tablero.  Las  casillas  de  energía  tienen  los
siguientes valores: 2, 3, 4, y 5.

Cada jugador inicia el juego con 7 unidades de energía. En cada turno, un jugador debe mover
su caballo a una nueva posición siguiendo las reglas del ajedrez. Cada movimiento tiene un costo
de 1 unidad de energía. Si el caballo llega a una casilla con puntos, el jugador obtiene la cantidad
indicada en ella. Si el caballo llega a una casilla de energía, aumenta su energía en esa cantidad.
Las casillas con puntos y las casillas de energía se consumen al ser utilizadas y no pueden volver
a ser usadas por ningún jugador. Si durante su turno un jugador no tiene energía suficiente para
realizar un movimiento, pierde el turno y se le descuentan 3 puntos. El juego continúa mientras
el otro jugador tenga movimientos disponibles. El juego termina cuando no queden casillas con
puntos  o  cuando  ninguno  de  los  jugadores  pueda  realizar  movimientos.  Gana  el  jugador  que
acumule la mayor cantidad de puntos al finalizar la partida. A continuación, se muestra un posible
estado inicial del juego.



Knight  energy presenta tres niveles  de  dificultad (principiante,  amateur, y  experto) que  el
usuario puede seleccionar al iniciar el juego. Se debe construir un árbol minimax con decisiones
imperfectas. La profundidad límite del árbol depende del nivel seleccionado por el usuario. Para
el nivel principiante se utiliza un árbol de profundidad 2, para amateur de profundidad 4, y para
experto de profundidad 6.


Aclaraciones generales:

- El juego siempre lo inicia la máquina quien jugará con el caballo blanco.
- Las  posiciones  iniciales  de  los  caballos,  de  las  casillas  con  puntos,  y  de  las  casillas  de  energía,  son
aleatorias y no pueden coincidir.
- Se debe mostrar en cada momento la cantidad de puntos y la energía disponible de cada jugador.
- Al finalizar el juego se debe indicar quién es el ganador o si hubo empate.
- Los caballos se mueven en L siguiendo las reglas del ajedrez.

Además de desarrollar el juego, debe presentar un informe donde se defina y explique la función
de utilidad heurística que se utiliza en el algoritmo minimax.