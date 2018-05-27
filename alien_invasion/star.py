from pygame.sprite import Sprite 
import pygame,sys
import datetime



class Star(Sprite):

	def __init__(self,ai_settings,screen):
		super().__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		self.image=pygame.image.load('images/star.bmp')
		self.rect=self.image.get_rect()
		self.screen_rect=screen.get_rect()
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom-20
		self.starttime = datetime.datetime.now()

	def show_star(self):
		# clock=pygame.time.Clock()
		# time_passed=clock.tick()
		endtime = datetime.datetime.now()
		if (endtime - self.starttime).seconds>5 :
			# print ((endtime - self.starttime).seconds)
			self.screen.blit(self.image,self.rect)
