import time
import RPi.GPIO as gpio

enable_L = 37
motorL_1 = 33
motorL_2 = 35
enable_R = 36
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
gpio.output(motorL_1, False)
gpio.output(motorL_2, False)
gpio.output(enable_R, False)
gpio.output(motorR_1, False)
gpio.output(motorR_2, False)


def setGPIO(EL=True, ML1=False, ML2=False, ER=True, MR1=False, MR2=False):
    gpio.output(enable_L, EL)
    gpio.output(motorL_1, ML1)
    gpio.output(motorL_2, ML2)
    gpio.output(enable_R, ER)
    gpio.output(motorR_1, MR1)
    gpio.output(motorR_2, MR2)


def fwd(tf=0.09):
    setGPIO(1, 1, 0, 1, 1, 0)
    time.sleep(tf)
    setGPIO()


def back(tf=0.09):
    setGPIO(1, 0, 1, 1, 0, 1)
    time.sleep(tf)
    setGPIO()


def right(tf=0.03):
    setGPIO(1, 1, 0, 1, 0, 0)
    time.sleep(tf)
    setGPIO()


def left(tf=0.03):
    setGPIO(1, 0, 0, 1, 1, 0)
    time.sleep(tf)
    setGPIO()

def right2(tf=0.03):
    setGPIO(1, 1, 0, 1, 0, 1)
    time.sleep(tf)
    setGPIO()


def left2(tf=0.03):
    setGPIO(1, 0, 1, 1, 1, 0)
    time.sleep(tf)
    setGPIO()

def right90(tf=0.5):
    setGPIO(1, 1, 0, 1, 0, 0)
    time.sleep(tf)
    setGPIO()

def left90(tf=0.5):
    setGPIO(1, 0, 0, 1, 1, 0)
    time.sleep(tf)
    setGPIO()

def turn(tf=1.2):
    setGPIO(1, 0, 1, 1, 1, 0)
    time.sleep(tf)
    setGPIO()

def stop(tf=1):
    fwd(tf)

def stay(tf=0.05):
    setGPIO(0, 0, 0, 0, 0, 0)
