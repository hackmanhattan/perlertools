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
logging.basicConfig(filename="./example.log", level=logging.DEBUG)
logging.info("test")
pygame.init()
logging.info("testb")
smallfont = pygame.font.SysFont('Arial',35)
servo = Servo(23)
motor = Motor(24) #needs to start off
color_000 = Color("black")
pos_key_list = list(position_dict.keys())
DISPLAY= pygame.display.set_mode((screen_w, screen_h))
#LOG CONFIG
cam = ColorCam()

#FONT

servo_delay = 0.001

def get_bead():
	#check if bead exists
	servo.set_pos_delay(position_dict["home"],servo_delay,True)
	cur_color = cam.get_color(bead_loc_x,bead_loc_y)
	default_color = cam.get_default_color()
	cur_diff = get_difference(cur_color,default_color)
	draw_cam_color(cam)
	while cur_diff < color_threshold*0.2:
		servo.set_pos_delay(position_dict["home"],servo_delay,True)
		motor.run_delay(motor_duration,motor_delay)
		time.sleep(1)
		cur_color = cam.get_color(bead_loc_x,bead_loc_y)
		cur_diff = get_difference(cur_color,default_color)
		draw_cam_color(cam)
	print("found diff",cur_diff)
	#return bead
	ret_bead = Bead(cur_color)
	print("creating bead with color ",cur_color)
	pygame.display.update()
	return ret_bead

def draw_cam_color(tgt_cam):
	init_y = cam_h - 60
	def_color = tgt_cam.get_default_color()
	def_rect = pygame.Rect(100,init_y,50,70)
	def_surf = pygame.Surface((50, 70))
	def_surf.fill(hex_tuple(def_color))
	DISPLAY.blit(def_surf,def_rect)
	def_text = smallfont.render("default",True,hex_tuple(color_000))
	DISPLAY.blit(def_text,(10,init_y))

	init_y+=80
	cur_color = tgt_cam.get_color(bead_loc_x,bead_loc_y)
	cam_rect = pygame.Rect(100,init_y,50,70)
	cam_surf = pygame.Surface((50,70))
	cam_surf.fill(hex_tuple(cur_color))
	DISPLAY.blit(cam_surf,cam_rect)
	cam_text = smallfont.render("CAM",True,hex_tuple(color_000))
	DISPLAY.blit(cam_text,(10,init_y))
	pygame.display.update()

def sort_bead(tgt_bead,tgt_bin_list):
	tgt_diff = 1000
	ret_idx = len(tgt_bin_list)-1
	for bin_idx in range(0,len(tgt_bin_list)-1):
		cur_bin = tgt_bin_list[bin_idx]
		cur_diff = cur_bin.compare_color(tgt_bead.get_color())
		if cur_bin.check_color_match(tgt_bead.get_color()) and cur_diff < tgt_diff:
			tgt_diff = cur_diff
			ret_idx = bin_idx
	return ret_idx

def refresh_servo():
	servo_color = Color("gray") 
	if servo.check_moving() is 1:
		servo_color = Color("green")

	servo_status_rect = pygame.Rect(servo_win_x,servo_win_y,50,30)
	servo_status_surf = pygame.Surface((50, 30))
	servo_status_surf.fill(hex_tuple(servo_color))
	DISPLAY.blit(servo_status_surf,servo_status_rect)
	servo_pos = servo.get_pos()
	text = smallfont.render(str(servo_pos), True ,hex_tuple(color_000))
	DISPLAY.blit(text,(servo_status_rect.x-50,servo_status_rect.y))
	textb = smallfont.render(servo.get_action(),True,hex_tuple(color_000))
	DISPLAY.blit(textb,(servo_status_rect.x-50,servo_status_rect.y+30))
def refresh_bins(tgt_bin_list):
	DISPLAY.fill(hex_tuple(Color("white"))) #clear screen
	for idx in range(len(tgt_bin_list)):
		tgt_bin_list[idx].move_to(cam_w+10,init_bin_y + idx*52)
		tgt_bin_list[idx].draw_bin(DISPLAY)

def init_cam():
	default_color = cam.get_color(bead_loc_x,bead_loc_y)
	cam.set_default_color(default_color)
	cam.set_overlay_img(bead_loc_x,bead_loc_y,default_color)
	cam.add_overlay()
def main():
	#init code
	filter_bin = ColorBin(Color("black"),-1,bead_x_cnt)
	filter_bin.move_to(cam_w+10,10)
	red_bin = ColorBin(Color("#bc2c33"),color_threshold,bead_x_cnt)
	red_bin.move_to(cam_w+10,62)
	bin_list = [red_bin,filter_bin]
	# default color_assume empty chamber
	servo.set_pos(position_dict["home"])
	init_cam()
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_LEFT:
					servo.set_pos(servo.get_pos()+servo_interval)
				if event.key == pygame.K_RIGHT:
					servo.set_pos(servo.get_pos()-servo_interval)
				if event.key == pygame.K_q: # dispense to graveyard
					logging.info("graveyard")
					print("graveyard")
					servo.move(position_dict["graveyard"],servo_delay,True)
				if event.key == pygame.K_e: # dispense to filter
					logging.info("filter")
					servo.move(position_dict["filter"],servo_delay,True)
				if event.key == pygame.K_w: # to home
					logging.info("home")
					servo.move(position_dict["home"],servo_delay,True)
					time.sleep(1)
				if event.key == pygame.K_t:
					print("setting default")
					cur_color = cam.get_color(bead_loc_x,bead_loc_y)
					cam.set_default_color(cur_color)
					cam.remove_overlay()
					cam.set_overlay_img(bead_loc_x,bead_loc_y,cur_color)
					cam.add_overlay()
				if event.key == pygame.K_s:
					if len(bin_list) == 1: # add bin
						cur_bead = get_bead()
						print("creating bin",cur_bead.get_color())
						new_bin = ColorBin(cur_bead.get_color(),color_threshold,bead_x_cnt)
						new_bin.add_bead(cur_bead)
						bin_list.insert(0,new_bin)
						servo.set_pos(position_dict["filter"])
						# servo.move(position_dict["filter"],0.2,True)
						motor.run_delay(motor_duration,motor_delay)
					else:
						for i in range(100):
							cur_bead = get_bead()
							bin_idx = sort_bead(cur_bead,bin_list)
							bin_list[bin_idx].add_bead(cur_bead)
							if bin_idx==0:
								print("filtering bead")
								
								servo.set_pos_delay(position_dict["filter"],servo_delay,True)
							else:
								print("burying bead")
								servo.set_pos_delay(position_dict["graveyard"],servo_delay,True)
								
							motor.run_delay(motor_duration,motor_delay)
							servo.set_pos(position_dict["home"])
							motor.run_delay(motor_duration,motor_delay)
							print("homing")
							refresh_bins(bin_list)
							pygame.display.update()
				if event.key == pygame.K_a:
					logging.info("run_motor")
					motor.run_delay(motor_duration,motor_delay)
		refresh_bins(bin_list)
		refresh_servo()
		draw_cam_color(cam)
		pygame.display.update()
if __name__ == "__main__":
	main()
