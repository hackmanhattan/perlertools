from time import sleep
import RPi.GPIO as GPIO
import sys

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)
EN = 16
delay = 0.1

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
    cur_delay = float(sys.argv[1])
    try:
        # enable
        GPIO.output(EN,GPIO.LOW)
        step_count = SPR * 10
        print("SPIN ONE WAY")
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

    except:
        GPIO.cleanup()

if __name__ == '__main__':
    sys.exit(main()) 