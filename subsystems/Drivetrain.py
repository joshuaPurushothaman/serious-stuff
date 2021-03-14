#!/usr/bin/env micropython

from util.alg.odometry import DiffDriveOdom
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent


class Drivetrain:
    TRACK_WIDTH = 0.127 # meters
    WHEEL_DIAMETER = 0.101 # meters

    leftMotor = LargeMotor(OUTPUT_B)
    rightMotor = LargeMotor(OUTPUT_C)

    odom = DiffDriveOdom(leftMotor, rightMotor, TRACK_WIDTH, WHEEL_DIAMETER)

    def updateOdom(self):
        self.odom.update()

