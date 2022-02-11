from byj.stepper import *
from picamcd.colorcam import *
import sys
import time
from servo.servo import *


wheel = Stepper([17,18,27,22])
sorter = Stepper([5,6,13,12])
servo = Servo(23)

cam = ColorCam()

drop_degree=110

def init():
	wheel.setSpeed(0.005)
	sorter.setSpeed(0.1)
	# servo init
	for key in position_dict:
		servo.set_pos_delay(position_dict[key],0.11)
	servo.set_pos_delay(position_dict["home"],.1)
def main():
	try:
		while True:
			print("cw?")
			time.sleep(3)
			time.sleep(3)
			#sorter.run_motor(True,drop_degree)
			#time.sleep(1)
			#print("ccw?")
			#sorter.run_motor(False,drop_degree)
			#time.sleep(1)
	except Exception as e:
		print("quit",e)
		#sorter.cleanup()
		#wheel.cleanup()
if __name__ == "__main__":
	init()
	main()
