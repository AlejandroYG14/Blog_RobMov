# Práctica 5 - Laser Mapping
El objetivo de esta práctica es desarrollar un algoritmo de navegación que permita a un robot explorar de forma autónoma un entorno de almacén y generar al mismo tiempo un mapa preciso de la zona utilizando datos del sensor LIDAR.

He usado la documentación de Unibotics para la práctica: https://jderobot.github.io/RoboticsAcademy/exercises/MobileRobots/laser_mapping

## Descripción

### Mapeado mediante grid de ocupación

He implementado un mapa de ocupación basado en log-odds (evidencias). Para cada celda mantengo un valor que representa la probabilidad de que dicha celda esté ocupada o libre. Este mapa tiene un tamaño fijo y se actualiza en coordenadas de píxel usando la conversión ```WebGUI.poseToMap(x, y, yaw)```.

Para actualizar el mapa:

1. Obtengo la pose del robot y los datos del láser.
2. Recorro todos los ángulos del láser y convierto cada medida en una coordenada global.
3. Trazo un rayo desde la posición del robot hasta el punto final detectado usando un algoritmo de Bresenham.
4. Las celdas intermedias del rayo las marco como libres y la celda final como ocupada si realmente había un obstáculo.
5. Los valores de log-odds están acotados para evitar saturaciones numéricas.
6. Solo actualizo el mapa cuando el robot se ha desplazado una distancia mínima, reduciendo así el coste computacional y evitando marcar varias veces el mismo rayo.

Además, genero un mapa donde las celdas libres se representan blancas, las ocupadas negras y las desconocidas con un gris intermedio.

### Navegación reactiva con sensor láser

He implementado un comportamiento de navegación reactivo basado en el láser. Este módulo funciona continuamente y toma decisiones inmediatas según la presencia de obstáculos. La lógica que he seguido es la siguiente:

1. Si detecto un obstáculo cerca justo delante o hacia la izquierda, giro a la izquierda.
2. Si detecto un obstáculo cerca hacia la derecha, giro a la derecha.
3. Si no detecto ningún obstáculo cercano, avanzo recto.

Este comportamiento asegura que el robot siempre se mueva hacia zonas despejadas. El sistema reajusta continuamente su velocidad lineal y angular para responder a cualquier cambio en el entorno.

### Rayos virtuales y decisiones de giro

Además del láser real, he implementado rayos virtuales que simulan hacia dónde podría avanzar el robot. Utilizo estos rayos para evaluar qué lado del robot ofrece más espacio libre y decidir giros cuando el entorno está muy cerrado o aparecen obstáculos inesperados. Esto permite tomar mejores decisiones cuando la navegación reactiva simple no es suficiente.

### Integración del mapa con la navegación

El mapa de ocupación se actualiza en paralelo a la navegación. Aunque el movimiento del robot es puramente reactivo, el sistema genera de forma continua un mapa coherente del entorno. De este modo consigo una arquitectura similar a un SLAM simplificado donde no existe planificación global, pero sí una representación del entorno en construcción constante.

### Bucle principal del sistema

El bucle de control se compone de tres tareas que se repiten a alta frecuencia:

1. Ejecuto el módulo de navegación reactiva.
2. Actualizo el mapa de ocupación si el robot se ha movido lo suficiente.
3. Envío el mapa resultante a la interfaz gráfica.
4. Mientras el programa está activo, el robot continúa moviéndose, mapeando y ajustando su trayectoria para evitar colisiones.

### Vídeo
Aquí tenemos un ejemplo de ejecución:


### Conclusión
Con este ejercicio he creado un sistema que combina navegación reactiva y mapeado probabilístico. El robot es capaz de moverse de manera autónoma sin un objetivo previo, evitando obstáculos y construyendo al mismo tiempo un mapa detallado del entorno
