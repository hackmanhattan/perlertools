#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import numpy as np
import logging
from threading import Thread
from .pathcalc import *
import pigpio

position_dict = {}
position_dict["graveyard"] = 1350
position_dict["home"] = 1695
position_dict["filter"] = 2030
#logging.basicConfig(filename="servo/servo.log",filemode="w",format='%(asctime)s -%(levelname)s -  %(message)s',datefmt='%d-%b-%y %H:%M:%S')
# logging.basicConfig(filename="servo/servo.log",level=logging.DEBUG)
class Servo():
	# brown = black GND
	# orange = red PWR
	# Yellow = white SIG
	sig_pin = 23
	round_val = 2
	
	def  __init__(self,tgt_sig_pin):
		self.action = ""
		self.sig_pin = tgt_sig_pin
		self.pwm = pigpio.pi() 
		self.pwm.set_mode(self.sig_pin, pigpio.OUTPUT)
		self.pwm.set_PWM_frequency( self.sig_pin, 50 )
		self.pwm.set_servo_pulsewidth( self.sig_pin, position_dict["home"] ) ;
		self.pos = position_dict["home"]
		self.is_moving = 0
		# logging.info("started servo")
	def cleanup(self):
		print("cleanup")
	def get_pos(self):
		return self.pos
	def set_pos_delay(self,tgt_pos,tgt_delay,tgt_wiggle):
		self.is_moving = 1
		init_pos = self.pos
		cur_diff = tgt_pos - self.pos
		# mov_list =  [round(curpos,self.round_val) for curpos in np.linspace(self.pos,tgt_pos,20)]
		mov_list = get_path(self.pos,tgt_pos,self.round_val)
		print(self.pos,tgt_pos)
		if self.pos != tgt_pos:
			self.action = "moving from " + str(mov_list[0]) + " to " + str(mov_list[-1])
			for idx in mov_list:
				self.pos = idx
				self.pwm.set_servo_pulsewidth( self.sig_pin, self.pos )
				time.sleep(tgt_delay)
			self.pos = tgt_pos
			if tgt_wiggle:
				self.wiggle(init_pos,tgt_pos)
		self.is_moving = 0
	def move(self,tgt_pos,tgt_delay,tgt_wiggle):
		#same as set_pos_delay but adds threading
		x = Thread(target=self.set_pos_delay, args=(tgt_pos,tgt_delay,tgt_wiggle))
		x.start()
	def check_moving(self):
		return self.is_moving
	def get_action(self):
		return self.action
	def set_pos(self,tgt_pos):
		self.pos = round(tgt_pos,self.round_val)
		self.pwm.set_servo_pulsewidth( self.sig_pin, tgt_pos)

	def wiggle(self,cur_pos,tgt_pos):
		# synchronous wiggle
		mov_list = get_wiggle_path(cur_pos,tgt_pos,self.round_val)
		self.action = "wiggle sync from " + str(min(mov_list)) + " to " + str(max(mov_list))
		for idx in mov_list:
			self.pos = idx
			self.pwm.set_servo_pulsewidth( self.sig_pin, idx)
			
		# self.stop_servo()
	# def stop_servo(self):
	# 	self.p.stop()
	# def start_servo(self):
	# 	self.p.ChangeFrequency(50)
	# 	self.p.start(0)
	# 	self.p.ChangeDutyCycle(self.pos)