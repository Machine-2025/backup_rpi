import serial
import time
import board
import neopixel
import signal


def automatisation():
    pixels = neopixel.NeoPixel(board.D21, 1, brightness=1)

    # Configuration du port série
    port = "/dev/ttyUSB0"  # Remplacez par le port série de votre Arduino
    baud_rate = 115200  # Baud rate pour la communication UART
    delay_between_commands = 0.25  # Délai entre chaque commande (en secondes)

    # Variables pour stocker les informations actuelles
    current_color = "NULL"
    passenger_counts = {"RED": 0, "GREEN": 0, "BLUE": 0, "YELLOW": 0, "PURPLE": 0}

    # Liste des couleurs valides
    valid_colors = ["RED", "GREEN", "BLUE", "YELLOW", "PURPLE"]
    try:
        # Initialiser la connexion série
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            print(f"Connexion au port {port} établie.")
            while True:
                # Lecture de la réponse depuis l'Arduino
                response = ser.readline().decode('utf-8').strip()
                
                if response:
                    print(f"Réponse reçue : {response}")
                    
                    # Si STAT:connected est détecté
                    if response == "STAT:connected":
                        print("Statut : connecté détecté.")
                        
                        # Envoyer INFO:C pour obtenir la couleur de la station
                        ser.write("INFO:C\n".encode('utf-8'))
                        response_info = ser.readline().decode('utf-8').strip()
                        # Mettre la led en fonction
                    
                        
                        if response_info.startswith("OK:"):
                            current_color = response_info.split(":")[1]
                            print(f"Couleur de la station connectée : {current_color}")
                            if(current_color == valid_colors[0]):
                                pixels.fill((0, 255, 0))
                                pixels.show()
                            elif(current_color == valid_colors[1]):
                                pixels.fill((255, 0, 0))
                                pixels.show()
                            elif(current_color == valid_colors[2]):
                                pixels.fill((0, 0, 255))
                                pixels.show()
                            elif(current_color == valid_colors[3]):
                                pixels.fill((255, 255, 0))
                                pixels.show()
                            elif(current_color == valid_colors[4]):
                                pixels.fill((0, 255, 255))
                                pixels.show()
                            else:
                                pixels.fill((0,0,0))
                                pixels.show()

                            # Envoyer SEND pour la couleur actuelle avec le nombre stocké
                            if current_color in passenger_counts:
                                send_command = f"SEND:{current_color}:{passenger_counts[current_color]}\n"
                                ser.write(send_command.encode('utf-8'))
                                print(f"Commande envoyée : {send_command.strip()}")
                                time.sleep(delay_between_commands)  # Délai après SEND
                            else:
                                print(f"Couleur {current_color} non valide ou non trouvée dans les passagers.")
                            
                            # Envoyer TAKE pour toutes les autres couleurs
                            for color in valid_colors:
                                if color != current_color:
                                    take_command = f"TAKE:{color}:1\n"
                                    ser.write(take_command.encode('utf-8'))
                                    print(f"Commande envoyée : {take_command.strip()}")
                                    time.sleep(delay_between_commands)  # Délai entre les commandes
                        else:
                            print(f"Réponse inattendue pour INFO:C : {response_info}")
                    
                    # Si STAT:disconnected est reçu
                    elif response == "STAT:disconnected":
                        print("Statut : déconnecté détecté. Envoi de INFO:B.")
                        pixels.fill((0,0,0,))
                        pixels.show()
                        # Envoyer INFO:B pour obtenir les quantités de chaque couleur
                        ser.write("INFO:B\n".encode('utf-8'))
                        response_info = ser.readline().decode('utf-8').strip()
                        
                        if response_info.startswith("OK:"):
                            counts = response_info.split(":")[1:]
                            passenger_counts = dict(zip(valid_colors, map(int, counts)))
                            print(f"Quantités mises à jour : {passenger_counts}")
                        else:
                            print(f"Réponse inattendue pour INFO:B : {response_info}")
                    
                    # Gérer d'autres réponses si nécessaire
                    else:
                        print(f"Réponse non gérée : {response}")
                
                # Pause avant de vérifier à nouveau
                time.sleep(delay_between_commands)

    except serial.SerialException as e:
        print(f"Erreur de connexion série : {e}")

    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur.")