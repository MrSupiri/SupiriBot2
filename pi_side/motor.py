import time
import RPi.GPIO as gpio


enable_L = 36
motorL_1 = 33
motorL_2 = 35
enable_R = 37
motorR_1 = 38
motorR_2 = 40
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(enable_L, gpio.OUT)
gpio.setup(motorL_1, gpio.OUT)
gpio.setup(motorL_2, gpio.OUT)
gpio.setup(enable_R, gpio.OUT)
gpio.setup(motorR_1, gpio.OUT)
gpio.setup(motorR_2, gpio.OUT)
gpio.output(enable_L, False)
gpio.output(motorL_1, True)
gpio.output(motorL_2, True)
gpio.output(enable_R, True)
gpio.output(motorR_1, True)
gpio.output(motorR_2, True)

led = 29
gpio.setup(led, gpio.OUT)
gpio.output(led, True)
led2 = 31
gpio.setup(led2, gpio.OUT)
gpio.output(led2, True)

def setGPIO(EL=1, ML1=0, ML2=0, ER=1, MR1=0, MR2=0):
    gpio.output(enable_L, EL)
    gpio.output(motorL_1, ML1)
    gpio.output(motorL_2, ML2)
    gpio.output(enable_R, ER)
    gpio.output(motorR_1, MR1)
    gpio.output(motorR_2, MR2)


def stop(tf=1):
    fwd(tf)


def fwd(tf=0.02):
    setGPIO(1, 1, 0, 1, 1, 0)
    time.sleep(tf)
    setGPIO()


def back(tf=0.03):
    setGPIO(1, 0, 1, 1, 0, 1)
    time.sleep(tf)
    setGPIO()


def right(tf=0.01):
    setGPIO(1, 1, 0, 1, 0, 0)
    time.sleep(tf)
    setGPIO()


def left(tf=0.01):
    setGPIO(1, 0, 0, 1, 1, 0)
    time.sleep(tf)
    setGPIO()


def fright(tf=0.03):
    setGPIO(1, 1, 0, 1, 0, 1)
    time.sleep(tf)
    setGPIO()


def fleft(tf=0.03):
    fwd(0.1)
    setGPIO(1, 0, 1, 1, 1, 0)
    time.sleep(tf)
    setGPIO()


def right90(tf=0.55):
    setGPIO(1, 1, 0, 1, 0, 1)
    time.sleep(tf)
    setGPIO()


def left90(tf=0.55):
    setGPIO(1, 0, 1, 1, 1, 0)
    time.sleep(tf)
    setGPIO()


def turn(tf=1.15):
    setGPIO(1, 0, 1, 1, 1, 0)
    time.sleep(tf)
    setGPIO()


def stay():
    setGPIO(0, 0, 0, 0, 0, 0)
