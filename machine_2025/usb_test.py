import serial
import time

# Configuration du port série
port = "/dev/ttyUSB0"  # Remplacez par le port série de votre Arduino
baud_rate = 115200  # Baud rate pour la communication UART
delay_between_commands = 0.25  # Délai entre chaque commande (en secondes)

# Variables pour stocker les informations actuelles
current_color = "NULL"
passenger_counts = {"RED": 0, "GREEN": 0, "BLUE": 0, "YELLOW": 0, "PURPLE": 0}

# Liste des couleurs valides
valid_colors = ["RED", "GREEN", "BLUE", "YELLOW", "PURPLE"]

ser = serial.Serial(port, baud_rate)

response_info = ser.readline().decode('utf-8').strip()
print(response_info)

ser.write("INFO:B\n".encode('utf-8'))

response_info = ser.readline().decode('utf-8').strip()

print(response_info)