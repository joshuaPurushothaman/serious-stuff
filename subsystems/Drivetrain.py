#!/usr/bin/env micropython

from time import sleep
from util.ezmath import clamp
from util.alg.AsyncPID import AsyncPID
from util.alg.SyncPID import SyncPID
# from util.alg.PID import PID
from ev3dev2.sensor.lego import InfraredSensor, GyroSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.motor import LargeMotor, MoveDifferential, MoveSteering, OUTPUT_B, OUTPUT_C, SpeedPercent, SpeedRPM

from subsystems.BigWheel import BigWheel

from util.alg.odometry.DiffDriveOdom import DiffDriveOdom

class Drivetrain:
    leftColor = ColorSensor(INPUT_1)
    rightColor = ColorSensor(INPUT_4)
    ir = InfraredSensor(INPUT_2)
    gyro = GyroSensor(INPUT_3)

    lMotor = LargeMotor(OUTPUT_B)
    rMotor = LargeMotor(OUTPUT_C)

    diff = MoveDifferential(OUTPUT_B, OUTPUT_C, BigWheel, 127)
    steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)

    def __init__(self):
        self.diff.odometry_start()
    
    def drive(self):
        # Use odometry to drive to specific coordinates
        self.diff.on_to_coordinates(SpeedRPM(40), 300, 300)
    
    def rc(self):
        return
    
    def line_follow(self):
        pid = AsyncPID(1.5, 0, 0.15, -100, 100)

        def pidInterrupter():
            return True
            # return not (self.leftColor.reflected_light_intensity + self.rightColor.reflected_light_intensity) > 190
        
        pid.startWork(lambda: self.leftColor.reflected_light_intensity,
                lambda: self.rightColor.reflected_light_intensity,
                # lambda output: self.steering_drive.on(output, -20),
                lambda output: self.arcadeDrive(-20, output),
                lambda: pidInterrupter())

        # pid = SyncPID(1.5, 0, 0.15, -100, 100)

        # while True:
        #     output = pid.calculate(self.leftColor.reflected_light_intensity,
        #         self.rightColor.reflected_light_intensity)

        #     self.steering_drive.on(output, -20)

    def arcadeDrive(self, fd, turn):
        leftPower = clamp(fd+turn, -100, 100)
        rightPower = clamp(fd-turn, -100, 100)

        self.tankDrive(leftPower, rightPower)
    
    def tankDrive(self, leftPower, rightPower):
        self.lMotor.on(leftPower)
        self.rMotor.on(rightPower)

