# Práctica 4 - Global Navigation

Esta práctica implementa un sistema de navegación autónoma para un coche en un mapa 2D. El coche puede desplazarse hasta un destino seleccionado por el usuario mientras evita obstáculos y planifica un camino eficiente usando Gradient Path Planning.

He usado la documentación de Unibotics para la práctica: https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/global_navigation/

## Descripción

### Gradient Path Planning

Se ha implementado un algoritmo de propagación tipo *wavefront* basado en Breadth-First Search (BFS) utilizando `collections.deque`. El mapa se binariza inicialmente (`map_data > 127`) para diferenciar celdas libres (`1`) de obstáculos (`0`).

La propagación comienza en la celda destino con coste 0 y se expande hacia el resto del mapa evaluando los 8 vecinos definidos en la lista `neighbors`:

- Movimientos ortogonales: coste 1.0.

- Movimientos diagonales: coste `math.sqrt(2)`.

Para optimizar el rendimiento y no procesar el mapa entero en cada iteración, la expansión se detiene automáticamente una vez que la onda alcanza la posición del coche y supera un margen adicional controlado por el parámetro `extra_expansion=15` (`cost_limit = field[row, col] + extra_expansion`). El resultado es una matriz `field` (inicializada a `np.inf`) donde cada celda refleja el coste mínimo estimado hasta el objetivo.

### Penalización por proximidad a obstáculos

Para evitar que el coche trace rutas pegadas a las paredes o esquinas, se calcula la distancia euclidiana de cada celda libre al obstáculo más cercano mediante `scipy.ndimage.distance_transform_edt(~obstacle_mask)`.

A todas las celdas situadas a una distancia menor o igual a `radius=3` se les aplica una penalización fija (`penalty_value=25`). Esta matriz de penalización se suma directamente al campo (`combined = field + penalty`), generando un campo combinado y definiendo una zona segura (`safe_zone = (penalty == 0)`).

### Selección de subobjetivo

En lugar de apuntar directamente al destino final, en cada iteración se selecciona un subobjetivo local alrededor del coche. La función `subgoal` explora ventanas cuadradas crecientes definidas en `radii = [2, 3, 4, 5, 6, 8, 10]` centradas en la posición actual del vehículo.

Para elegir la celda con menor valor en el campo combinado, se aplican los siguientes filtros:

- Se descartan obstáculos (`value >= 1e9`) y celdas fuera de la `safe_zone`.

- Se ignoran celdas demasiado cercanas al robot mediante distancia Manhattan (`abs(d_row) + abs(d_col) < 2`).

- Histéresis: si la celda evaluada coincide con el `previous_subgoal`, su valor se reduce un 10% (`value *= 0.9`) para evitar cambios bruscos de objetivo entre iteraciones.

En cuanto se encuentra un candidato válido en un radio, se devuelve inmediatamente; si no se encuentra ninguno, se devuelve la posición actual.

### Control del coche

El subobjetivo seleccionado en coordenadas de cuadrícula se transforma a coordenadas del mundo real con `WebGUI.gridToWorld((subgoal_col, subgoal_row))`. A partir de la pose actual obtenida con `HAL.getPose3d()`, se calcula:
- La distancia euclidiana al subobjetivo (`math.hypot(dx, dy)`).
- El error angular normalizado entre -pi y pi usando `math.atan2(math.sin(angle_diff - robot_theta), math.cos(angle_diff - robot_theta))`.

Se aplica un control proporcional con ganancias `Kv = 7.0` y `Kw = 3.5`:
- Velocidad angular: `angular_velocity = Kw * error`.
- Velocidad lineal: se modula en función del error angular (`Kv * max(0.0, 1 - (abs(error)/math.pi))`), reduciéndose progresivamente en giros pronunciados. Además, si la distancia al subobjetivo es inferior a 0.3, se aplica un factor de frenado (`linear_velocity *= 0.4`).

Finalmente, el coche se detiene y reinicia el destino cuando la distancia en la cuadrícula entre el robot y el objetivo es menor a 2 celdas.

### Visualización

Para depurar y mostrar el funcionamiento del algoritmo en tiempo real, se genera una copia del campo combinado (`visualization = combined.copy()`). Las celdas correspondientes a muros o zonas no alcanzadas (`field >= 1e9`) se fijan a 0 (negro), y el resto de valores se normalizan al rango 0–255 en formato `np.uint8` para mostrarlos en la interfaz con `WebGUI.showNumpy(visualization)`.

## Problemas surgidos

- **Ajuste de ganancias del controlador**: Encontrar el equilibrio entre Kv y Kw ha sido complicado. Con valores altos de velocidad lineal, el coche tendía a oscilar o a frenar bruscamente al acercarse a muros, lo que llevó a modular la velocidad lineal según el error angular y añadir la reducción del 60% (`* 0.4`) cuando `distance < 0.3`.

- **Correspondencia de coordenadas entre interfaz y mapa**: Uno de los mayores inconvenientes ha sido la convención de ejes entre la interfaz y las matrices de `NumPy`. Fue necesario invertir las coordenadas al llamar a `WebGUI.rowColumn([target[1], target[0]])` y `WebGUI.rowColumn([pose.y, pose.x])`, así como pasar el subobjetivo en orden `(col, fila)` al convertirlo de vuelta con `WebGUI.gridToWorld((subgoal_col, subgoal_row))`.

- **Inestabilidad en el subobjetivo**: En determinadas zonas del mapa, el subobjetivo saltaba entre celdas cercanas o no apuntaba de forma estable hacia el destino. Esto se solucionó combinando la búsqueda por radios crecientes (`radii`), el descarte de celdas a distancia Manhattan menor que 2 y el factor de histéresis (0.9) sobre `previous_subgoal`.

## Vídeo
Aquí tenemos un ejemplo de ejecución marcando cuatro destinos:

https://github.com/user-attachments/assets/57094417-6a01-4524-8964-71b957473b70


