from colour import Color
from beadsort.hexcolor import *
screen_w = 1280
screen_h = 600
cam_w = 640
cam_h = 480
bead_loc_x = 360
bead_loc_y = 240
init_bin_y = 10
bead_dimension = 10
bead_x_cnt = int((screen_w - cam_w - bead_dimension -2) / (bead_dimension+2))

max_threshold = get_difference(Color("black"),Color("white"))
color_threshold = max_threshold/10