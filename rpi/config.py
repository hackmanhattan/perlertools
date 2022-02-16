from colour import Color
from beadsort.hexcolor import *
screen_w = 1280
screen_h = 600
cam_w = 640
cam_h = 480
bead_loc_x = 380
bead_loc_y = 240
init_bin_y = 10
bead_dimension = 10
bead_x_cnt = int((screen_w - cam_w - bead_dimension -2) / (bead_dimension+2))

max_threshold = get_difference(Color("black"),Color("white"))
color_threshold = max_threshold/6

motor_duration = 0.1
motor_delay = 0.8

servo_win_x = 250
servo_win_y = cam_h - 40

servo_interval = 5.0