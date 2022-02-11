from time import sleep
import RPi.GPIO as GPIO
import sys

DIR = 26   # Direction GPIO Pin
STEP = 19  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)
EN = 16
delay = 0.1

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EN,GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CW)

def step(move_forward):
    if move_forward:
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)            
        sleep(delay)
    else:
        GPIO.output(STEP, GPIO.LOW)            
        sleep(delay)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)


def main():
    init()
    cur_delay = float(sys.argv[1])
    try:
        # enable
        GPIO.output(EN,GPIO.LOW)
        step_count = SPR * 10
        print("SPIN ONE WAY ",sys.argv[1])
        for x in range(step_count):
            print("HIGH")
            GPIO.output(STEP, GPIO.HIGH)
            sleep(cur_delay)
            print("LOW")
            GPIO.output(STEP, GPIO.LOW)
            sleep(cur_delay)
        GPIO.cleanup()
    except:
        print("exit")
        GPIO.cleanup()

if __name__ == '__main__':
    sys.exit(main()) 
