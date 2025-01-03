import pigpio
import time
import struct
import board
from pyrf24 import RF24, RF24_PA_HIGH
import neopixel
import serial
from time import sleep
import sys


# Configuration du port série
port = "COM10"  # Remplacez par le port série de votre Arduino
baud_rate = 115200  # Baud rate pour la communication UART
delay_between_commands = 0.25  # Délai entre chaque commande (en secondes)

# Variables pour stocker les informations actuelles
current_color = "NULL"
passenger_counts = {"RED": 0, "GREEN": 0, "BLUE": 0, "YELLOW": 0, "PURPLE": 0}

# Liste des couleurs valides
valid_colors = ["RED", "GREEN", "BLUE", "YELLOW", "PURPLE"]

# Servo Initialization
pi = pigpio.pi()
SERVO_PINS = [12, 13, 18]
MIN_PULSE = 500
MAX_PULSE = 2500

# RF24 Initialization
radio = RF24(22, 0)  # CE pin is 22, CSN pin is 0
address = b"00002"  # Address for communication

class PackageNRF:
    struct_format = '<hhccH'  # Format: 2 signed shorts, 2 chars, 1 unsigned short (total: 8 bytes)
    size = struct.calcsize(struct_format)

    def __init__(self, dir_left=0, dir_right=0, servo=b'a', color=b'n', claw=10):
        self.dir_left = dir_left
        self.dir_right = dir_right
        self.servo = servo
        self.color = color
        self.claw = claw

    def to_bytes(self):
        """Pack the structure into bytes."""
        return struct.pack(
            self.struct_format,
            self.dir_left,
            self.dir_right,
            self.servo,
            self.color,
            self.claw
        )

    @classmethod
    def from_bytes(cls, data):
        """Unpack bytes into a PackageNRF instance."""
        unpacked = struct.unpack(cls.struct_format, data)
        return cls(
            dir_left=unpacked[0],
            dir_right=unpacked[1],
            servo=unpacked[2],
            color=unpacked[3],
            claw=unpacked[4]
        )

def set_servo_angle(pin, angle):
    """Set the angle of a servo motor."""
    pulse_width = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
    pi.set_servo_pulsewidth(pin, pulse_width)

def setup_radio():
    """Setup the nRF24 radio."""
    while not radio.begin(22, 0):
        radio.stopListening()
        radio.flush_rx()
        radio.flush_tx()
        print("Connecting...")
        time.sleep(0.1)

    radio.openReadingPipe(0, address)
    radio.setPALevel(RF24_PA_HIGH)
    radio.startListening()

def setup_serial():
    ser = serial.Serial(port, baud_rate)

def receive_message():
    """Receive and process messages from the nRF24."""
    if radio.available():
        # Read the incoming message
        received_data = radio.read(PackageNRF.size)
        if received_data:
            # Decode the received data into a PackageNRF instance
            package = PackageNRF.from_bytes(received_data)
            print(f"Received: {vars(package)}")
            return package
    return None

def neopixel_reset():
    pixels = neopixel.NeoPixel(board.D21, 1, brightness=1)
    pixels.fill((0, 0, 0))
    pixels.show()

def control_neopixel():
    """Control NeoPixel LED with predefined colors."""
    pixels = neopixel.NeoPixel(board.D21, 1, brightness=1)

    # Set color to red
    pixels.fill((255, 0, 0))
    pixels.show()
    sleep(2)

    # Set color to green
    pixels.fill((0, 255, 0))
    pixels.show()
    sleep(2)

    # Set color to blue
    pixels.fill((0, 0, 255))
    pixels.show()
    

def main():
    """Main loop to control servos and NeoPixel based on RF24 data."""
    setup_radio()
    setup_serial()
    try:
        while True:
            package = receive_message()
            if package:
                if package.servo == b'b':
                    for index in range(len(SERVO_PINS)):
                        set_servo_angle(SERVO_PINS[index], 90)

                elif package.servo == b'f':
                    for index in range(len(SERVO_PINS)):
                        set_servo_angle(SERVO_PINS[index], 120)
                

            control_neopixel()
            print("penis")

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Turn off all servos and NeoPixel
        for pin in SERVO_PINS:
            pi.set_servo_pulsewidth(pin, 0)
        neopixel_reset()
        pi.stop()

if __name__ == '__main__':
    main()
