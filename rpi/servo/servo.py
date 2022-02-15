#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys
import numpy as np
import logging
from threading import Thread
from .pathcalc import *
position_dict = {}
position_dict["home"] = 8.0
position_dict["graveyard"] = 6.4 - 0.1
position_dict["filter"] = 9.6 + 0.1
#logging.basicConfig(filename="servo/servo.log",filemode="w",format='%(asctime)s -%(levelname)s -  %(message)s',datefmt='%d-%b-%y %H:%M:%S')
# logging.basicConfig(filename="servo/servo.log",level=logging.DEBUG)
class Servo(Exception):
	# brown = black GND
	# orange = red PWR
	# Yellow = white SIG
	sig_pin = 23
	p = 0 #what is p
	pos = position_dict["home"]
	is_moving = False
	round_val = 2
	action = ""
	def  __init__(self,tgt_sig_pin):
		self.sig_pin = tgt_sig_pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup( self.sig_pin, GPIO.OUT)
		self.p = GPIO.PWM(self.sig_pin,50)
		self.p.ChangeFrequency(50)
		self.p.start(position_dict["home"])
		self.p.ChangeDutyCycle(position_dict["home"])
		self.pos = position_dict["home"]
		self.is_moving = False
		# logging.info("started servo")
	def cleanup(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.sig_pin, GPIO.OUT)
		GPIO.output(self.sig_pin, GPIO.LOW)
		GPIO.cleanup()
	def get_pos(self):
		return self.pos
	def set_pos_delay(self,tgt_pos,tgt_delay,tgt_wiggle):
		self.start_servo()
		self.is_moving = True
		cur_diff = tgt_pos - self.pos
		# mov_list =  [round(curpos,self.round_val) for curpos in np.linspace(self.pos,tgt_pos,20)]
		mov_list = get_path(self.pos,tgt_pos,self.round_val)
		self.action = "moving to " + str(mov_list)
		for idx in mov_list:
			self.pos = idx
			self.p.ChangeDutyCycle(self.pos)
			time.sleep(tgt_delay)
		# at position wiggle back and forth
		if tgt_wiggle:
			mov_list = get_wiggle_path(self.pos,tgt_pos,self.round_val)
			self.action = "wiggle to " + str(mov_list)
			for mov_pos in mov_list:
				self.pos = mov_pos
				self.p.ChangeDutyCycle(self.pos)
				time.sleep(tgt_delay)
		self.pos = tgt_pos
		self.is_moving = False
		self.stop_servo()
	def move(self,tgt_pos,tgt_delay,tgt_wiggle):
		#same as set_pos_delay but adds threading
		x = Thread(target=self.set_pos_delay, args=(tgt_pos,tgt_delay,tgt_wiggle))
		x.start()
	def wiggle(self):
		# synchronous wiggle
		self.start_servo()
		mov_list = get_wiggle_path(1,self.pos,self.round_val)
		self.action = "wiggle sync " + str(mov_list)
		for idx in mov_list:
			# cur_diff = (idx-3)*0.1
			# tgt_pos = self.pos + cur_diff
			self.p.ChangeDutyCycle(self.pos)
			time.sleep(0.25)
		self.stop_servo()
	def stop_servo(self):
		self.p.stop()
	def start_servo(self):
		self.p.ChangeFrequency(50)
		self.p.start(0)
		self.p.ChangeDutyCycle(self.pos)
	def set_pos(self,tgt_pos):
		self.start_servo()
		self.is_moving = True
		self.pos = round(tgt_pos,self.round_val)
		self.p.ChangeDutyCycle(self.pos)
		time.sleep(0.5)
		self.is_moving = False
		self.stop_servo()
	def run(self,tgt_cycle):
		self.is_moving = True
		cur_dir = 1
		if self.cur_cycle > tgt_cycle:
			cur_dir = -1
		print(self.cur_cycle,tgt_cycle,cur_dir)
		self.p.ChangeDutyCycle(tgt_cycle)
		time.sleep(0.1)
		self.pos = tgt_cycle
		self.is_moving = False
	def check_moving(self):
		return self.is_moving
	def get_action(self):
		return self.action