import pygame
from pygame.sprite import Sprite 
from random import choice

class Alien(Sprite):
	"""表示单个外星人的类"""
	def __init__(self,ai_settings,screen):
		super().__init__()
		self.screen=screen
		self.ai_settings=ai_settings

		# 加载外星人图像，并设置其rect属性
		self.image=pygame.image.load('images/alien.bmp')
		self.rect=self.image.get_rect()

		# 每个外星人最初都在屏幕左上角附近
		self.rect.x=self.rect.width
		self.rect.y=self.rect.height
		# fleet_direction为1表示向右移，为-1表示向左移
		choices=[-1,1]
		self.fleet_direction=choice(choices)
		self.updown_direction=-1
		# 存储外星人的准确位置
		# self.x=float(self.rect.x)

	def check_edges(self):
		"""如果外星人位于屏幕边缘，就返回True"""
		hit_right=True
		hit_left=True
		screen_rect=self.screen.get_rect()
		if self.rect.right>=screen_rect.right:
			return hit_right
		elif self.rect.left<=0:
			return hit_left

	def check_top_edge(self):
		hit_top=True
		if self.rect.top<=0:
			return hit_top


	def update(self):
		"""向右移动外星人"""
		self.rect.x+=self.ai_settings.alien_speed_factor*self.fleet_direction
		self.rect.y+=self.ai_settings.alien_speed_factor*self.updown_direction
		# self.rect.x=self.x	

	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image,self.rect)