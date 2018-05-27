import sys
import pygame
from bullet import Bullet
from alien import Alien
from star import Star
from time import sleep
from random import randint


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""更新子弹的位置，并删除已消失的子弹""" 
	# 更新子弹的位置
	bullets.update()
	# 删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
	# 检查是否有子弹击中了外星人 
	# 如果是这样，就删除相应的子弹和外星人
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""响应子弹和外星人的碰撞""" 
	# 删除发生碰撞的子弹和外星人
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score+=ai_settings.alien_points*len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	if len(aliens)==0:
		# 删除现有的子弹并新建一群外星人
		bullets.empty()
		ai_settings.increase_speed()
		stats.level+=1
		sb.prep_level()
		create_fleet(ai_settings,stats,screen,ship,aliens)

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
	elif event.key==pygame.K_q:
			sys.exit()
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
	elif event.key==pygame.K_UP:
		ship.moving_up=True
	elif event.key==pygame.K_DOWN:
		ship.moving_down=True
	elif event.key==pygame.K_SPACE:
		ship.fire_bullets=True

def fire_bullet(ai_settings,screen,ship,bullets):
	# 创建一颗子弹，并将其加入到编组bullets中
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False
	if event.key==pygame.K_UP:
		ship.moving_up=False
	elif event.key==pygame.K_DOWN:
		ship.moving_down=False
	elif event.key==pygame.K_SPACE:
		ship.fire_bullets=False


"""响应按键和鼠标事件"""
def check_event(ai_settings,screen,stats,sb,play_button,ship,stars,aliens,bullets):
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,stars,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,stars,aliens,bullets,mouse_x,mouse_y):
	"""在玩家单击Play按钮时开始新游戏"""
	button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active=True

		sb.prep_level()
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_ships()

		aliens.empty()
		bullets.empty()
		stars.empty()

		create_fleet(ai_settings,stats,screen,ship,aliens)
		ship.center_ship()


"""更新屏幕上的图像，并切换到新屏幕"""
def update_screen(ai_settings,screen,stats,sb,ship,stars,aliens,bullets,play_button):
	# 每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	"""在指定位置绘制飞船"""
	ship.blitme()
	stars.draw(screen)
	aliens.draw(screen)
	sb.show_score()
	# 让最近绘制的屏幕可见
	if not stats.game_active:
		play_button.draw_button()
	# pygame.display.flip()将不断更新屏幕，以显示元素的新位置，并在原来的位置隐藏元素， 从而营造平滑移动的效果。	
	pygame.display.flip()

def get_number_aliens_x(ai_settings,alien_width):
	"""计算每行可容纳多少个外星人"""
	available_space_x=ai_settings.screen_width-2*alien_width
	number_alines_x=int(available_space_x/(2*alien_width))
	return number_alines_x

def get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y=ai_settings.screen_height-3*alien_height-ship_height
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows

def create_alien(ai_settings,stats,screen,ship,aliens):
	alien=Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien_height=alien.rect.height
	number_alines_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	alien_x_number=randint(0,number_alines_x)
	alien_y_number=randint(0,number_rows)
	alien.rect.x = alien_width + 2 * alien_width * alien_x_number+randint(-alien_width,alien_width-30)
	alien.rect.y=alien_height+2*alien_height*alien_y_number+randint(0,alien_height)
	aliens.add(alien)
def create_fleet(ai_settings,stats,screen,ship,aliens):
	alien=Alien(ai_settings,screen)
	for a in range(int((stats.level)/2)+1):
		create_alien(ai_settings,stats,screen,ship,aliens)


def creat_one_star(ai_settings,stats,screen,ship,stars):
	star=Star(ai_settings,screen)
	alien=Alien(ai_settings,screen)
	star_width=star.rect.width
	number_alines_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	star_x_number=randint(0,number_alines_x)
	star_y_number=randint(0,number_rows)
	star.rect.x=star_width+2*star_width*star_x_number
	star.rect.y=star.rect.height+2*star.rect.height*star_y_number
	stars.add(star)

def create_some_star(ai_settings,stats,screen,ship,stars):
	star=Star(ai_settings,screen)
	for a in range(int((stats.level)/10)+1):
		creat_one_star(ai_settings,stats,screen,ship,stars)

def check_level(ai_settings,stats,screen,sb,ship,stars):
	check_ship_star_collisions(stats,sb,ship,stars)
	while stats.level%10==1 and stats.level_active:
		create_some_star(ai_settings,stats,screen,ship,stars)
		stats.level_active=False
	if stats.level%10==2:
		stats.level_active=True

def check_ship_star_collisions(stats,sb,ship,stars):
	found_star=pygame.sprite.spritecollideany(ship,stars)
	if found_star:
		stats.ships_left+=1
		stars.remove(found_star)
		sb.prep_ships()
 
def ship_hit(ai_settings,stats,screen,sb,ship,stars,aliens,bullets):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left>1:
		# 将ships_left减1
		stats.ships_left-=1
		sb.prep_ships()
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 创建一群新的外星人，并将飞船放到屏幕底端中央
		create_fleet(ai_settings,stats,screen,ship,aliens)
		ship.center_ship()
		# 暂停
		sleep(1)
	else:
		stats.game_active=False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,stars,aliens,bullets):
	"""检查是否有外星人到达了屏幕底端"""
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			# 像飞船被撞到一样进行处理
			ship_hit(ai_settings,stats,screen,sb,ship,stars,aliens,bullets)
			break
		
def check_fleet_edges(ai_settings,aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			alien.rect.y+=ai_settings.fleet_drop_speed
			alien.fleet_direction*=-1
			alien.rect.x+=ai_settings.alien_speed_factor*alien.fleet_direction
		if alien.check_top_edge():
			alien.updown_direction*=-1
			alien.rect.y+=ai_settings.alien_updown_speed*alien.updown_direction


def update_aliens(ai_settings,stats,screen,sb,ship,stars,aliens,bullets):
	"""检查是否有外星人位于屏幕边缘，并更新整群外星人的位置,更新外星人群中所有外星人的位置"""
	check_fleet_edges(ai_settings,aliens)
	aliens.update()

	# 检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,sb,ship,stars,aliens,bullets)
	check_aliens_bottom(ai_settings,stats,screen,sb,ship,stars,aliens,bullets)

def check_high_score(stats,sb):
	if stats.score>stats.high_score:
		stats.high_score=stats.score
		sb.prep_high_score()

