#!/usr/bin/env micropython

from ev3dev2.motor import LargeMotor
from util.geometry import Pose2d
import math

class DiffDriveOdometry:
    pose: Pose2d

    def __init__(self, lMotor: LargeMotor, rMotor: LargeMotor, TRACK_WIDTH: float, WHEEL_DIAMETER: float):
        """
        units in meters please!
        """
        self.lMotor = lMotor
        self.rMotor = rMotor
        self.TRACK_WIDTH = TRACK_WIDTH
        self.WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi
    
    def update(self) -> Pose2d:
        """
            call periodically plsZ!
            thanks http://seattlerobotics.org/encoder/200610/Article3/IMU%20Odometry,%20by%20David%20Anderson.htm
        """
        # calculate how far each side has gone
        lRotMeters = (self.leftMotor.position / LargeMotor.count_per_rot) * self.WHEEL_CIRCUMFERENCE
        rRotMeters = (self.rightMotor.position / LargeMotor.count_per_rot) * self.WHEEL_CIRCUMFERENCE

        self.pose.x = math.sin((lRotMeters + rRotMeters) / 2.0)
        self.pose.y = math.cos((lRotMeters + rRotMeters) / 2.0)
        self.pose.theta = (lRotMeters - rRotMeters) / self.TRACK_WIDTH; # in radians!!
    
        return self.pose