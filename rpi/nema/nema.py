from time import sleep
import RPi.GPIO as GPIO


class Nema:
	dir_pin = 20   # Direction GPIO Pin
	step_pin_ = 16  # Step GPIO Pin
	en_pin = 21
	delay = 0.002
	def __init__(self,tgt_dir,tgt_step,tgt_en,tgt_delay):
		self.dir_pin = tgt_dir
		self.step_pin = tgt_step
		self.en_pin = tgt_en
		self.delay = tgt_delay
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.dir_pin,GPIO.OUT)
		GPIO.setup(self.step_pin,GPIO.OUT)
		GPIO.setup(self.en_pin,GPIO.OUT)
		GPIO.output(self.dir_pin,GPIO.LOW)
		GPIO.output(self.en_pin,GPIO.LOW)
	def set_delay(self,tgt_delay):
		self.delay = tgt_delay
	def step(self,tgt_delay):
		GPIO.output(self.step_pin,GPIO.HIGH)
		sleep(tgt_delay)
		GPIO.output(self.step_pin,GPIO.LOW)
		sleep(tgt_delay)
	def run(self,tgt_steps,tgt_cw):
		if tgt_cw:
			GPIO.output(self.dir_pin,GPIO.HIGH)
		else:
			GPIO.output(self.dir_pin,GPIO.LOW)
		for i in range(0,tgt_steps):
			self.step(self.delay)
	def ease(self,tgt_steps,tgt_cw):
		if tgt_cw:
			GPIO.output(self.dir_pin,GPIO.HIGH)
		else:
			GPIO.output(self.dir_pin,GPIO.LOW)
		for i in range(0,int(tgt_steps*3/4)):
			self.step(self.delay)
		for i in range(0,int(tgt_steps/4)):
			self.step(self.delay*4)
	def wiggle(self):
		wiggle_steps = 6
		#left 
		GPIO.output(self.dir_pin,GPIO.LOW)
		delay_modifier = 8
		for i in range(0,wiggle_steps):
			GPIO.output(self.step_pin,GPIO.HIGH)
			sleep(self.delay/delay_modifier)
			GPIO.output(self.step_pin,GPIO.LOW)
			sleep(self.delay/delay_modifier)
		GPIO.output(self.dir_pin,GPIO.HIGH)
		for i in range(0,wiggle_steps):
			GPIO.output(self.step_pin,GPIO.HIGH)
			sleep(self.delay/delay_modifier)
			GPIO.output(self.step_pin,GPIO.LOW)
			sleep(self.delay/delay_modifier)
	def runDelay(self,tgt_steps,tgt_cw,tgt_delay):
		if tgt_cw:
			GPIO.output(self.dir_pin,GPIO.HIGH)
		else:
			GPIO.output(self.dir_pin,GPIO.LOW)
		for i in range(tgt_steps):
			GPIO.output(self.step_pin,GPIO.HIGH)
			sleep(tgt_delay)
			GPIO.output(self.step_pin,GPIO.LOW)
			sleep(tgt_delay)
