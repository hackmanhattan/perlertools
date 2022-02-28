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
	def run(self,tgt_duration):
		GPIO.output(self.motor_pin,GPIO.HIGH)
		time.sleep(tgt_duration)
		GPIO.output(self.motor_pin,GPIO.LOW)
	def run_delay(self,tgt_duration,tgt_delay):
		GPIO.output(self.motor_pin,GPIO.HIGH)
		time.sleep(tgt_duration)
		GPIO.output(self.motor_pin,GPIO.LOW)
		time.sleep(tgt_delay)
	def wiggle(self,tgt_repeat_cnt):
		for i in range(tgt_repeat_cnt):
			GPIO.output(self.motor_pin,GPIO.HIGH)
			time.sleep(0.1 + i*0.1)
			GPIO.output(self.motor_pin,GPIO.LOW)
			time.sleep(0.2)
