#from numpy import in1d, int32
import RPi.GPIO as GPIO
import time

class Endstop:
	endstop_pin = 25
	def __init__(self,tgt_es_pin):
		GPIO.setmode(GPIO.BCM)
		self.endstop_pin = tgt_es_pin
		GPIO.setup( tgt_es_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
	def is_engaged(self):
		if GPIO.input(self.endstop_pin)==GPIO.HIGH:
			return True
		else:
			return False
