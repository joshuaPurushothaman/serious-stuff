#!/usr/bin/env micropython

import math
import _thread

from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import GyroSensor
from util.geometry.Pose2d import Pose2d

class DiffDriveOdom:
    """
        Deprecated, use MoveDifferential instead
    """
    pose = Pose2d()

    def __init__(self, lMotor: LargeMotor, rMotor: LargeMotor, gyro: GyroSensor, TRACK_WIDTH: float, WHEEL_DIAMETER: float):
        """
        units in meters please!
        """
        self.lMotor = lMotor
        self.rMotor = rMotor
        self.gyro = gyro
        self.TRACK_WIDTH = TRACK_WIDTH
        self.WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi
    
    def update(self) -> Pose2d:
        def periodic():
            """
                call periodically plsZ!
                thanks http://seattlerobotics.org/encoder/200610/Article3/IMU%20Odometry,%20by%20David%20Anderson.htm
            """
            # calculate how far each side has gone
            lRotMeters = (self.leftMotor.position / LargeMotor.count_per_rot) * self.WHEEL_CIRCUMFERENCE
            rRotMeters = (self.rightMotor.position / LargeMotor.count_per_rot) * self.WHEEL_CIRCUMFERENCE

            self.pose.x = math.sin((lRotMeters + rRotMeters) / 2.0)
            self.pose.y = math.cos((lRotMeters + rRotMeters) / 2.0)
            
            if self.gyro == None:
                self.pose.theta = (lRotMeters - rRotMeters) / self.TRACK_WIDTH; # in radians!!
            else:
                self.pose.theta = math.degrees(self.gyro.angle)
        
            return self.pose
        
        # WIP, use _thread