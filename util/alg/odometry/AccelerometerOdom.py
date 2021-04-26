#!/usr/bin/env micropython

import math
import _thread

from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import GyroSensor
from util.geometry.Pose2d import Pose2d
from subsystems import HTAccelerometer

class AccelerometerOdom:
    """
    assumes v0 = x0 = 0
    """
    pose = Pose2d()

    def __init__(self, accel: HTAccelerometer, gyro: GyroSensor):
        self.accel = accel
        self.gyro = gyro

        self.pose.x = 0
        self.pose.y = 0
        self.pose.theta = 0
    
    def update(self) -> Pose2d:
        xVel = 0
        yVel = 0

        def periodic():
            """
                call periodically plsZ!
            """
            # calculate how far each side has gone
            # self.pose.x, y, theta


            xVel += self.accel.xAccel
            yVel += self.accel.yAccel

            self.pose.x += xVel
            self.pose.y += yVel

            self.pose.theta = self.gyro.angle

            return self.pose
        
        # WIP, use _thread