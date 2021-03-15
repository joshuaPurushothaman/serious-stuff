#!/usr/bin/env micropython

from time import sleep

from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from subsystems.Drivetrain import Drivetrain
# from subsystems.Arm import Arm

class Robot:
    leds = Leds()
    sound = Sound()

    dt = Drivetrain()

    def run(self, mode: str):
        if mode == 'rc':
            self.rc()
        elif mode == 'test':
            self.test()
        else:
            self.auto()
    
    def auto(self):
        """ Default main program """
        # self.dt.drive()
        self.dt.line_follow()

    def test(self):
        """ Used for testing code out before using the final version. """
        return

    def rc(self):
        """ Intended for remote control with the IR sensor. """
        return