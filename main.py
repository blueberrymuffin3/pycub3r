#!/usr/bin/python3
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from enum import Enum
from time import sleep

import math

class ArmPositions(Enum):
    Up = 1
    Settle = 2
    Down = 3
    Flip = 4

armMotor = LargeMotor(OUTPUT_A)
armMotorSpeed = 22

tableMotor = LargeMotor(OUTPUT_B)
tableMotorSpeed = 35
tableMotorOvershoot = 40

scannerMotor = MediumMotor(OUTPUT_C)
scannerMotorSpeed = 50

def turnTable(turns):
    overshoot = math.copysign(tableMotorOvershoot, turns)
    degrees = 270 * turns
    tableMotor.on_for_degrees(tableMotorSpeed, degrees + overshoot)
    tableMotor.on_for_degrees(tableMotorSpeed, -overshoot)
    sleep(.25)

def moveArm(position):
    #print(".... Moving arm", end="\r")
    if position == ArmPositions.Up:
        on_to_position_timeout(armMotor, armMotorSpeed, 0)
    elif position == ArmPositions.Down:
        on_to_position_timeout(armMotor, armMotorSpeed, 100)
    elif position == ArmPositions.Settle:
        on_to_position_timeout(armMotor, armMotorSpeed, 85)
    elif position == ArmPositions.Flip:
        on_to_position_timeout(armMotor, armMotorSpeed, 180)
    #print("Done")
    #print()
    sleep(.2)

def on_to_position_timeout(motor, speed, position, brake=True, block=True, timeout=1000):
    speed = motor._speed_native_units(speed)
    motor.speed_sp = int(round(speed))
    motor.position_sp = position
    motor._set_brake(brake)
    motor.run_to_abs_pos()

    if block:
        motor.wait_until('running', timeout=100)
        motor.wait_until_not_moving(timeout=timeout)

def flipCube(times=1):
    for _ in range(times):
        moveArm(ArmPositions.Flip)
        moveArm(ArmPositions.Settle)
    moveArm(ArmPositions.Down)

def rotateCube(times):
    moveArm(ArmPositions.Up)
    turnTable(times)
        
def initMotors():
    print("Initializing Arm...")
    armMotor.stop_action = "brake"
    armMotor.on_for_seconds(-armMotorSpeed, 3)
    armMotor.position = -10
    armMotor.position_sp = 0
    moveArm(ArmPositions.Up)

    print("Initializing Table...")
    tableMotor.stop_action = "brake"
    turnTable(.5)
    turnTable(-.5)

    print("Initializing Scanner...")
    scannerMotor.stop_action = "brake"

    print("Done Initializing")
    print()

def shutdownMotors():
    print("Shutting Down Motors")
    armMotor.off(False)
    tableMotor.off(False)
    scannerMotor.off(False)

def pat_a():
    moveArm(ArmPositions.Down)
    turnTable(2)
    flipCube(2)

    moveArm(ArmPositions.Down)
    turnTable(-2)

def main():
    initMotors()
    
    pat_a()
    flipCube(1)
    pat_a()
    rotateCube(1)
    flipCube(1)
    pat_a()

    sleep(1)
    moveArm(ArmPositions.Up)
    tableMotor.on_for_rotations(50, 3)
    sleep(1)

    shutdownMotors()

if __name__ == "__main__":
    try:
        main()
    except:
        shutdownMotors()