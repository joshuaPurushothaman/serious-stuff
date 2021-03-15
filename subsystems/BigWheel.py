#!/usr/bin/env micropython

from ev3dev2.wheel import Wheel

class BigWheel(Wheel):
    def __init__(self):
        Wheel.__init__(self, 127, 19)