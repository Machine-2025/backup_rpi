#!/usr/bin/env python3
import board
import neopixel
import signal
from time import sleep


# Initialize NeoPixel object
pixels = neopixel.NeoPixel(board.D21, 1, brightness=1)

def clean_up():
    """Turn off all servos and NeoPixel."""
    pixels.fill((0, 0, 0))
    pixels.show()
    print("Clean-up completed. Exiting program.")


def signal_handler(sig, frame):
    """Handle termination signals."""
    print("\nTermination signal received. Cleaning up...")
    clean_up()

# Attach the signal handler to SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

def main():
    try:
        while True:
            #color is GRB
            # Set color to green
            pixels.fill((255, 0, 0))
            pixels.show()
            sleep(1)

            # Set color to red
            pixels.fill((0, 255, 0))
            pixels.show()
            sleep(1)

            # Set color to blue
            pixels.fill((0, 0, 255))
            pixels.show()
            sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        clean_up()

if __name__ == '__main__':
    main()
