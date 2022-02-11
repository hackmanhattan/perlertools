import pygame
from pygame.locals import *
from hexcolor import *
from colour import Color
import math
import sys
from bead import *
from colorbin import *
screen_width = 1000
screen_height = 500
DISPLAY=pygame.display.set_mode((screen_width,screen_height),0,32)

# determine bead dimensions
bead_x_margin = 100
bead_hopper_cnt = 2123
bead_dimension = 10
bead_x_cnt = int((screen_width - bead_x_margin) / (bead_dimension+2))
bead_y_cnt = int(bead_hopper_cnt / bead_x_cnt)
# max color
max_threshold = get_difference(Color("white"),Color("black"))
tgt_threshold = max_threshold/10
def generate_random_beads(bead_cnt):
	ret_list = []
	for idx in range(bead_cnt):
		cur_x = int((bead_x_margin/2) + (idx%bead_x_cnt)*(bead_dimension+2))
		cur_y = (int(idx/bead_x_cnt)+1) * (bead_dimension+2)
		cur_bead = Bead()
		cur_bead.move_to(cur_x,cur_y)
		cur_bead.set_random_color()
		ret_list.append(cur_bead)
	return ret_list

def refresh_screen(tgt_bead_list,tgt_bin_list):
	w = screen_width - bead_x_margin
	h = (int(len(tgt_bead_list)/bead_x_cnt)+1) * (bead_dimension+2)
	back_surf = pygame.Surface((w, h))
	rect = pygame.Rect(bead_x_margin/2,bead_dimension+2,w,h)
	back_surf.fill(hex_tuple(Color("gray")))
	DISPLAY.blit(back_surf,rect )
	for cur_bead in tgt_bead_list:
		cur_bead.draw_bead(DISPLAY)
	# init bin y
	init_bin_y = h + (bead_dimension+2)*2
	for idx in range(len(tgt_bin_list)):
		tgt_bin_list[idx].move_to(bead_x_margin/2,init_bin_y + idx*52)
		tgt_bin_list[idx].draw_bin(DISPLAY)
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
def main():
	pygame.init()
	bead_list = generate_random_beads(bead_hopper_cnt)
	# generate bin list
	filter_bin = ColorBin(Color("black"),-1,bead_x_cnt)
	filter_bin.move_to(bead_x_margin/2,(bead_y_cnt+3)*(bead_dimension+2))
	bin_list = [filter_bin]
	sort_mode = False
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_a:
					cur_color = bead_list[-1].get_color()
					if len(bin_list)==1 or sort_bead(bead_list[-1],bin_list) == len(bin_list)-1:
						new_bin = ColorBin(cur_color,tgt_threshold,bead_x_cnt)
						new_bin.add_bead(bead_list[-1])
						bin_list.insert(0,new_bin)
						bead_list.pop(-1)
				if event.key == pygame.K_s:
					sort_mode = not sort_mode
		if sort_mode and len(bead_list)>0:
			cur_bead = bead_list[-1]
			bin_idx = sort_bead(cur_bead,bin_list)
			bin_list[bin_idx].add_bead(cur_bead)
			bead_list.pop(-1)

		DISPLAY.fill(hex_tuple(Color("white")))
		refresh_screen(bead_list,bin_list)
		pygame.display.update()
main()
