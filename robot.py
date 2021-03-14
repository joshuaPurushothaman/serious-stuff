#!/usr/bin/env micropython

from time import sleep

from ev3dev2.sensor.lego import InfraredSensor, GyroSensor, ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

from subsystems.Drivetrain import Drivetrain as dt
from subsystems.Arm import Arm as arm

leftColor = ColorSensor(INPUT_1)
rightColor = ColorSensor(INPUT_4)
ir = InfraredSensor(INPUT_2)
gyro = GyroSensor(INPUT_3)

leds = Leds()
sound = Sound()

#---- Code here:

def init():
    return

def periodic():
    sound.play_song((
            ('D4', 'e3'),
            ('D4', 'e3'),
            ('D4', 'e3'),
            ('G4', 'h'),
            ('D5', 'h')
        ))
    return

#---- end