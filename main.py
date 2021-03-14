#!/usr/bin/env micropython

import robot
from time import sleep

def main():
    robot.init()
    while True:
        robot.periodic()
        sleep(0.01) # Makes periodic loops 100hz.

if __name__ == "__main__":
    main()