# ----import libarys----
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import re
import os

# ----Initialise I2C----
i2c = busio.I2C(board.SCL, board.SDA)

kit1 = MotorKit(i2c=i2c, address=0x60)
kit2 = MotorKit(i2c=i2c, address=0x70)

motors = [kit1.stepper1, kit1.stepper2, kit2.stepper1, kit2.stepper2]


def move_stepper(direction, speed, duration, motor_id):
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
                move_stepper(direction, speed, duration, motor_id)

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Fehler: {e}")

# Motoren ausschalten
for m in motors:
    m.release()
