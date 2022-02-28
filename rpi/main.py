from byj.stepper import *
from picamcd.colorcam import *
import sys
import time
from servo.servo import *
from motor.motor import *
import pygame
from pygame.locals import *
from config import *
from beadsort.hexcolor import *
from beadsort.bead import *
from beadsort.colorbin import *
import logging
from threading import Thread
import math

logging.basicConfig(filename="./example.log", level=logging.DEBUG)
logging.info("test")
pygame.init()
logging.info("testb")
smallfont = pygame.font.SysFont('Arial',35)
servo = Servo(23,position_dict["home"])
motor = Motor(24) #needs to start off
color_000 = Color("black")
DISPLAY= pygame.display.set_mode((screen_w, screen_h))
#LOG CONFIG
cam = ColorCam()
cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
#color wheel
color_wheel_list = generate_circle_color(1)

def get_bead():
	#check if bead exists
	servo.set_pos_delay(position_dict["home"],servo_delay,True)
	default_color = cam.get_default_color()
	repeat_cnt = 4
	init_motor_delay = 0.01
	cur_diff = get_difference(cur_color,default_color)
	while cur_diff < def_threshold:
		for i in range(repeat_cnt):
			motor.run_delay(i*0.01,0.1)
		# cur_refresh_vals = cam.get_refresh_vals(bead_loc_x,bead_loc_y,bead_loc_dimension)
		# cur_refresh_vals = refresh_vals()
		# cur_color = cur_refresh_vals[0]
		# cur_diff = cur_refresh_vals[1]
		cur_diff = get_difference(cur_color,default_color)
		if cur_diff > def_threshold:
			break
		repeat_cnt+=1
		if repeat_cnt > 10:
			print("giving up")
			return Bead(Color("black"))
	#return bead
	ret_bead = Bead(cur_color)
	print("creating bead with color ",cur_color,"diff",cur_diff)
	return ret_bead

def get_tgt_bin(tgt_bead,tgt_bin_list):
	tgt_diff = 1000
	ret_idx = len(tgt_bin_list)-1
	for bin_idx in range(0,len(tgt_bin_list)-1):
		cur_bin = tgt_bin_list[bin_idx]
		cur_diff = cur_bin.compare_color(tgt_bead.get_color())
		if cur_bin.check_color_match(tgt_bead.get_color()) and cur_diff < tgt_diff:
			tgt_diff = cur_diff
			ret_idx = bin_idx
	return ret_idx

def sort_bead(tgt_bin_list):
	cur_bead = get_bead()
	bin_idx = get_tgt_bin(cur_bead,tgt_bin_list)
	tgt_bin_list[bin_idx].add_bead(cur_bead)
	if bin_idx==0:
		print("filtering bead")
		servo.set_pos_delay(position_dict["filter"],servo_delay,True)
		time.sleep(0.4)
		servo.set_pos(position_dict["filter"])
		time.sleep(0.3)
		motor.wiggle(1)
	else:
		print("burying bead")
		servo.set_pos_delay(position_dict["graveyard"],servo_delay,True)	
	motor.run_delay(wiggle_delay,motor_delay)
	# servo.set_pos_delay(position_dict["home"],servo_delay,True)
	servo.set_pos_delay(position_dict["home"],servo_delay,True)
	time.sleep(0.25)
	servo.set_pos(position_dict["home"])
	time.sleep(0.4)
	motor.run_delay(wiggle_delay*0.5,motor_delay)
	print("going home")

def refresh_vals():
	tmp_color = None
	while tmp_color is None:
		try:
			tmp_color = cam.get_refresh_vals(bead_loc_x,bead_loc_y,bead_loc_dimension)
		except:
			tmp_color = None
	return tmp_color
