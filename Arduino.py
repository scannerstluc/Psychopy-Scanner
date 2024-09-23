import time

import serial

def send_character(port, baud_rate):
    char="t"
    try:
        # Ouvrir le port série
        with serial.Serial(port=port, baudrate=baud_rate, timeout=1) as ser:
            print(f"Connexion ouverte sur {port}. Envoi de '{char}'...")
            ser.write(b'H')
            time.sleep(0.5)
            ser.write(b'L')
            print("Pin 2 activé puis désactivé")  # Message de confirmation


    except serial.SerialException as e:
        print(f"Erreur d'ouverture ou d'utilisation du port série : {e}")


if __name__ == "__main__":
    print("changement pour voir avec giddthub desktop")
    send_character('COM7', 115200)
