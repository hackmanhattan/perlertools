from colour import Color
from beadsort.hexcolor import *
screen_w = 1280
screen_h = 800

cam_w = 640
cam_h = 480

bead_loc_x = 325
bead_loc_y = 135
bead_loc_w = 40
bead_loc_h = 50
bead_loc_dimension = (bead_loc_w,bead_loc_h)
init_bin_y = cam_h

bead_dimension = 10
bead_x_cnt = int((screen_w - cam_w - bead_dimension -2) / (bead_dimension+2))

color_wheel_x = 900
color_wheel_y = 400

max_threshold = get_difference(Color("black"),Color("white"))
color_threshold = max_threshold/10
def_threshold = color_threshold*0.25

motor_duration = 0.4
wiggle_delay = motor_duration * 0.5
motor_delay = 0.2

position_dict = {}
position_dict["graveyard"] = 1505
position_dict["home"] = 1795
position_dict["filter"] = 2095


color_x = cam_w + 10
color_y = 10

servo_win_x = cam_w + 10
servo_win_y = color_y + 160 + 10

servo_delay = 0.0015
servo_interval = 2.5

def_color = "#4d4e4a"
bead_yellow = "#faef6e"
bead_blue = "#baefed"

stepper_pin_list = [5,6,12,13]
stepper_interval =  int(2048/8)

max_bin = 10