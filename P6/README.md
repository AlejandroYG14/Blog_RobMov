# Práctica 6 - Marker Based Visual Loc

El objetivo de esta práctica es estimar la posición y orientación (pose) de un robot en un mapa 2D mediante la detección y el análisis de marcadores visuales, concretamente AprilTags.

He usado la documentación de Unibotics para la práctica: https://jderobot.github.io/RoboticsAcademy/exercises/ComputerVision/marker_visual_loc

## Descripción

### Sistema de visión y calibración

Utilizo la librería ```pyapriltags``` para la detección de marcadores en la imagen. He configurado el sistema de la siguiente manera:
- Modelo de cámara: Defino una matriz de cámara intrínseca basada en las dimensiones de la imagen recibida.

- Transformaciones geométricas: He implementado una cadena cinemática completa para transformar la posición relativa del tag detectado a la posición global del robot. Para ello:
  - He aplicado una corrección de la inclinación de la cámara (Pitch) en la matriz de rotación inicial.
  - Alineo los ejes de coordenadas de visión (OpenCV) con los del robot usando la matriz ```T_cv_fix```.
  - Utilizo la función ```rpy_to_rot``` para manejar las rotaciones en el espacio 3D.

### Algoritmo de localización

He diseñado un enfoque híbrido para determinar la pose del robot:
- Estimación visual (PnP): Cuando se detecta un tag válido dentro del rango (```MAX_VISUAL_RANGE```), utilizo el algoritmo Perspective-n-Point (```cv2.solvePnP```) con los puntos del objeto (```object_points```) para obtener la posición precisa.
- Corrección de odometría: Calculo la diferencia (offset) entre la posición reportada por la odometría bruta (```HAL.getOdom```) y la posición visual calculada.
- Navegación ciega: Cuando no hay tags visibles, mantengo la localización sumando el último offset calculado a la odometría actual.

### Navegación

He gobernado el comportamiento del robot mediante una máquina de estados. Gestiono los estados a través de la variable ```nav_state```:
- Estado **AVOID**:
  - He programado que se active si el sensor láser detecta cualquier obstáculo por debajo de un umbral crítico.
  - En este estado, el robot ejecuta una maniobra de retroceso y giro.
  - Utilizo histéresis para evitar oscilaciones en el comportamiento.

- Estado **ADVANCE** :
  - He configurado que se active automáticamente cuando la variable ```tag_detected``` es verdadera.
  - He implementado un controlador proporcional que ajusta la velocidad angular basándose en el error horizontal del centro del tag en la imagen (```error_x```).

    Esto permite al robot alinearse y avanzar hacia la baliza.

- Estado **SEARCH**:
  - He implementado un ciclo temporizado con ```search_timer``` que alterna entre dos fases:
    - Giro (```SEARCH_SPIN```): El robot gira para buscar un tag.
    - Desplazamiento (```SEARCH_MOVE```): El robot avanza brevemente para cambiar de zona.

    Incluyo una comprobación con el láser (```min_front```) para abortar el avance y volver a girar si se detecta una pared, evitando activar el estado AVOID innecesariamente.

### Procesamiento de sensores
- Láser: Uso la función ```parse_laser_data``` para convertir las lecturas a coordenadas polares, lo que me permite analizar distancias en diferentes sectores.
- Odometría: Normalizo los ángulos utilizando la función ```normalize_angle``` y promedio las orientaciones visuales con ```circular_mean``` para evitar errores matemáticos.
- Gestión de mapa: Cargo la configuración de las balizas desde un archivo YAML, almacenando sus posiciones en la variable ```tags_world```.

## Vídeo
En este vídeo se muestra la práctica funcionando:

https://github.com/user-attachments/assets/79595034-6dff-4014-904b-56cd077adcc1


## Conclusión
He logrado integrar la localización visual precisa con una navegación reactiva robusta, permitiendo al robot operar de forma autónoma en el entorno.

