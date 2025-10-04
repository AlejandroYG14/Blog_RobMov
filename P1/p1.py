import WebGUI
import HAL
import Frequency
import math
import time
import random

# Estados posibles
state = "FORWARD"

forward_start_time = time.time()
backward_start_time = 0
turn_start_time = 0

v_forward = 1.0
v_increment = 0.001
spiral_duration = 5.0
straight_duration = 2.0

backward_duration = 1.5
turn_speed = 3.0
turn_angle = math.pi / 2

# Dirección de giro
giro = 1

while True:
    dt = Frequency.tick(50)
    now = time.time()

    bumper = HAL.getBumperData().state

    if bumper == 1:
        if state != "BACKWARD":
            state = "BACKWARD"
            backward_start_time = now
        else:
            # más tiempo para alejarse
            backward_start_time = now

        HAL.setV(-0.5)
        HAL.setW(0.0)
        continue

    if state == "FORWARD":
        elapsed = now - forward_start_time

        if elapsed < spiral_duration:
            # Fase espiral
            v_forward += v_increment
            HAL.setV(v_forward)
            HAL.setW(2.0)

        elif elapsed < spiral_duration + straight_duration:
            # Fase recta
            HAL.setV(1.5)
            HAL.setW(0.0)

        else:
            forward_start_time = now
            v_forward = 1.0

    elif state == "BACKWARD":
        HAL.setV(-0.5)
        HAL.setW(0.0)

        if now - backward_start_time > backward_duration:
            state = "TURN"
            turn_start_time = now
            giro = 1 if random.random() < 0.5 else -1

    elif state == "TURN":
        HAL.setV(0.0)
        HAL.setW(turn_speed * giro)

        # Tiempo necesario para girar 90° a w=3 rad/s
        if now - turn_start_time > (turn_angle / turn_speed):
            state = "FORWARD"
            forward_start_time = now
            v_forward = 1.0
