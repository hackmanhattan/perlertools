from picamcd.colorcam import *
import sys
import time
from motor.motor import *
from stepper.stepper import *
import pygame
from pygame.locals import *
from config import *
from beadsort.hexcolor import *
from beadsort.bead import *
from beadsort.colorbin import *
import logging
from threading import Thread
import math
from nema.nema import *
from endstop.endstop import *
#LOG CONFIG
logging.basicConfig(filename="./example.log", level=logging.DEBUG)
pygame.init()
smallfont = pygame.font.SysFont('Arial',25)

color_000 = Color("black")
stepper = Stepper(stepper_pin_list)
stepper.set_delay(0.00070)
nema = Nema(20,16,21,0.004)
DISPLAY= pygame.display.set_mode((screen_w, screen_h))
cam = ColorCam()
cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
#color wheel
color_wheel_list = generate_circle_color(0)
bin_list = []
sort_endstop = Endstop(25)
def get_bead():
	default_color = cam.get_default_color()
	repeat_cnt = 1
	init_motor_delay = 0.01
	global cur_color
	cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)	
	cur_diff = get_difference(cur_color,default_color)
	global sort_mode
	while cur_diff < def_threshold:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					exit()
		# refresh_display()
		cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
		nema.run(4,True)
		cur_diff = get_difference(cur_color,default_color)
		if cur_diff > def_threshold:
			print("detected bead")
			break
		repeat_cnt+=1
		if repeat_cnt > 30:
			nema.run(18,False)
			repeat_cnt = 0
			print("giving up, jam?")
			#sort_mode = False
			#return Bead(Color("black"))
	#return bead
	#move forward a bit
	nema.run(6,True)
	cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
	ret_bead = Bead(cur_color)
	return ret_bead
def stepper_home():
	# home
	while sort_endstop.is_engaged() is False:
		stepper.move(stepper_interval,True)
		# DISPLAY.fill(hex_tuple(Color("white"))) #clear screen
		# refresh_bins()
		# refresh_stepper()
		# draw_cam_color()
		# pygame.display.update()
	stepper.set_position(0)
	stepper.cleanup()
def dispense_bead(tgt_bead_idx,tgt_debug=False):
	# move to correct slot
	print("moving to bead " + str(tgt_bead_idx))
	if tgt_debug:
		return
	move_interval = 32
	print("going to ",stepper.get_pos(),"vs",tgt_bead_idx*stepper_slot_rotation)
	while stepper.get_pos()>(tgt_bead_idx*stepper_slot_rotation*-1):
		stepper.move(move_interval,True)
	nema.run(58,True)
	time.sleep(0.5)
	# go back other way if okay
	if tgt_bead_idx<3:
		stepper.move(tgt_bead_idx*stepper_slot_rotation,False)
	else:
		stepper_home()
def get_tgt_bin(tgt_bead,tgt_bin_list):
	tgt_diff = 1000
	ret_idx = 0
	for bin_idx in range(1,len(bin_list)):
		cur_bin = bin_list[bin_idx]
		cur_diff = cur_bin.compare_color(tgt_bead.get_color())
		if cur_diff < tgt_diff and cur_diff < color_threshold:
			tgt_diff = cur_diff
			ret_idx = bin_idx
	print("setting bead to bin number",ret_idx,tgt_diff)
	tgt_bin_list[ret_idx].add_bead(tgt_bead)
	return ret_idx

def sort_bead(tgt_bin_list):
	cur_bead = get_bead()
	bin_idx = get_tgt_bin(cur_bead,bin_list)
	if bin_idx == 0 and len(bin_list)<max_bin:
		new_bin = ColorBin(cur_bead.get_color(),color_threshold,bead_x_cnt)
		# add bin
		bin_list.append(new_bin)
		bin_idx = len(bin_list)-1
	bin_list[bin_idx].add_bead(cur_bead)

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
	# first row
	def_text = smallfont.render("default",True,hex_tuple(color_000))
	DISPLAY.blit(def_text,(color_x,init_y))

	def_rect = pygame.Rect(color_x+80,init_y,50,70)
	def_surf = pygame.Surface((50, 50))
	def_surf.fill(hex_tuple(def_color))
	DISPLAY.blit(def_surf,def_rect)
 
	def_rect_b = pygame.Rect(color_x+140,init_y,50,70)
	def_surf_b = pygame.Surface((50, 50))
	tmp_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
	def_surf_b.fill(hex_tuple(tmp_color))
	DISPLAY.blit(def_surf_b,def_rect_b)

	def_rgb = smallfont.render(str(def_color) ,True,hex_tuple(color_000))
	DISPLAY.blit(def_rgb,(color_x+220,init_y))
	def_rgb = smallfont.render(str(tmp_color) ,True,hex_tuple(color_000))
	DISPLAY.blit(def_rgb,(color_x+220,init_y+24))

	init_y+=70
	# second row
	cam_text = smallfont.render("CAM",True,hex_tuple(color_000))
	DISPLAY.blit(cam_text,(color_x,init_y))

	draw_color = cur_color
	cam_rect = pygame.Rect(color_x+80,init_y,50,70)
	cam_surf = pygame.Surface((50,50))
	cam_surf.fill(hex_tuple(draw_color))
	DISPLAY.blit(cam_surf,cam_rect)

	cam_rgb = smallfont.render(str(draw_color),True,hex_tuple(color_000))
	DISPLAY.blit(cam_rgb,(color_x+140,init_y))
	
	cam_diff_str = get_difference(def_color,cur_color)
	cam_diff_str = round(cam_diff_str,5)
	cam_diff_str = str(cam_diff_str) + " / " + str(def_threshold)
	cam_diff = smallfont.render(cam_diff_str,True,hex_tuple(color_000))
	DISPLAY.blit(cam_diff,(color_x+140,init_y+25))
	#draw color wheel match
	cur_w = 0
	cur_radius = 10
	angle_interval = math.radians(360/len(color_wheel_list))
	wheel_radius = 80
	cur_closest_idx = 0
	cur_diff = 1000.0
	closest_idx = get_closest_wheel_color(draw_color,color_wheel_list)
	for idx in range(len(color_wheel_list)):
		tmp_color = hex_tuple(color_wheel_list[idx])
		cur_angle = (angle_interval * idx) - 90
		cur_x = int(wheel_radius * math.cos(cur_angle) + color_wheel_x)
		cur_y =  int(wheel_radius * math.sin(cur_angle) + color_wheel_y)
		tmp_radius = cur_radius

		if idx == closest_idx:
			tmp_radius = 20
		if idx == 0:
			tmp_radius = 5
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
	pygame.display.update()
	return draw_color

