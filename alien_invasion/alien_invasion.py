import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from star import Star
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	# 初始化pygame、设置和屏幕对象
	pygame.init()
	ai_settings=Settings()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')
	play_button=Button(ai_settings,screen,"FUCK")

	# 创建一个用于存储游戏统计信息的实例
	stats=GameStats(ai_settings)

	ship=Ship(ai_settings,screen)
	# stars=Star(ai_settings,screen)

	# 创建一个用于存储子弹的编组
	bullets=Group()
	stars=Group()
	aliens=Group()
	# 创建外星人群
	gf.create_fleet(ai_settings,stats,screen,ship,aliens)
	sb=Scoreboard(ai_settings,screen,stats)

	while True:
		gf.check_event(ai_settings,screen,stats,sb,play_button,ship,stars,aliens,bullets)
		if stats.game_active:
			ship.update()
			if ship.fire_bullets:
				gf.fire_bullet(ai_settings,screen,ship,bullets)
			gf.check_level(ai_settings,stats,screen,sb,ship,stars)
			gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
			gf.update_aliens(ai_settings,stats,screen,sb,ship,stars,aliens,bullets)
		gf.update_screen(ai_settings,screen,stats,sb,ship,stars,aliens,bullets,play_button)



run_game()