# Import libraries
import RPi.GPIO as GPIO
import time
from servo import *
from pynput.keyboard import Key,Listener,KeyCode
from pynput import keyboard
servo = Servo(23)
motor_pin = 14
motor_delay = 1.2
pos_list = [4.4,5.8,7.4]
cur_pos = 1.0
def on_press(key):
	tgt_pos = servo.get_pos()
	if key==Key.up:
		tgt_pos += 0.1
		servo.set_pos(tgt_pos)
	if key==Key.down:
		tgt_pos -= 0.1
		servo.set_pos(tgt_pos)
	if str(key)=="'q'":
		tgt_pos = pos_list[0]
		servo.set_pos(tgt_pos)
		time.sleep(1)
		tgt_pos = pos_list[1]
		servo.set_pos(tgt_pos)
	if str(key)=="'e'":
		tgt_pos = pos_list[2]
		servo.set_pos(tgt_pos)
		time.sleep(motor_delay)
		tgt_pos = pos_list[1]
		servo.set_pos(tgt_pos)
	if key==Key.left:
		GPIO.output(motor_pin,GPIO.HIGH)
		time.sleep(motor_delay)
		GPIO.output(motor_pin,GPIO.LOW)
	print(servo.get_pos())
try:
	threshold = 120
	# GPIO INIT
	tgt_pos = 0.0
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(motor_pin,GPIO.OUT)
	idx = 0
	listener = keyboard.Listener(on_press=on_press)
	listener.start()
	while True:
		idx+=1
		if idx > 1000:
			idx = 0
    #while True:
        #Ask user for angle and turn servo to it
    #    angle = int(input('Enter angle between 0 & 100: '))
        #angle = 2+(angle/18)
        #servo1.ChangeDutyCycle(2+(angle/18))
    #    servo.run(angle)
    #    time.sleep(1)
    #    #servo1.ChangeDutyCycle(0)

finally:
    #Clean things up at the end
    #servo1.stop()
	
	GPIO.cleanup()
	print("Servo Stop")
