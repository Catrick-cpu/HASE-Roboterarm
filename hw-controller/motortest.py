from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import re
import os
import sys
import argparse

os.system("sudo i2cdetect -y 1")

i2c = busio.I2C(board.SCL, board.SDA)
kit1 = MotorKit(i2c=i2c, address=0x60)
motors = [kit1.stepper1, kit1.stepper2]

direction = "forward"
P = int(input("range:"))
for i in range(P):
    
    dir_map = {direction: str("forward")"forward": stepper.FORWARD, "backward": stepper.BACKWARD}
    dir_value = dir_map.get(direction.lower())
    motor = motors[0]
    motor.onestep(direction=dir_value, style=stepper.SINGLE)
