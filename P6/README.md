# Práctica 6 - Marker Based Visual Loc

El objetivo de esta práctica es estimar la posición y orientación (pose) de un robot en un mapa 2D mediante la detección y el análisis de marcadores visuales, concretamente AprilTags.

He usado la documentación de Unibotics para la práctica: https://jderobot.github.io/RoboticsAcademy/exercises/ComputerVision/marker_visual_loc

## Descripción

### Sistema de visión y calibración

Utilizo la librería ```pyapriltags``` para la detección de marcadores en la imagen. He configurado el sistema de la siguiente manera:
- Modelo de cámara: Configuración de una matriz de cámara intrínseca adaptativa en base al tamaño del frame de vídeo, aplicando un factor de escala focal de `0.87 * w`.

- Transformaciones geométricas (PnP): Cuando hay tags en el campo de visión, el sistema calcula el área de cada una y selecciona exclusivamente la baliza más grande (más cercana), garantizando precisión geométrica.

- Con la baliza óptima seleccionada, se ejecuta el algoritmo Perspective-n-Point (`cv2.solvePnP`) empleando los puntos tridimensionales fijos del tag (`object_points`).

- La matriz resultante se invierte y se compone con la matriz de pose absoluta del tag obtenido del mapa global (`tags_world`). Finalmente, se realiza un cambio y reajuste de ejes espaciales (de OpenCV al sistema del robot) para extraer las coordenadas globales finales (`est_x`, `est_y`, `est_yaw`).

### Algoritmo de localización

Se ha diseñado un enfoque que combina la corrección visual con la estimación incremental por odometría:

- Estimación visual (Prioritaria): Si hay algún tag en pantalla, la pose del robot se sobrescribe directamente con el cálculo absoluto derivado del PnP de la baliza más grande. Esta pose se almacena en `global_estimated_pose` y sirve como nueva base de referencia.

- Navegación ciega: Cuando el robot pierde de vista los tags, la odometría absoluta de HAL no se usa directamente, ya que acumularía error o desvíos con respecto al mapa global. En su lugar, el algoritmo calcula frame a frame la diferencia de desplazamiento ocurrida en esa única iteración del bucle (`odom - last_odom`). Estos diferenciales (`delta_x`, `delta_y`, `delta_yaw`) se suman de manera acumulativa a la última pose estimada por visión, manteniendo una trayectoria continua y suave en zonas ciegas.

### Navegación

El comportamiento de exploración del entorno está gobernado por una máquina de estados finitos que guía al robot deambulando por el espacio. Los estados se gestionan a través de la variable `explore_state`:

- `WANDER_FWD`: El robot se desplaza en línea recta (`HAL.setV(0.5)`) explorando el mapa doméstico en busca de balizas. Permanece en este estado hasta que el sensor láser detecta una pared u obstáculo frontal por debajo del umbral de seguridad definido en `OBSTACLE_THRESHOLD`.

- `PLAN_TURN`: Se activa inmediatamente tras detectar un obstáculo frontal. El robot se detiene por completo y calcula de forma aleatoria un nuevo rumbo objetivo (`goal_yaw`) basándose en su orientación actual y un desfase limitado por `MAX_YAW_DELTA`. Una vez fijado el rumbo, transiciona al siguiente estado.

- `EXECUTE_TURN`: El robot rota sobre su propio eje central a velocidad angular controlada. Se calcula la distancia angular más corta hacia el objetivo mediante `shortest_angle_diff`. Para suavizar la maniobra y evitar sobreoscilaciones, se aplica un control de velocidad proporcional acotado por `MAX_ANGULAR_VEL`. Cuando el error de rumbo entra dentro de la tolerancia permitida (`YAW_TOLERANCE`), el robot se detiene y regresa al estado `WANDER_FWD` para continuar su marcha.

### Procesamiento de sensores
- Láser: Se implementa la función `check_front_obstacle` de manera adaptativa. Analiza las muestras centrales del array de distancias para cubrir el sector frontal de avance del robot, filtrando lecturas fuera de rango o inferiores a la distancia mínima física del propio chasis (`LASER_MIN_DIST`).

- Odometría y cálculos: Los cálculos angulares están protegidos contra desbordamientos matemáticos mediante `normalize_angle` y `shortest_angle_diff`, lo que asegura que las transiciones de -pi a +pi no generen discontinuidades ni giros infinitos en el robot. Los datos de odometría del entorno se tratan como incrementos relativos.

- Gestión del mapa: Al arrancar el script, se parsea el archivo de configuración estructurado en formato YAML (`apriltags_poses.yaml`) que contiene las matrices de transformación RT y posiciones absolutas tridimensionales de cada AprilTag del escenario.

## Vídeos
En estos vídeos se muestra la práctica funcionando en diferentes ejecuciones:


https://github.com/user-attachments/assets/ac093c22-53e6-40c2-89ec-86453aa5fa69


https://github.com/user-attachments/assets/390aafc7-65da-4e1c-8730-49e85b0c7153


https://github.com/user-attachments/assets/ae895500-31e4-402c-88e8-016f7786cd1f


## Conclusión
He logrado integrar la localización visual precisa con una navegación reactiva robusta, permitiendo al robot operar de forma autónoma en el entorno.

