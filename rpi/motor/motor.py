# Import libraries
import RPi.GPIO as GPIO
import time

class Motor:
	motor_pin = 14
	def __init__(self,tgt_pin):
		self.motor_pin = tgt_pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.motor_pin,GPIO.OUT)
		GPIO.output(self.motor_pin,GPIO.LOW)
	def run(self,tgt_delay):
		GPIO.output(self.motor_pin,GPIO.HIGH)
		time.sleep(tgt_delay)
		GPIO.output(self.motor_pin,GPIO.LOW)
