# ----import libarys----

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import re
import os

# ----READ THIS----


# ----Starting Up + I2C Detect----
print("DISCLAIMER:")
print("1. Dont unplug while running, always Poweroff.")
time.sleep(1)
print("2. Script for private and Educational Purposes only.")
time.sleep(1)
print("3. Ask Creator of Repository for more info.")
time.sleep(3)
print("Starting Up")
print("------------")
time.sleep(0.5)
print("===---------")
time.sleep(0.5)
print("======------")
time.sleep(0.5)
print("=========---")
time.sleep(0.5)
print("============")
print("Starting Up Complete")
time.sleep(1)
print("The Script now does an I2C-Detect")
print("The following Output should show something like 60----------70")
time.sleep(0.5)
os.system("sudo i2cdetect -y 1")


# ----Initialise I2C----
i2c = busio.I2C(board.SCL, board.SDA)

# ----Configurate Adafruit Motor Hats----
print("Enter Adress 1")
adress_kit_1 = int(input("Enter Number from I2C-Detect Output (Example: 0x60):"))
kit1 = MotorKit(i2c=i2c, address=adress_kit_1)
print("Do you want to add a second Adress?")
input("y/n:")
if input == "y":
    print("Enter Adress 2")
    adress_kit_2 = int(input("Enter Number from I2C-Detect Output (Example: 0x60):"))
    kit2 = MotorKit(i2c=i2c, address=adress_kit_2)

time.sleep(1)

# ----Motor Defenitions----
print("Motor Defenitons")
motors = [kit1.stepper1, kit1.stepper2]
time.sleep(0.5)


# ----Motor Control----
def move_stepper(direction, speed, duration, motor_id):
    print(
        "Usage: steppermotor(direction, speed, duration, motor id), Exampel: steppermotor(forward, 10, 60, 1)"
    )
    print("Motor Console:")
    print("exit to leave")

    motor = motors[motor_id - 1]
    dir_map = {"forward": stepper.FORWARD, "backward": stepper.BACKWARD}
    dir_value = dir_map.get(direction.lower())
    if dir_value is None:
        print("Ungültige Richtung! Nutze 'forward' oder 'backward'.")
        return
    print(f"Motor {motor_id}: {direction} ({speed} Speed, duration={duration})")
    speed_delay = 1 / speed
    loops = duration / speed_delay
    for _ in range(loops):
        motor.onestep(direction=dir_value, style=stepper.SINGLE)
        time.sleep(speed_delay)


while True:
    try:
        command = input(">>> ").strip()

        if command.lower() in ("exit", "quit"):
            print("Beende Programm…")
            break

        # Beispiel:
        # steppermotor(forward, 120, 5, 1)
        match = re.match(
            r"steppermotor\(\s*([a-zA-Z]+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
            command,
        )

        if match:
            direction = match.group(1)  # forward / backward
            speed = int(match.group(2))  # steps per second
            duration = int(match.group(3))  # seconds / loops etc.
            motor_id = int(match.group(4))  # 1-4

            if 1 <= motor_id <= 4:
                move_stepper(direction, speed, duration, motor_id)
            else:
                print("Motornummer muss zwischen 1 und 4 liegen.")

        else:
            print("unknown command")
            print("Usage: steppermotor(forward, 120, 5, 1)")

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Fehler: {e}")

# Motoren ausschalten
for m in motors:
    m.release()

print("Application Ended")
