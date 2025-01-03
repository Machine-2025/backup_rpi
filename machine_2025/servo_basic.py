import pigpio
import time

# Initialisation des servos
pi = pigpio.pi()
SERVO_PINS = [12, 13, 18]
MIN_PULSE = 500
MAX_PULSE = 2500

ANGLE1 = 90
ANGLE2 = 120

def set_servo_angle(pin, angle):
    pulse_width = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
    pi.set_servo_pulsewidth(pin, pulse_width)

while True:
    for index in range(len(SERVO_PINS)):
        set_servo_angle(SERVO_PINS[index], ANGLE1)

    time.sleep(2)

    for index in range(len(SERVO_PINS)):
        set_servo_angle(SERVO_PINS[index], ANGLE2)
   
    time.sleep(2)

for pin in SERVO_PINS:
    pi.set_servo_pulsewidth(pin, 0)
pi.stop()