def draw_cam_color():
	init_y = color_y
	def_color = cam.get_default_color()
	global cur_color
	# print("draw_cam",cur_color)
	# cur_refresh_vals = cam.get_refresh_vals(bead_loc_x,bead_loc_y,bead_loc_dimension)
	# cur_refresh_vals = refresh_vals()
	def_rect = pygame.Rect(color_x+120,init_y,50,70)
	def_surf = pygame.Surface((50, 70))
	def_surf.fill(hex_tuple(def_color))
	DISPLAY.blit(def_surf,def_rect)
	def_text = smallfont.render("default",True,hex_tuple(color_000))
	DISPLAY.blit(def_text,(color_x,init_y))
	def_rgb = smallfont.render(str(def_color),True,hex_tuple(color_000))
	DISPLAY.blit(def_rgb,(color_x+180,init_y))

	init_y+=80
	draw_color = cur_color
	cam_rect = pygame.Rect(color_x+120,init_y,50,70)
	cam_surf = pygame.Surface((50,70))
	cam_surf.fill(hex_tuple(draw_color))
	DISPLAY.blit(cam_surf,cam_rect)
	cam_text = smallfont.render("CAM",True,hex_tuple(color_000))
	DISPLAY.blit(cam_text,(color_x,init_y))
	cam_rgb = smallfont.render(str(draw_color),True,hex_tuple(color_000))
	DISPLAY.blit(cam_rgb,(color_x+180,init_y))
	
	cam_diff_str = get_difference(def_color,cur_color)#str(cur_refresh_vals[1])
	cam_diff_str = round(cam_diff_str,5)
	cam_diff_str = str(cam_diff_str) + " / " + str(def_threshold)
	cam_diff = smallfont.render(cam_diff_str,True,hex_tuple(color_000))
	DISPLAY.blit(cam_diff,(color_x+350,init_y))
	#draw color wheel match
	cur_w = 0
	cur_radius = 10
	angle_interval = math.radians(360/len(color_wheel_list))
	wheel_radius = 150
	cur_closest_idx = 0
	cur_diff = 1000.0
	closest_idx = get_closest_wheel_color(draw_color,color_wheel_list)
	for idx in range(len(color_wheel_list)):
		tmp_color = hex_tuple(color_wheel_list[idx])
		cur_angle = angle_interval * idx
		cur_x = int(wheel_radius * math.cos(cur_angle) + color_wheel_x)
		cur_y =  int(wheel_radius * math.sin(cur_angle) + color_wheel_y)
		tmp_radius = cur_radius
		if idx == closest_idx:
			tmp_radius = 20
		pygame.draw.circle(DISPLAY,tmp_color,(cur_x,cur_y),tmp_radius)
	# blit idx val
	hsl_diff_str = get_hsl_difference(draw_color,color_wheel_list[closest_idx])
	hsl_diff_str = "HSL: " + str(round(hsl_diff_str,5))
	rgb_diff_str = get_difference(draw_color,color_wheel_list[closest_idx])
	rgb_diff_str = "RGB: " + str(round(rgb_diff_str,5)) + "/" + str(round(max_threshold,5))
	hsl_text = smallfont.render(hsl_diff_str,True,hex_tuple(color_000))
	DISPLAY.blit(hsl_text,(color_wheel_x-80,color_wheel_y-20))
	rgb_text = smallfont.render(rgb_diff_str,True,hex_tuple(color_000))
	DISPLAY.blit(rgb_text,(color_wheel_x-80,color_wheel_y+20))
	# wheel_idx_text = smallfont.render(str(closest_idx)+":"+,True,hex_tuple(color_000))
	# DISPLAY.blit(wheel_idx_text,(color_wheel_x,color_wheel_y))
	pygame.display.update()
	return draw_color

