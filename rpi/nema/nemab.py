import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib


DIR = 26
STEP = 19
STEPPER_GPIO = (21,20,16)
stepper = RpiMotorLib.A4988Nema(DIR,STEP,STEPPER_GPIO,"A4988")
stepper.motor_go(True,"Full",100,1,False,0.05)


