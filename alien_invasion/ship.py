import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self,ai_settings,screen):
		"""初始化飞船并设置其初始位置"""
		super().__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		# self.image=pygame.image.load('images/ship.bmp')
		self.image=pygame.image.load('images/ship.bmp')
		self.rect=self.image.get_rect()
		self.screen_rect=screen.get_rect()
		# 将每艘新飞船放在屏幕底部中央
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom
		# 在飞船的属性center中存储小数值
		self.center=float(self.rect.centerx)
		self.bottom=float(self.rect.bottom)

		# 移动标志
		self.moving_right=False
		self.moving_left=False
		self.moving_up=False
		self.moving_down=False
		self.fire_bullets=False



	def update(self):
		"""根据移动标志调整飞船的位置"""
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.center+=self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left>0:
			self.center-=self.ai_settings.ship_speed_factor
		self.rect.centerx=self.center

		if self.moving_up and self.rect.top>0:
			self.bottom-=self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
			self.bottom+=self.ai_settings.ship_speed_factor
		self.rect.bottom=self.bottom




	def center_ship(self):
		"""让飞船在屏幕上居中"""
		self.center=self.screen_rect.centerx
		self.bottom=self.screen_rect.bottom




	def blitme(self):
		self.screen.blit(self.image,self.rect)