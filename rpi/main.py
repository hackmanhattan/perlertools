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
motor = Motor(14)
color_000 = Color("black")
pos_key_list = list(position_dict.keys())
DISPLAY= pygame.display.set_mode((screen_w, screen_h))
#LOG CONFIG
cam = ColorCam()
cam.add_overlay(bead_loc_x,bead_loc_y)
#FONT

def_delay = 0.5

def get_bead():
	#check if bead exists
	cur_color = cam.get_color(bead_loc_x,bead_loc_y)
	cur_diff = get_difference(cur_color,cam.get_default_color())
	print(cur_diff)
	draw_cam_color(cam)
	while cur_diff < color_threshold*0.1:
		motor.run(0.3)
		time.sleep(2)
		# wiggle
		# servo.move(position_dict["home"],0.2,True)
		servo.wiggle()
		servo.set_pos(position_dict["home"])
		cur_color = cam.get_color(bead_loc_x,bead_loc_y)
		cur_diff = get_difference(cur_color,cam.get_default_color())
		print(cur_diff,color_threshold*0.1)
		draw_cam_color(cam)
	#return bead
	ret_bead = Bead()
	ret_bead.set_color(cur_color)
	pygame.display.update()
	return ret_bead

def draw_cam_color(tgt_cam):
	def_color = tgt_cam.get_default_color()
	def_rect = pygame.Rect(10,cam_h,50,70)
	def_surf = pygame.Surface((50, 70))
	def_surf.fill(hex_tuple(def_color))
	DISPLAY.blit(def_surf,def_rect)
	cur_color = tgt_cam.get_color(bead_loc_x,bead_loc_y)
	cam_rect = pygame.Rect(80,cam_h,50,70)
	cam_surf = pygame.Surface((50,70))
	cam_surf.fill(hex_tuple(cur_color))
	print(def_color,cur_color)
	DISPLAY.blit(cam_surf,cam_rect)


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

def refresh_servo(tgt_servo):
	servo_color = Color("gray") 
	if tgt_servo.check_moving():
		servo_color = Color("green")

	servo_status_rect = pygame.Rect(200,cam_h+2,50,50)
	servo_status_surf = pygame.Surface((50, 50))
	servo_status_surf.fill(hex_tuple(servo_color))
	DISPLAY.blit(servo_status_surf,servo_status_rect)
	servo_pos = tgt_servo.get_pos()
	text = smallfont.render(str(servo_pos), True ,hex_tuple(color_000))
	DISPLAY.blit(text,(servo_status_rect.x-50,servo_status_rect.y))
	textb = smallfont.render(servo.get_action(),True,hex_tuple(color_000))
	DISPLAY.blit(textb,(servo_status_rect.x-50,servo_status_rect.y+30))
def refresh_bins(tgt_bead_list,tgt_bin_list):
	DISPLAY.fill(hex_tuple(Color("white"))) #clear screen
	for idx in range(len(tgt_bin_list)):
		tgt_bin_list[idx].move_to(cam_w+10,init_bin_y + idx*52)
		tgt_bin_list[idx].draw_bin(DISPLAY)

def main():
	#init code
	filter_bin = ColorBin(Color("black"),-1,bead_x_cnt)
	filter_bin.move_to(cam_w+10,10)
	bin_list = [filter_bin]
	# default color_assume empty chamber
	default_color = cam.get_color(bead_loc_x,bead_loc_y)
	cam.set_default_color(default_color)
	servo.move(position_dict["home"],0.05,True)
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
					servo.set_pos(servo.get_pos()+0.1)
				if event.key == pygame.K_RIGHT:
					servo.set_pos(servo.get_pos()-0.1)
				if event.key == pygame.K_q: # dispense to graveyard
					logging.info("graveyard")
					print("graveyard")
					# servo.move(position_dict["graveyard"],def_delay,True)
					servo.set_pos(position_dict["graveyard"])
				if event.key == pygame.K_e: # dispense to filter
					logging.info("filter")
					print("filter")
					#servo.move(position_dict["filter"],def_delay,True)
					servo.set_pos(position_dict["filter"])
				if event.key == pygame.K_w: # to home
					logging.info("home")
					servo.move(position_dict["home"],def_delay,True)
					time.sleep(1)
					servo.set_pos(position_dict["home"])
				if event.key == pygame.K_t:
					print("setting default")
					cur_color = cam.get_color(bead_loc_x,bead_loc_y)
					cam.set_default_color(cur_color)
				if event.key == pygame.K_s:
					cur_bead = get_bead()
					if len(bin_list) == 1: # add bin
						new_bin = ColorBin(cur_bead.get_color(),color_threshold,bead_x_cnt)
						new_bin.add_bead(cur_bead)
						bin_list.insert(0,new_bin)
					else:
						bin_idx = sort_bead(cur_bead,bin_list)
						bin_list[bin_idx].add_bead(cur_bead)
						if bin_idx==0:
							servo.set_pos(position_dict["filter"])
						else:
							servo.set_pos(position_dict["graveyard"])
				if event.key == pygame.K_a:
					logging.info("run_motor")
					motor.run(0.5)
		refresh_bins([],bin_list)
		refresh_servo(servo)
		draw_cam_color(cam)
		pygame.display.update()
if __name__ == "__main__":
	main()
