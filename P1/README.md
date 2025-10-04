# Práctica 1 - Basic Vacuum Cleaner
Esta práctica implementa el control reactivo de una aspiradora robótica utilizando una máquina de estados finitos (FSM).
Mi objetivo es que la aspiradora se desplace de forma autónoma, limpiando el entorno mientras detecta y evita obstáculos mediante su sensor de colisión (bumper).

He utilizado la documentación de usuario de Unibotics para este ejercicio: https://jderobot.github.io/RoboticsAcademy/exercises/MobileRobots/vacuum_cleaner

## Descripción general
He diseñado un comportamiento de navegación en el que la aspiradora alterna entre tres estados principales:

- **Avanzar** para cubrir el área de limpieza.

- **Retroceder** cuando detecta una colisión.

- **Girar** para cambiar de dirección tras un obstáculo.

El sistema se ejecuta en un bucle continuo a 50 Hz, actualizando las velocidades lineal (V) y angular (W) mediante el módulo HAL.

## Funcionamiento de los estados
- **FORWARD** — Avance

En este estado la aspiradora se desplaza hacia adelante realizando un patrón de movimiento que combina:

Espiral:
Aumento progresivo de la velocidad lineal (v_forward) mientras mantiene un giro constante (W = 2.0), cubriendo el área de forma circular y eficiente.

Recta:
Avanza sin girar durante unos segundos para continuar la limpieza en línea recta y limpiar en otra zona.

Al finalizar ambas fases, el ciclo de avance se reinicia automáticamente.
Si el bumper detecta un obstáculo, la aspiradora cambia inmediatamente al estado BACKWARD.

- **BACKWARD** — Retroceso por colisión

Cuando la aspiradora detecta un choque, retrocede lentamente durante un tiempo determinado para alejarse del obstáculo.

Si vuelve a chocar mientras retrocede, interrumpe el retroceso y pasa directamente al estado TURN para girar y buscar una nueva trayectoria.

De esta forma evito que la aspiradora quede atascada entre obstáculos.

- **TURN** — Giro

Después de retroceder, la aspiradora realiza un giro sobre sí misma (V = 0.0, W = ±3.0) durante el tiempo necesario para rotar 90° (π/2 rad).

La dirección del giro (giro = ±1) se elige aleatoriamente, lo que le permite cambiar su trayectoria y explorar nuevas zonas del entorno sin seguir siempre el mismo patrón.
Al finalizar el giro, vuelve al estado FORWARD para continuar limpiando.


## Funcionamiento

https://github.com/user-attachments/assets/754486b6-0b23-4b84-b45d-54d19cbe3e7d

Tras un rato de ejecución obtenemos este resultado:

<img width="1103" height="329" alt="funcionamiento" src="https://github.com/user-attachments/assets/512b0a7b-839f-44d2-b417-10f7fa941581" />

