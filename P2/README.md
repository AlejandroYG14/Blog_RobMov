# Práctica 2 - Visual Follow Line
El objetivo de esta práctica es implementar un control reactivo PID para que un coche de carreras sea capaz de seguir la línea pintada en el circuito.

He usado la documentación de Unibotics para este ejercicio: https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/follow_line/

## Descripción

### Detección del color rojo

Primero convierto la imagen de la cámara de **BGR a HSV** con OpenCV, porque este espacio de color facilita la segmentación por tono.  
Uso dos rangos de umbrales para detectar el color rojo, ya que el rojo se encuentra tanto en los valores bajos como en los altos del espacio HSV.

```python
min1 = np.array([0, 100, 100])
max1 = np.array([10, 255, 255])
min2 = np.array([170, 100, 100])
max2 = np.array([180, 255, 255])
```
Combino ambas máscaras (mask1 y mask2) con una operación bitwise_or, y después calculo el centroide de la región roja en la mitad inferior de la imagen (ROI).
Este centroide representa el punto medio de la línea que el coche debe seguir.

### Control del giro (PID angular)

El error angular se calcula como la distancia en píxeles entre el centro de la imagen y el centroide detectado.
Con ese error aplico un control PID:
- P: corrige el error actual.
- I: acumula errores persistentes para eliminar sesgos.
- D: suaviza las oscilaciones anticipando el cambio de error.

El resultado del PID se traduce en una velocidad angular W que mantiene el coche centrado sobre la línea.

### Control de velocidad (PD lineal)

La velocidad lineal depende del valor absoluto del error angular.
Cuando el coche está bien alineado (error pequeño), acelera; cuando el error aumenta, reduce la velocidad para evitar salirse.

Esto me permite tener una conducción fluida, más rápida en rectas y más controlada en curvas.

### Recuperación ante pérdida de la línea

Si la línea no se detecta:
- Atenúo el acumulador integral para evitar saturación.
- Reseteo los errores previos.
- Hago que el coche retroceda ligeramente

De esta forma, el coche puede recuperarse automáticamente si la cámara deja de ver la línea.

## Problemas
Durante el desarrollo de esta práctica me encontré con varios problemas que conseguí solucionar:

### Ajuste de los parámetros PID

El principal problema fue encontrar los valores adecuados del PID.
Cada vez que cambiaba la velocidad base del coche, era necesario reajustar los tres parámetros, ya que el comportamiento dinámico variaba mucho.
Empecé con una velocidad baja para lograr estabilidad y, poco a poco, fui aumentando la velocidad hasta conseguir reducir el tiempo de vuelta a menos de un minuto.
Ha sido un proceso de prueba y error bastante largo, pero fundamental para lograr un seguimiento preciso.

### Rendimiento del simulador y GPU

Al ejecutar el contenedor Docker sin acceso a la GPU, el simulador funcionaba solo con la CPU, lo que reducía los FPS y afectaba directamente el tiempo real de ejecución del coche.
Cuando empecé a ejecutarlo con la aceleración GPU los FPS y el Real Time Factor incrementaron y pude seguir sin problemas. 

### Carga de la CPU y frecuencia del bucle

También observé que, dependiendo de la carga de la CPU, el coche se comporta de forma diferente.
Cuando el procesador está sobrecargado, la frecuencia del bucle de control no se mantiene constante, lo que hace que el coche responda peor y aumenten las oscilaciones.

## Vídeos
En este vídeo se observa cómo el coche completa una vuelta al circuito en 53 segundos. Sin embargo, el mejor tiempo no lo he grabado, que han sido 50 segundos.



En este otro vídeo se observa cómo el coche se recupera al perder la línea.



