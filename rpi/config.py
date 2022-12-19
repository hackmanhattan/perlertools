from colour import Color
from beadsort.hexcolor import *
screen_w = 1280
screen_h = 800

cam_w = 640
cam_h = 480

bead_loc_x = 320
bead_loc_y = 354
bead_loc_w = 36
bead_loc_h = 36
bead_loc_dimension = (bead_loc_w,bead_loc_h)
init_bin_y = cam_h

bead_dimension = 10
bead_x_cnt = int((screen_w - cam_w - bead_dimension -2) / (bead_dimension+2))

color_wheel_x = 800
color_wheel_y = 350

max_threshold = get_difference(Color("black"),Color("white"))
color_threshold = max_threshold/8
def_threshold = max_threshold/5

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

def_color = "#ece4f4"
bead_yellow = "#faef6e"
bead_blue = "#baefed"

stepper_pin_list = [5,6,12,13]
stepper_interval =  32
stepper_full_rotation = 6592*2 # from measuring half
stepper_slot_rotation = int(stepper_full_rotation / 6)

max_bin = 10

# nema config
nema_interval=67
