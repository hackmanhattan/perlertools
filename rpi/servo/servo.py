#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys
import numpy as np
position_dict = {}
position_dict["home"] = 4.5
position_dict["result"] = 2.4 
position_dict["rest"] = 6.6
class Servo:
	# brown = black GND
	# orange = red PWR
	# Yellow = white SIG
	sig_pin = 23
	p = 0 #what is p
	pos = 0
	def  __init__(self,tgt_sig_pin):
		self.sig_pin = tgt_sig_pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup( self.sig_pin, GPIO.OUT)
		self.p = GPIO.PWM(self.sig_pin,50)
		self.p.ChangeFrequency(50)
		self.p.start(0)
		self.p.ChangeDutyCycle(0)
		self.pos = 0
	def cleanup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.sig_pin, GPIO.OUT)
		GPIO.output(self.sig_pin, GPIO.LOW)
		GPIO.cleanup()
	def get_pos(self):
		return self.pos
	def set_pos(self,tgt_pos):
		self.pos = tgt_pos
		self.p.ChangeDutyCycle(tgt_pos)
	def set_pos_delay(self,tgt_pos,tgt_delay):
		if self.pos > tgt_pos:
			cur_dir = -0.1
		for idx in np.linspace(self.pos,tgt_pos,10):
			self.p.ChangeDutyCycle(idx)
			time.sleep(tgt_delay)
		self.pos = tgt_pos
	def run(self,tgt_cycle):
		cur_dir = 1
		if self.cur_cycle > tgt_cycle:
			cur_dir = -1
		print(self.cur_cycle,tgt_cycle,cur_dir)
		self.p.ChangeDutyCycle(tgt_cycle)
		time.sleep(0.1)
		self.pos = tgt_cycle
