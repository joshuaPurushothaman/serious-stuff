#!/usr/bin/env micropython

from time import sleep
import _thread

from util.ezmath import clamp
from util.alg.AsyncPID import AsyncPID
from util.alg.SyncPID import SyncPID
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
    accel = Accelerometer()

    lMotor = LargeMotor(OUTPUT_B)
    rMotor = LargeMotor(OUTPUT_C)

    diff = MoveDifferential(OUTPUT_B, OUTPUT_C, BigWheel, 127)
    steering_drive = MoveSteering(OUTPUT_B, OUTPUT_C)

    def __init__(self):
        self.diff.odometry_start()
        self.beginPrintOdometry()
    
    def drive(self):
        # Use odometry to drive to specific coordinates
        self.diff.on_to_coordinates(SpeedRPM(40), 300, 300)
    
    def rc(self):
        while True:
            self.remoteDrive(self.ir, 0.5)
            sleep(0.01)


    # TODO: tune
    heading_pid = SyncPID(1.5, 0, 0.15, -100, 100)
    dist_pid = SyncPID(1.5, 0, 0.15, -100, 100)

    def remoteDrive(self, ir: InfraredSensor, power = 1):
        if ir.beacon():   #   follow remote if beacon is pressed
            fd = self.dist_pid.calculate(0, ir.distance() if ir.distance() != None else 0)
            turn = self.heading_pid.calculate(0, ir.heading())
            
            self.arcadeDrive(fd, turn)
        else:   #   tank drive if not
            leftPower = (power if ir.top_left() else 0
                        -power if ir.bottom_left() else 0)
            
            rightPower = (power if ir.top_right() else 0
                        -power if ir.bottom_right() else 0)

            self.tankDrive(leftPower, rightPower)
            # yes, a remote control class exists

    
    def line_follow(self):
        line_follow_pid = AsyncPID(1.5, 0, 0.15, -100, 100)

        # def pidInterrupter():
            # return not (self.leftColor.reflected_light_intensity + self.rightColor.reflected_light_intensity) > 190
        
        line_follow_pid.startWork(lambda: self.leftColor.reflected_light_intensity,
                lambda: self.rightColor.reflected_light_intensity,
                # lambda output: self.steering_drive.on(output, -20),
                lambda output: self.arcadeDrive(-20, output),
                lambda: True)

        # pid = SyncPID(1.5, 0, 0.15, -100, 100)

        # while True:
        #     output = pid.calculate(self.leftColor.reflected_light_intensity,
        #         self.rightColor.reflected_light_intensity)

        #     self.steering_drive.on(output, -20)

    def arcadeDrive(self, fd: float, turn: float):
        leftPower = clamp(fd+turn, -100, 100)
        rightPower = clamp(fd-turn, -100, 100)

        self.tankDrive(leftPower, rightPower)
    
    def tankDrive(self, leftPower: float, rightPower: float):
        self.lMotor.on(leftPower)
        self.rMotor.on(rightPower)

    def beginPrintOdometry(self):
        def loop():
            print("--ODOMETRY--")
            while True:
                print("x: %4d y: %4d rot: %2.2d" % 
                (self.diff.x_pos_mm, self.diff.y_pos_mm, self.diff.theta))
        
        _thread.start_new_thread(loop)