def refresh_servo():
	servo_color = Color("gray") 
	if servo.check_moving() is 1:
		servo_color = Color("green")
	servo_pos = servo.get_pos()
	text = smallfont.render(str(servo_pos), True ,hex_tuple(color_000))
	DISPLAY.blit(text,(servo_win_x,servo_win_y))

	servo_status_rect = pygame.Rect(servo_win_x+120,servo_win_y,50,30)
	servo_status_surf = pygame.Surface((50, 30))
	servo_status_surf.fill(hex_tuple(servo_color))
	DISPLAY.blit(servo_status_surf,servo_status_rect)

	textb = smallfont.render(servo.get_action(),True,hex_tuple(color_000))
	DISPLAY.blit(textb,(servo_win_x+200,servo_win_y))




def refresh_bins(tgt_bin_list):
	for idx in range(len(tgt_bin_list)):
		tgt_bin_list[idx].move_to(10,init_bin_y + idx*52)
		tgt_bin_list[idx].draw_bin(DISPLAY)

def init_cam():
	# default_color = cam.get_color(bead_loc_x,bead_loc_y)
	default_color = Color("#413c3e") #hardcode
	cam.set_default_color(default_color)
	cam.set_default_viewport(bead_loc_x,bead_loc_y,bead_loc_dimension)
	cam.set_overlay_img(bead_loc_x,bead_loc_y,bead_loc_dimension,default_color)
	# cam.save_img_locally()

	cam.add_overlay()
	cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
def main():
	# generate circle

	#init code
	print(position_dict)
	filter_bin = ColorBin(Color("black"),-1,bead_x_cnt)
	filter_bin.move_to(cam_w+10,10)
	red_bin = ColorBin(Color("#700a13"),color_threshold,bead_x_cnt) #0a3616 green
	red_bin.move_to(cam_w+10,62)
	bin_list = [red_bin,filter_bin]
	# default color_assume empty chamber
	servo.set_pos(position_dict["home"])
	init_cam()
	sort_mode = False
	motion_thread = Thread()
	while True:
		global cur_color
		cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
		# print("main loop",cur_color)
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_LEFT:
					servo.set_pos(servo.get_pos()-servo_interval)
				if event.key == pygame.K_RIGHT:
					servo.set_pos(servo.get_pos()+servo_interval)
				if event.key == pygame.K_q: # dispense to graveyard
					logging.info("graveyard")
					servo.set_pos_delay(position_dict["graveyard"],servo_delay,True)
				if event.key == pygame.K_e: # dispense to filter
					logging.info("filter")
					servo.set_pos_delay(position_dict["filter"],servo_delay,True)
				if event.key == pygame.K_w: # to home
					logging.info("home")
					servo.set_pos_delay(position_dict["home"],servo_delay,True)
					time.sleep(1)
				if event.key == pygame.K_t:
					# cur_color = cam.get_refresh_vals(bead_loc_x,bead_loc_y,bead_loc_dimension)[0]
					cur_color = refresh_vals()[0]
					print("setting default",cur_color)
					cam.set_default_color(cur_color)
					cam.set_default_viewport(bead_loc_x,bead_loc_y,bead_loc_dimension)
					cam.remove_overlay()
					cam.set_overlay_img(bead_loc_x,bead_loc_y,bead_loc_dimension,cur_color)
					cam.add_overlay()
				if event.key == pygame.K_s:
					sort_mode = not sort_mode
				if event.key == pygame.K_a:
					logging.info("run_motor")
					motor.run_delay(wiggle_delay,motor_delay)
				if event.key == pygame.K_g:
					logging.info("run sequence")
				if event.key == pygame.K_h:
					for i in range(20):
						motor.run_delay(motor_delay + i*0.02,0.2)
		if sort_mode:
			if motion_thread.is_alive() is False:
				print("sorting bead")
				motion_thread = Thread(target=sort_bead,args=(bin_list,))
				motion_thread.start()
		DISPLAY.fill(hex_tuple(Color("white"))) #clear screen
		refresh_bins(bin_list)
		refresh_servo()
		draw_cam_color()
		pygame.display.update()
if __name__ == "__main__":
	main()
