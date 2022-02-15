from .hexcolor import *

import pygame
from pygame.locals import *
from colour import Color
class ColorBin(pygame.sprite.Sprite):
	threshold = -1 # -1 = unsorted
	color = Color("#777777")
	beadlist = []
	rect = pygame.Rect(0,0,50,50)
	surf = 0
	smallfont = 0
	bead_width = 0
	def __init__(self,tgt_color,tgt_threshold,tgt_bead_width):
		super(ColorBin, self).__init__()
		self.color = tgt_color
		self.threshold = tgt_threshold
		self.beadlist = []
		self.surf = pygame.Surface((50, 50))
		self.surf.fill(hex_tuple(self.color))
		self.rect = self.surf.get_rect()
		pygame.font.init()
		self.smallfont = pygame.font.SysFont('Arial',35)
		self.bead_width = tgt_bead_width - 10
	def move_to(self,x,y):
		self.rect.x = x
		self.rect.y = y
	def set_threshold(self,tgt_threshold):
		self.threshold = tgt_threshold
	def compare_color(self,tgt_color):
		res = get_difference(self.color,tgt_color)
		return res
	def get_color(self):
		return self.color
	def check_color_match(self,tgt_color):
		res = get_difference(self.color,tgt_color)
		if res < self.threshold:
			return True
		return False
	def get_bead_count(self):
		return len(self.beadlist)
	def check_hsv_match(self,tgt_color):
		res = abs(self.color.hue - tgt_color.hue)
		#print("check_hsv_match",res)
		if res < self.threshold:
			return True
		return False
	def clear_bin(self):
		self.beadlist = []
	def draw_bin(self,DISPLAY):
		#draw bin
		DISPLAY.blit(self.surf,self.rect)
		cur_bead_rect = pygame.Rect(self.rect.x,self.rect.y,10,10)
		text = self.smallfont.render(str(len(self.beadlist)), True , hex_tuple(Color("black")))
		for idx in range(len(self.beadlist)):
			cur_x = self.rect.x + 60 + ((idx%self.bead_width)*12)
			cur_y = self.rect.y + int(idx/self.bead_width)*12
			self.beadlist[idx].move_to(cur_x,cur_y)
			self.beadlist[idx].draw_bead(DISPLAY)
		DISPLAY.blit(text,(self.rect.x-50,self.rect.y))
	def add_bead(self,tgt_bead):
		print("adding bead",tgt_bead.get_color())
		self.beadlist.append(tgt_bead)
