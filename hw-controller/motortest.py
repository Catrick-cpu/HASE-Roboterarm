#! /usr/bin/python3

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import board
import busio
import time
import re
import os
import sys
import argparse

###MOTORS###                                                                                                                                                                                                                                                                                                                            Luca stinkt

i2c = busio.I2C(board.SCL, board.SDA)

kit1 = MotorKit(i2c=i2c, address=0x60)  # KIT 1 DEF

kit2 = MotorKit(i2c=i2c, address=0x70)  # KIT 2 DEF

motors = [kit1.stepper1, kit1.stepper2, kit2.stepper1, kit2.stepper2]

###PARSER###

parser = argparse.ArgumentParser()  # setting up arguments

parser.add_argument("--ss", "--stepstyle", help="Options: SINGLE, DOUBLE, MICRO")
parser.add_argument("--mid", "--motorid", help="Options: 1, 2, 3, 4")
parser.add_argument("--sc", "--stepcount", help="How Many Steps")
parser.add_argument("--sd", "--stepdelay")
parser.add_argument("--dir", "--direction", help="Options: forward, backward")

args = parser.parse_args()


##Setting It Up##                                                                                                                                                                                                                                                                                   Wer das liest ist dumm

stepcount = args.stepcount
stepstyle = str(args.stepstyle)
motorid = args.motorid
delay = args.stepdelay
direction = args.direction

for i in range(stepcount):

    style_map = {
        "SINGLE": stepper.SINGLE,
        "DOUBLE": stepper.DOUBLE,
        "MICRO": stepper.MICROSTEP,
    }
    style_str = (args.stepstyle or "single").lower()
    style_value = style_map.get(style_str, stepper.SINGLE)

    motor = motors[motorid - 1]
    dir_map = {"forward": stepper.FORWARD, "backward": stepper.BACKWARD}
    dir_value = dir_map.get(direction.lower())
    motor.onestep(direction=dir_value, style=style_value)
