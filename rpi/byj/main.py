#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import sys

in1 = 17
in2 = 18
in3 = 27
in4 = 22

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.02

step_count = 4096*1 # 5.625*(1/64) per step, 4096 steps is 360°
step_count = 1000
direction = False # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# setting up
def setup():
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( in1, GPIO.OUT )
    GPIO.setup( in2, GPIO.OUT )
    GPIO.setup( in3, GPIO.OUT )
    GPIO.setup( in4, GPIO.OUT )

    # initializing
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )


motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0


def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()


# the meat
def run_motor(tgt_direction,tgt_step_speed):
    i = 0
    motor_step_counter = 0
    cur_step_count = 10
    for i in range(cur_step_count):
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
        if tgt_direction==True:
            motor_step_counter = (motor_step_counter - 1) % 8
        elif tgt_direction==False:
            motor_step_counter = (motor_step_counter + 1) % 8
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
        time.sleep( tgt_step_speed )

def main():
    # print main.py 100 ccw 0.02
    print(sys.argv[1],sys.argv[2],sys.argv[3])
    setup()
    cur_cycle = int(sys.argv[1])
    cur_step_speed = float(sys.argv[3])
    try:
        for i in range(cur_cycle):
            if sys.argv[2] == "ccw":
                run_motor(True,cur_step_speed)
            else:
                run_motor(False,cur_step_speed)
        cleanup()
    except:
        e = sys.exec_info()[0]
        print(e)
        cleanup()


if __name__ == '__main__':
    setup()
    main()
