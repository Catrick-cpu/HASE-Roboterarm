#! /usr/bin/python3


# ----import libarys----
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import re
import os
import sys
import argparse  # for getting arguments

# ---- Lockfile zur Verhinderung mehrfacher Ausführung ----
lockfile = "/tmp/my_script_running.lock"
if os.path.exists(lockfile):
    print("Script läuft bereits! Beende Ausführung…")
    sys.exit(0)
else:
    with open(lockfile, "w") as f:
        f.write(str(os.getpid()))  # PID speichern


parser = argparse.ArgumentParser()  # setting up arguments

parser.add_argument("mode")
# Server für server und manual für manuelle
args = parser.parse_args()


if args.mode in ("server", "manual"):
    mode = args.mode
else:
    print("Wrong Argument, quitting")
    sys.exit(0)


def Interactive_Startup() -> None:
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


if mode == "manual":
    Interactive_Startup()


i2c = busio.I2C(board.SCL, board.SDA)

count_motors = 2

if mode == "manual":
    # ----Configurate Adafruit Motor Hats----
    count_motors = 1
    print("Enter Adress 1")
    adress_kit_1 = int(input("Enter Number from I2C-Detect Output (Example: 0x60):"))
    kit1 = MotorKit(i2c=i2c, address=adress_kit_1)
    print("Do you want to add a second Adress?")
    input("y/n:")
    if input == "y":
        count_motors = 2
        print("Enter Adress 2")
        adress_kit_2 = int(
            input("Enter Number from I2C-Detect Output (Example: 0x60):")
        )
        kit2 = MotorKit(i2c=i2c, address=adress_kit_2)

elif mode == "server":
    kit1 = MotorKit(i2c=i2c, address=0x60)
    kit2 = MotorKit(i2c=i2c, address=0x70)
    motors = [kit1.stepper1, kit1.stepper2, kit2.stepper1, kit2.stepper2]
    time.sleep(1)

if mode == "manual":
    # ----Motor Defenitions----
    print("Motor Defenitons")

    if count_motors == 2:
        motors = [kit1.stepper1, kit1.stepper2, kit2.stepper1, kit2.stepper2]

    else:
        motors = [kit1.stepper1, kit1.stepper2]
    time.sleep(0.5)


# ----Motor Control----
def interactive_move_stepper(direction, speed, duration, motor_id) -> None:
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


def noninteractive_move_stepper(direction, speed, duration, motor_id) -> None:
    motor = motors[motor_id - 1]
    dir_map = {"forward": stepper.FORWARD, "backward": stepper.BACKWARD}
    dir_value = dir_map.get(direction.lower())
    if dir_value is None:
        print("Error")
        return

    speed_delay = 1 / speed
    loops = duration / speed_delay
    for _ in range(loops):
        motor.onestep(direction=dir_value, style=stepper.SINGLE)
        time.sleep(speed_delay)


def Interacive_console() -> None:
    while True:
        try:
            command = input().strip()

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
                    interactive_move_stepper(direction, speed, duration, motor_id)
                else:
                    print("Motornummer muss zwischen 1 und 4 liegen.")

            else:
                print("unknown command")
                print("Usage: steppermotor(forward, 120, 5, 1)")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Fehler: {e}")


def noninteractive_console() -> None:
    while True:
        try:
            command = input(">>> ").strip()
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
                    noninteractive_move_stepper(direction, speed, duration, motor_id)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Fehler: {e}")


if mode == "server":
    noninteractive_console()

elif mode == "manual":
    Interacive_console()

# Motoren ausschalten
for m in motors:
    m.release()

print("Application Ended")
