import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
enable_A = 37
motorA_1 = 33
motorA_2 = 35

enable_B = 36
motorB_1 = 38
motorB_2 = 40

gpio.setup(enable_A, gpio.OUT)
gpio.setup(motorA_1, gpio.OUT)
gpio.setup(motorA_2, gpio.OUT)

gpio.setup(enable_B, gpio.OUT)
gpio.setup(motorB_1, gpio.OUT)
gpio.setup(motorB_2, gpio.OUT)

gpio.output(enable_A,False)
gpio.output(motorA_1,False)
gpio.output(motorA_2,False)

gpio.output(enable_B,True)
gpio.output(motorB_1,True)
gpio.output(motorB_2,False)



gpio.cleanup()
