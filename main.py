#!/usr/bin/env micropython

import sys
from Robot import Robot

def main():
    robot = Robot()

    if len(sys.argv) > 0:
        robot.run(sys.argv[1])
    else:
        robot.run("auto")

if __name__ == "__main__":
    main()