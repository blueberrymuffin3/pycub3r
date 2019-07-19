#!/usr/bin/python3
import motors as M
import lights as L

from time import sleep

def pat_a():
    M.moveArm(M.ArmPositions.Down)
    M.turnTable(2)
    M.flipCube(2)

    M.moveArm(M.ArmPositions.Down)
    M.turnTable(-2)

def main():
    M.initMotors()
    
    pat_a()
    M.flipCube(1)
    pat_a()
    M.rotateCube(1)
    M.flipCube(1)
    pat_a()

    sleep(1)
    M.moveArm(M.ArmPositions.Up)
    M.tableMotor.on_for_rotations(50, 3)
    sleep(1)


if __name__ == "__main__":
    try:
        main()
        main()
        L.startLights()
    finally:
        M.shutdownMotors()
        L.stopLights()
