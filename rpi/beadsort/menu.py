import pygame
from hexcolor import *
from colour import Color
from config import *

import json

screen_mid_x =int(screen_width / 2) 
screen_mid_y =int(screen_height / 2)

def drawMenuButtons(tgt_display):
	# Opening menumap file
	f = open('./menumap.json')

	# returns JSON object as
	# a dictionary
	menudata = json.load(f)
	smallfont = pygame.font.SysFont('Corbel',35)
	for menu_dict in menudata:
		cur_label = menu_dict["label"]
		text = smallfont.render(cur_label, True , hex_tuple(Color("black")))
		cur_pos = pygame.Rect(menu_dict["x"],menu_dict["y"],menu_dict["w"],menu_dict["h"])
		cur_color = Color(menu_dict["bg_c"])
		pygame.draw.rect(tgt_display,hex_tuple(cur_color),cur_pos)
		tgt_display.blit(text,(menu_dict["x"],menu_dict["y"]))