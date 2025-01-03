import pigpio
import time
import struct
from pyrf24 import RF24, RF24_PA_HIGH
from usb import automatisation

release_done = False

# Servo Initialization
pi = pigpio.pi()
SERVO_PINS = [12, 13, 18]
MIN_PULSE = 500
MAX_PULSE = 2500

ANGLE1 = 90
ANGLE2 = 120

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

def selectServoIndex(package : PackageNRF):
    index = 0
    if package.color == "N":
        index = 0
    elif package.color == "P":
        index = 1
    elif package.color == "G":
        index = 2
    return index

def main():
    """Main loop to control servos based on RF24 data."""
    setup_radio()

    try:
        while True:
        # if release_done:
            automatisation()
        # else:
            package = receive_message()
            if package:
                print(package)
                index = selectServoIndex(package)
                if (package.servo == b'b'):
                    set_servo_angle(SERVO_PINS[index], ANGLE1)
                if (package.servo == b'f'):
                    set_servo_angle(SERVO_PINS[index], ANGLE2)
                if index == 2:
                    release_done = True

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        # Turn off all servos and cleanup
        for pin in SERVO_PINS:
            pi.set_servo_pulsewidth(pin, 0)
        pi.stop()

if __name__ == '__main__':
    main()
