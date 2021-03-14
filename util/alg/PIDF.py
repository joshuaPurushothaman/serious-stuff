#!/usr/bin/env micropython

from util.alg import PID

class PIDF(PID):
    def __init__(self, kP, kI, kD, kFF = 0.0):
        super().__init__(kP, kI, kD)
        self.kFF = kFF

    def calculate(self, setpoint: float, processVariable: float):
        return (super().calculate(setpoint, processVariable) 
                + self.kFF * processVariable)