#!/usr/bin/env micropython

from util.alg.SyncPID import SyncPID
from types import LambdaType
import _thread
from time import sleep

infinity = float("inf")

class AsyncPID(SyncPID):
    def __init__(self, kP=1.0, kI=0.0, kD=0.0, minOutput = infinity, maxOutput=-infinity, iZone=0):
        super().__init__(kP, kI, kD, minOutput, maxOutput, iZone)
    
    def startWork(self, setpointGetter: LambdaType, processVariableGetter: LambdaType,
                outputReceiver: LambdaType, interrupter: LambdaType):
        """ Pass in lambdas that return the current setpoint, current PV and 
        receives the output as a parameter; interrupter should return true when to quit the pid loop """
        
        def periodic():
            while True:
                outputReceiver(self.calculate(setpointGetter(), processVariableGetter()))

        try:
            _thread.start_new_thread(periodic, ())
            print("INFO: PID thread started")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print (message)
            print("Error starting PID thread")

        while interrupter():
            sleep(0)
