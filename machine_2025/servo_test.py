#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the servos
servo_pins = [12, 13, 18]

# Set up PWM for each servo pin
pwm = {}
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm[pin] = GPIO.PWM(pin, 50)  # 50Hz frequency for servos
    pwm[pin].start(0)  # Start with 0% duty cycle (servo at 0 position)

# Function to set the angle of the servo
def set_angle(servo, angle):
    duty_cycle = (angle / 18) + 2  # Formula to convert angle to duty cycle
    GPIO.output(servo, True)
    pwm[servo].ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo, False)
    pwm[servo].ChangeDutyCycle(0)

def sweep_servos():
    try:
        while True:
            # Sweep from 0 to 180 degrees and back
            for angle in range(0, 181, 10):  # Sweep from 0 to 180 in steps of 10
                for pin in servo_pins:
                    set_angle(pin, angle)
                time.sleep(0.5)  # Pause for a while before moving to the next angle

            for angle in range(180, -1, -10):  # Sweep back from 180 to 0 in steps of 10
                for pin in servo_pins:
                    set_angle(pin, angle)
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("Program interrupted")
        stop_servos()

# Function to stop PWM and clean up GPIO
def stop_servos():
    for pin in servo_pins:
        pwm[pin].stop()
    GPIO.cleanup()

if __name__ == "__main__":
    sweep_servos()

