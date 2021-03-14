#!/usr/bin/env micropython

from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_D, SpeedPercent

class Arm:
    liftMotor = LargeMotor(OUTPUT_D)
    gripMotor = MediumMotor(OUTPUT_A)