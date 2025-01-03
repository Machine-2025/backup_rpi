import pigpio
import time
from pyrf24 import RF24, RF24_PA_HIGH

# Initialisation des servos
pi = pigpio.pi()
SERVO_PINS = [12, 13, 18]
MIN_PULSE = 500
MAX_PULSE = 2500

# Initialisation du nRF24L01
radio = RF24(22, 0)  # CE=GPIO 22, CSN=GPIO 8 (SPI0)

# Adresse et canal
address = b"00002"
radio.begin(22, 0)
radio.stopListening()
radio.flush_rx()
radio.flush_tx()
radio.openReadingPipe(0, address)
radio.setPALevel(RF24_PA_HIGH)
radio.startListening()

def set_servo_angle(pin, angle):
    """Définit l'angle d'un servo en fonction de la broche et de l'angle."""
    pulse_width = MIN_PULSE + (angle / 180.0) * (MAX_PULSE - MIN_PULSE)
    pi.set_servo_pulsewidth(pin, pulse_width)

try:
    while True:
        if radio.available():
            # Lecture des données reçues
            data = radio.read(32).decode('utf-8').strip()
            print(f"Reçu : {data}")

            # Exemple de commande : "S1:90" (Servo 1 à 90°)
            if data.startswith("S"):
                servo_id, angle = map(int, data[1:].split(":"))
                if 1 <= servo_id <= 3:
                    set_servo_angle(SERVO_PINS[servo_id - 1], angle)
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Arrêt")

# Arrête tout
for pin in SERVO_PINS:
    pi.set_servo_pulsewidth(pin, 0)
pi.stop()
radio.stopListening()
