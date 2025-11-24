# Práctica 4 - Global Navigation

Esta práctica implementa un sistema de navegación autónoma para un coche en un mapa 2D. El coche puede desplazarse hasta un destino seleccionado por el usuario mientras evita obstáculos y planifica un camino eficiente usando Gradient Path Planning.

He usado la documentación de Unibotics para la práctica: https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/global_navigation/

## Descripción
### Gradient Path Planning

He utilizado un algoritmo de propagación tipo *wavefront*, basado en Gradient Path Planning. La propagación calcula un campo de costes desde la celda destino hasta el resto del mapa usando BFS (Breadth-First Search). Se consideran los vecinos en las ocho direcciones, teniendo las diagonales un coste de raíz de 2: `math.sqrt(2)`. La expansión se limita mediante un umbral adicional tras alcanzar la posición del coche, optimizando el rendimiento y reduciendo el área procesada.

El resultado es un campo de potencial donde cada celda indica el coste aproximado para llegar desde el destino.

### Penalización por proximidad a obstáculos

He calculado la distancia a los obstáculos usando la transformada euclidiana. Las celdas dentro de un radio definido recibieron una penalización, creando zonas de seguridad alrededor de muros y evitando que el subobjetivo se acercara demasiado a paredes o estrechamientos. Esta penalización se suma al campo de ondas para obtener un campo combinado

### Selección de subobjetivo

En lugar de dirigir el coche directamente al destino, he seleccionado un subobjetivo cercano. He evaluado anillos concéntricos alrededor de la posición del coche y he escogido la celda con menor valor en el campo combinado, asegurando que fuera transitable, segura y suficientemente alejada del coche. He aplicado una pequeña histéresis para mantener la estabilidad.

### Control del coche

El controlador calcula el error angular entre la orientación del coche y la dirección del subobjetivo. He aplicado control proporcional para la velocidad angular y modulado la velocidad lineal según el error angular y la distancia al subobjetivo.

### Visualización

He generado una representación del campo combinado normalizado, mostrando con `WebGUI.showNumpy` los muros en negro y las zonas libres con valores relativos de coste.

## Problemas surgidos

- Ajustar las ganancias del controlador lineal y angular ha sido complicado; cuando subía demasiado la velocidad lineal, el coche oscilaba o frenaba bruscamente cerca de muros.

- Un gran problema ha sido la correspondencia entre las coordenadas de la interfaz gráfica y las del mapa, y he tenido que invertir ejes y convertir filas y columnas.

- En algunas ocasiones, el subobjetivo no apuntaba exactamente al destino que había marcado, así que he aplicado histéresis y límites de radio para estabilizar la trayectoria.

## Vídeo
Aquí tenemos un ejemplo de ejecución marcando cuatro destinos:

https://github.com/user-attachments/assets/57094417-6a01-4524-8964-71b957473b70


## Conclusión
Finalmente, he conseguido diseñar un sistema de navegación global seguro y eficiente.

