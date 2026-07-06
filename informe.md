# Informe: Funcion De Utilidad Heuristica

## Contexto

Knight Energy usa minimax con profundidad limitada porque no se explora el arbol completo de la partida. La profundidad depende del nivel seleccionado:

- Principiante: profundidad 2.
- Amateur: profundidad 4.
- Experto: profundidad 6.

La maquina juega con el caballo blanco y maximiza la utilidad. El jugador humano usa el caballo negro y minimiza la utilidad de la maquina.

## Funcion Heuristica

La utilidad evalua un estado desde el punto de vista de la maquina:

```text
utility = 10 * (machine_score - human_score)
        + 2 * (machine_energy - human_energy)
        + machine_reachable_item_bonus
        - human_reachable_item_bonus
        - machine_energy_risk_penalty
        + human_energy_risk_penalty
```

## Componentes

La diferencia de puntos es el factor dominante porque el objetivo final es terminar con mas puntos que el adversario. Por eso se multiplica por 10: una ventaja real en puntos debe pesar mas que una ventaja temporal de energia.

La diferencia de energia se multiplica por 2. La energia no gana la partida directamente, pero permite seguir moviendo el caballo y evita penalizaciones de turno. Una ventaja de energia representa mayor movilidad futura.

El bono por items alcanzables valora las casillas que el jugador puede tomar en un movimiento. Las estrellas alcanzables suman `valor * 3`, porque capturarlas cambia el puntaje de inmediato. Las casillas de energia alcanzables suman `valor * 2` solo cuando el jugador tiene poca energia, ya que en ese caso recuperar energia evita quedarse sin turnos.

La penalizacion por riesgo energetico castiga estados donde un jugador tiene energia muy baja. Con 0 energia se aplica una penalizacion alta porque el jugador perdera el turno y recibira -3 puntos. Con 1 energia se aplica una penalizacion menor porque despues del siguiente movimiento puede quedar bloqueado.

## Justificacion

La heuristica combina objetivos inmediatos y futuros. Los puntos reflejan la condicion de victoria. La energia refleja la capacidad de continuar jugando. Los bonos por items cercanos hacen que la maquina prefiera oportunidades concretas del tablero, y las penalizaciones por energia evitan decisiones que dejan al caballo sin capacidad de actuar.

Como minimax alterna entre maximizar y minimizar, esta utilidad permite que la maquina busque estados buenos para ella y anticipe respuestas que favorecen al jugador humano.
