#!/usr/bin/env micropython

from ev3dev2.sensor import I2cSensor, Sensor
from util import ezmath

class HTAccelerometer(I2cSensor):
    """HiTechnic NXT Accelerometer. Acceleration is measured in the range of –2g to +2g.\n
    http://docs.ev3dev.org/projects/lego-linux-drivers/en/ev3dev-stretch/sensor_data.html#ht-nxt-accel"""
    
    # TODO: Return in units of m/s^2, currently returns in 200 units per g.

    SYSTEM_CLASS_NAME = Sensor.SYSTEM_CLASS_NAME
    SYSTEM_DEVICE_NAME_CONVENTION = Sensor.SYSTEM_DEVICE_NAME_CONVENTION

    MODE_ACCEL = 'ACCEL'
    MODE_ALL = 'ALL'
    MODES = (MODE_ACCEL, MODE_ALL)

    def __init__(self, address=None, name_pattern=SYSTEM_DEVICE_NAME_CONVENTION, name_exact=False, **kwargs):
        super(HTAccelerometer, self).__init__(address, name_pattern, name_exact, **kwargs)
        self._poll_ms = 0.1

    def getSingleAxis(self):
        """unsure, avoid using this"""
        self._ensure_mode(self.MODE_ACCEL)
        return self.value(0)

    def xAccel(self):
        self._ensure_mode(self.MODE_ALL)
        accel = (self.value(0) << 2) + (self.value(3) >> 6)
        return self.nativeAccelUnitsToSI(accel)
        
    def yAccel(self):
        self._ensure_mode(self.MODE_ALL)
        accel = (self.value(1) << 2) + (self.value(4) >> 6)
        return self.nativeAccelUnitsToSI(accel)
    
    def zAccel(self):
        self._ensure_mode(self.MODE_ALL)
        accel = (self.value(2) << 2) + (self.value(5) >> 6)
        return self.nativeAccelUnitsToSI(accel)
        
    def nativeAccelUnitsToSI(self, value: float):
        return ezmath.map(value, -400, 400, -2*9.81, 2*9.81)
