import pygame
from pygame.locals import *
from hexcolor import *
from colour import Color
import math
screen_width = 1000
screen_height = 500
DISPLAY=pygame.display.set_mode((screen_width,screen_height),0,32)
def color_wheel(tgt_radius,tgt_color_list):
	# number of points in circle separation
	separation_degrees = int(360/len(tgt_color_list))
	print(separation_degrees)
	mp_x = screen_width/2
	mp_y = screen_height/2
	for i in range(len(tgt_color_list)):
		cur_angle = i * separation_degrees*(math.pi/180)
		cur_x = mp_x - math.sin(cur_angle)*tgt_radius
		cur_y = mp_y - math.cos(cur_angle)*tgt_radius
		print(i * separation_degrees, tgt_color_list[i].rgb)
		pygame.draw.circle(DISPLAY,hex_tuple(tgt_color_list[i]),(cur_x,cur_y),5)
def main():
	pygame.init()
	
	



	c_white=Color("white")
	c_red=Color("red")
	c_blue=Color("blue")
	c_green=Color("green")
	color_list = [c_red,c_green,c_blue]

	DISPLAY.fill(hex_tuple(c_white)) #back ground
	#loop color wheel
	for cycle in range(3):
		new_list = []
		for i in range(len(color_list)):
			next_color_idx = (i+1)%len(color_list)
			new_color = mix_color(color_list[i],color_list[next_color_idx])
			print("mix",color_list[i].rgb, color_list[next_color_idx].rgb)
			print("insert at ",i,new_color)
			new_list.append(color_list[i])
			new_list.append(new_color)
			#if i+1<len(color_list):
				#new_list.append(color_list[i+1])
			# new_list.append(color_list[-1])
		color_list = new_list
	block_width = int((screen_width-100)/len(color_list))
	for i in range(len(color_list)):
		pygame.draw.rect(DISPLAY,hex_tuple(color_list[i]),(i*block_width+50,0,block_width-2,50))
		# pygame.draw.circle(DISPLAY,hex_tuple(color_list[i]),(i*block_width+50,50),5)
	color_wheel(200,color_list)

	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
main()
