import pygame
from colour import Color
from hexcolor import *
import secrets
WHITE = (255, 255, 255)
RED = (255,0,0)

class Bead(pygame.sprite.Sprite):
	rect = pygame.Rect(0,0,10,10)
	color = Color("#222")
	surf = 0
	def __init__(self):
		super(Bead, self).__init__()
		self.surf = pygame.Surface((10, 10))
		self.surf.fill(hex_tuple(self.color))
		self.rect = self.surf.get_rect()
	def move_to(self,x,y):
		self.rect.x = x
		self.rect.y = y
	def resize(self,w,h):
		self.image = pygame.transform.scale(self.image,(w,h))
	def set_random_color(self):
		cur_hex = "#" + secrets.token_hex(3)
		self.color = Color(cur_hex)
		self.surf.fill(hex_tuple(self.color))
	def draw_bead(self,DISPLAY):
		DISPLAY.blit(self.surf,self.rect)
	def get_color(self):
		return self.color