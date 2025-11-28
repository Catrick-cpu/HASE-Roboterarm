#!!!!!!!!!!!!!!!!!!!!!!!!!
# THIS SCRIPT IS OUTDATED
#!!!!!!!!!!!!!!!!!!!!!!!!!
#
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


direction = "forward"
speed_delay = 0.01
loops = 100
motor = motors[0]
dir_map = {"forward": stepper.FORWARD, "backward": stepper.BACKWARD}
dir_value = dir_map.get(direction.lower())

for _ in range(loops):
    motor.onestep(direction=dir_value, style=stepper.SINGLE)
    time.sleep(speed_delay)
