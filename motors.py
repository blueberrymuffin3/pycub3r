from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from enum import Enum
from time import sleep
import threading
import math

class ArmPositions(Enum):
    Up = 1
    Settle = 2
    Down = 3
    Flip = 4

armMotor = LargeMotor(OUTPUT_A)
armMotorSpeed = 25

tableMotor = LargeMotor(OUTPUT_B)
tableMotorSpeed = 50
tableMotorOvershoot = 50
tableDegreesPerTurn = 270

scannerMotor = MediumMotor(OUTPUT_C)
scannerMotorSpeed = 50
scannerPositionHold = -200
scannerPositionCenter = -750
scannerPositionEdge = -625
scannerPositionCorner = -575


def turnTable(turns, doOvershoot=True):
    degrees = tableDegreesPerTurn * turns
    if(doOvershoot):
        overshoot = math.copysign(tableMotorOvershoot, turns)
        tableMotor.on_for_degrees(tableMotorSpeed, degrees + overshoot)
        tableMotor.on_for_degrees(tableMotorSpeed, -overshoot)
    else:
        tableMotor.on_for_degrees(tableMotorSpeed, degrees)

def moveArm(position):
    if position == ArmPositions.Up:
        on_to_position_timeout(armMotor, armMotorSpeed, 0)
    elif position == ArmPositions.Down:
        on_to_position_timeout(armMotor, armMotorSpeed, 100)
    elif position == ArmPositions.Settle:
        on_to_position_timeout(armMotor, armMotorSpeed, 75)
    elif position == ArmPositions.Flip:
        on_to_position_timeout(armMotor, armMotorSpeed, 190)

def moveScanner(position, brake=True, block=True):
    on_to_position_timeout(scannerMotor, scannerMotorSpeed, position, brake, block, 3000)

def on_to_position_timeout(motor, speed, position, brake=True, block=True, timeout=1000):
    # TODO why is the timeout necessary?
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

    print("Initializing Scanner...")
    scannerMotor.on_for_seconds(scannerMotorSpeed/5, 5)
    scannerMotor.speed_sp = scannerMotor._speed_native_units(scannerMotorSpeed)
    scannerMotor.position = -10
    moveScanner(0)

    print("Initializing Table...")
    tableMotor.stop_action = "brake"
    turnTable(.5)
    turnTable(-.5)

    print("Done Initializing")
    print()

def shutdownMotors():
    print("Shutting Down Motors")
    sleep(1)
    armMotor.off(False)
    tableMotor.off(False)
    scannerMotor.off(False)
