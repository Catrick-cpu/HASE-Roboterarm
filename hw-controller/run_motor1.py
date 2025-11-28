from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import os
import sys


def main() -> None:
    # I2C initialisieren
    i2c = busio.I2C(board.SCL, board.SDA)

    # Adafruit Motor HAT Standardadresse 0x60
    kit = MotorKit(i2c=i2c, address=0x60)
    motor = kit.stepper1

    try:
        print("Starte: Motor 1 wird 1000 Schritte vorwärts bewegt (delay=0.01s)")
        for i in range(1000):
            motor.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
            time.sleep(0.01)
        print("Fertig.")
    except KeyboardInterrupt:
        print("Abgebrochen durch Benutzer.")
    except Exception as e:
        print(f"Fehler beim Bewegen des Motors: {e}")


while True:
    main()
