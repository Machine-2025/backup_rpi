import time
import struct
from pyrf24 import RF24, RF24_PA_HIGH, RF24_PA_LOW

# Define the radio parameters
radio = RF24(22, 0)  # CE pin is 25, CSN pin is 0
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
        print(unpacked)
        return cls(
            dir_left=unpacked[0],
            dir_right=unpacked[1],
            servo=unpacked[2],
            color=unpacked[3],
            claw=unpacked[4]
        )


def setup():
    """Setup the nRF24 radio."""
    while not (radio.begin(22, 0)):
        radio.stopListening()
        radio.flush_rx()
        radio.flush_tx()
        print("Connecting...")
        time.sleep(0.1)

    #if(radio.begin(22, 0)):
    #    print("Radio is set up and listening...")
    #else:
    #    print("radio not setup")
    
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
            print(f"Received: {vars(package)}")  # Print the package as a dictionary


def main():
    """Main loop to continuously receive messages."""
    setup()
    while True:
        receive_message()
        time.sleep(0.1)  # Sleep for 100ms to reduce CPU usage


if __name__ == '__main__':
    main()
