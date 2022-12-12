from numpy import in1d, int32
import RPi.GPIO as GPIO
import time

class Stepper:
    stepper_pin_list = [5,6,12,13]
    step_sequence = [[1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1],
                 [1,0,0,1]]
    cur_position = 0
    stepper_delay = 0.00001
    moving = False
    def __init__(self,tgt_pin_list):
        self.stepper_pin_list = tgt_pin_list
        GPIO.setmode(GPIO.BCM)
        for cur_pin in self.stepper_pin_list:
            GPIO.setup( cur_pin, GPIO.OUT )
            GPIO.output( cur_pin, GPIO.LOW )
        # style
        self.stepper_delay = 0.00001
    def set_delay(self,tgt_delay):
        self.stepper_delay = tgt_delay

    def set_position(self,tgt_pos):
        self.cur_position = tgt_pos
    def cleanup(self):
        for cur_pin in self.stepper_pin_list:
            GPIO.output(cur_pin,GPIO.LOW)
    def move(self,tgt_step_count,tgt_dir):
        i = 0
        motor_step_counter = 0
        self.moving = True
        for i in range(tgt_step_count):
            if tgt_dir == True:
                self.cur_position -= 1
            if tgt_dir == False:
                self.cur_position += 1
            cur_sequence = self.cur_position % len(self.step_sequence)
            for cur_pin in range(0, len(self.stepper_pin_list)):
                GPIO.output( self.stepper_pin_list[cur_pin], self.step_sequence[cur_sequence][cur_pin] )
            time.sleep(self.stepper_delay)
        self.cleanup()
        self.moving = False
    def is_moving(self):
        return self.moving
    def set_home(self):
        self.cur_position = 0
        return self.cur_position
    def get_pos(self):
        return self.cur_position
