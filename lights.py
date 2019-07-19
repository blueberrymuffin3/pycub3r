from ev3dev2.led import Leds
from time import sleep
import math
import threading

leds = Leds()

doLights = False
lights = None

def coolLightThing():
    i = 0
    while doLights:
        i += .1
        color1 = (max(0, math.sin(i+.5)), max(0, math.cos(i+.5)))
        color2 = (max(0, math.sin(i   )), max(0, math.cos(i   )))
        leds.set_color('LEFT', color1)
        leds.set_color('RIGHT', color2)
        sleep(.02)
    leds.set_color('LEFT', 'GREEN')
    leds.set_color('RIGHT', 'GREEN')

def startLights():
    global doLights
    if not doLights:
        doLights = True
        lights = threading.Thread(target=coolLightThing)
        lights.start()

def stopLights():
    global doLights
    if doLights:
        doLights = False
        lights.join()