def refresh_stepper():
	stepper_color = Color("gray")
	if sort_endstop.is_engaged() is True:
		stepper_color = Color("green")
	stepper_pos = stepper.get_pos()
	pos_label_text = smallfont.render("POS: " + str(stepper_pos), True ,hex_tuple(color_000))
	DISPLAY.blit(pos_label_text,(servo_win_x,servo_win_y))

	stepper_status_rect = pygame.Rect(servo_win_x+180,servo_win_y,50,30)
	stepper_status_surf = pygame.Surface((50, 30))
	stepper_status_surf.fill(hex_tuple(stepper_color))
	DISPLAY.blit(stepper_status_surf,stepper_status_rect)

	# pos_text = smallfont.render(str(stepper.get_pos()), True ,hex_tuple(color_000))
	# DISPLAY.blit(pos_label_text,(servo_win_x+150,servo_win_y))


def refresh_bins():
	cur_bin_y = init_bin_y-20
	cur_x = 110
	for idx in range(0,len(bin_list)):
		bin_list[idx].move_to(cur_x,cur_bin_y)
		cur_bin_y += 52
		bin_list[idx].draw_bin(DISPLAY)
		if idx == int(max_bin/2)+1:
			cur_x += int(screen_w/2)
			cur_bin_y = init_bin_y-60

def init_cam():
	# default_color = cam.get_color(bead_loc_x,bead_loc_y)
	default_color = Color(def_color) #hardcode
	cam.set_default_color(default_color)
	cam.set_default_viewport(bead_loc_x,bead_loc_y,bead_loc_dimension)
	cam.set_overlay_img(bead_loc_x,bead_loc_y,bead_loc_dimension,default_color)
	cam.add_overlay()
	cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)

def refresh_display():
	DISPLAY.fill(hex_tuple(Color("white"))) #clear screen
	refresh_bins()
	refresh_stepper()
	draw_cam_color()
	pygame.display.update()
def main():
	# generate circle
	#init code
	print(position_dict)
	# default color_assume empty chamber
	init_cam()
	global sort_mode
	sort_mode = False
	global cur_color
	motion_thread = Thread()
	# generate preset bin
	for tmp_color in color_wheel_list:
		bin_list.append(ColorBin(tmp_color,color_threshold,bead_x_cnt))
	while True:	
		cur_color = cam.get_color(bead_loc_x,bead_loc_y,bead_loc_dimension)
		if sort_mode:
			tmp_bead = get_bead()
			tgt_bin_idx = get_tgt_bin(tmp_bead,bin_list)
			refresh_display()
			dispense_bead(tgt_bin_idx)
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_LEFT:
					nema.run(2,True)
				if event.key == pygame.K_RIGHT:
					nema.run(2,False)
				if event.key == pygame.K_q: # dispense to graveyard
					nema.run(nema_interval,True)
				if event.key == pygame.K_e: # dispense to filter
					nema.run(nema_interval,False)
				if event.key == pygame.K_w: # to home
					nema.ease(134,True)
				if event.key == pygame.K_i:
					stepper.move(stepper_interval,True)
				if event.key == pygame.K_p:
					stepper.move(stepper_interval,False)
				if event.key == pygame.K_k:
					stepper.cleanup()
				if event.key == pygame.K_l:
					tmp_bead = get_bead()
					tgt_bin_idx = get_tgt_bin(tmp_bead,bin_list)
					refresh_display()
					dispense_bead(tgt_bin_idx)
				if event.key == pygame.K_h:
					logging.info("home")
					stepper_home()
				if event.key == pygame.K_n:
					sort_mode = True
					tmp_bead = get_bead()
					tgt_bin_idx = get_tgt_bin(tmp_bead,bin_list)
					refresh_display()
					dispense_bead(tgt_bin_idx)
					nema.run(76,True)
				if event.key == pygame.K_m:
					sort_mode = False
				if event.key == pygame.K_j:
					tmp_stepper_pos = stepper_interval*20
					stepper.move(stepper_interval*20,True)
					while sort_endstop.is_engaged() is False:
						stepper.move(stepper_interval,True)
						time.sleep(0.005)
						tmp_stepper_pos += stepper_interval
					print(tmp_stepper_pos)
				if event.key == pygame.K_b:
					print("sort mode",sort_mode)
				if event.key == pygame.K_1:
					dispense_bead(1)
		refresh_display()
if __name__ == "__main__":
	main()
