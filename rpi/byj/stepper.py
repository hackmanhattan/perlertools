#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys

in1 = 17
in2 = 18
in3 = 27
in4 = 22

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.02

step_count = 4096*1 # 5.625*(1/64) per step, 4096 steps is 360°
step_count = 1000
direction = False # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]
class Stepper:
	pin_list = []
	speed = 0.01
	moving = False
	def  __init__(self,tgt_pin_list):
		self.pin_list = tgt_pin_list
		GPIO.setmode(GPIO.BCM)
		for idx in range(len(self.pin_list)):
			GPIO.setup( self.pin_list[idx], GPIO.OUT )
			GPIO.output( self.pin_list[idx], GPIO.LOW )
	def setSpeed(self,tgt_speed):
		self.speed = tgt_speed
	def cleanup(self):
		GPIO.setmode(GPIO.BCM)
		for idx in range(len(self.pin_list)):
			GPIO.output(self.pin_list[idx],GPIO.LOW)
		GPIO.cleanup()

	def run_motor(self,tgt_dir,tgt_step_count):
		motor_step_cnt = 0
		moving = True
		for idx in range(tgt_step_count):
			for pin in range(0,len(self.pin_list)):
				GPIO.output(self.pin_list[pin],step_sequence[motor_step_cnt][pin])
			if tgt_dir:
				motor_step_cnt = (motor_step_cnt -1) % 8
			elif tgt_dir==False:
				motor_step_cnt = (motor_step_cnt + 1) % 8
			else:
				cleanup()
				exit(1)
			time.sleep(self.speed)
		moving = False
	def is_moving(self):
		return self.moving