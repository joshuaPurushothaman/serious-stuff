#!/usr/bin/env micropython

class PID:
    iErr = 0
    def __init__(self, kP=1.0, kI=0.0, kD=0.0):
        self.kP = kP
        self.kI = kI
        self.kD = kD
    
    def calculate(self, setpoint: float, processVariable: float):
        error = setpoint - processVariable

        # integrate error
        self.iErr += error

        # calculate dErr
        lastError = 0
        dErr = error - lastError
        lastError = error

        # output
        return (self.kP * error
                + self.kI * self.iErr
                + self.kD * dErr)