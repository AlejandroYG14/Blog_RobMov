# Práctica 3 - Obstacle Avoidance

El objetivo de esta práctica es implementar la lógica del algoritmo de navegación VFF, haciendo que un coche de carreras pueda completar un circuito sin chocar con obstáculos.

He usado la documentación de Unibotics para este ejercicio: https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/obstacle_avoidance

## Descripción
Este ejercicio implementa un sistema de navegación reactiva utilizando el método de campos de fuerzas virtuales (VFF). El coche se desplaza hacia una serie de objetivos evitando obstáculos detectados mediante un sensor láser, combinando fuerzas atractivas y repulsivas que determinan su movimiento en tiempo real, sin necesidad de utilizar un mapa global del entorno.

He priorizado que el coche se mueva de manera segura y eficiente hacia los distintos objetivos, aunque no tarda demasiado en completar el circuito.

El sistema se basa en el cálculo de vectores de fuerza:

- **Fuerza atractiva**: dirige al coche hacia el objetivo. Su magnitud se ajusta para evitar valores extremos, limitando tanto su crecimiento cuando el objetivo está lejos como su reducción excesiva cuando está muy cerca.

- **Fuerza repulsiva**: aleja al coche de los obstáculos detectados dentro de un radio de influencia definido. Su intensidad depende de la distancia al obstáculo más próximo.

- **Fuerza resultante**: combina ambas influencias y determina la dirección y velocidad de avance del coche.

Estos vectores se visualizan en tiempo real en la interfaz usando `WebGUI.showForces`

Se procesan de forma continua los datos del sensor láser para identificar los obstáculos más cercanos dentro de un radio de influencia.

He aplicado ponderaciones variables (`alpha` y `beta`) para las fuerzas atractiva y repulsiva, de modo que cuando el coche detecta obstáculos próximos da prioridad a la evasión, y cuando el camino está despejado incrementa la atracción hacia el objetivo.

## Problemas
### Aumento de la velocidad y riesgo de colisión
Al principio, al intentar que el coche se desplazara más rápido, aparecieron problemas de estabilidad y evasión de obstáculos. La mayor velocidad hacía que el sistema reaccionara tarde ante los obstáculos cercanos, provocando colisiones. Tras varios ajustes, encontré una velocidad manejable que permitió mantener la seguridad.

### Ajuste de las ponderaciones `alpha` y `beta`
Encontrar los valores adecuados ha sido uno de los mayores problemas. Con valores inadecuados, el coche podía moverse de forma errática o mostrarse demasiado conservador, reduciendo su eficiencia.

### Crecimiento excesivo del vector atractivo
Al aproximarse a algunos objetivos, el vector de atracción aumentaba demasiado, generando giros bruscos o trayectorias inestables, especialmente en curvas. Para resolverlo, establecí una limitación en la magnitud máxima del vector atractivo, garantizando un comportamiento más controlado y seguro.

### Debilitamiento del vector atractivo en distancias cortas
Cuando el coche se encontraba muy cerca del objetivo, el vector atractivo se volvía demasiado pequeño, lo que podía hacer que el coche se detuviera antes de alcanzarlo completamente. Para corregirlo, establecí también una magnitud mínima, asegurando que el coche mantuviera impulso suficiente hasta completar la llegada al objetivo.

## Vídeos
Este es el funcionamiento de la práctica, tarda en terminar el circuito ya que he dado más importancia a la seguridad.

https://github.com/user-attachments/assets/bd27a004-6554-4e1e-8202-b888cf8092b7

Este es el mismo vídeo pero con la velocidad aumentada:

https://github.com/user-attachments/assets/2379f652-7c80-4efc-b374-48bff990a194

## Conclusiones
En conclusión, he conseguido un sistema de navegación local reactiva estable y eficiente, asegurando la seguridad.
