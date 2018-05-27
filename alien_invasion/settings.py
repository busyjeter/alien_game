class Settings():
	def __init__(self):
		self.screen_width=1100
		self.screen_height=600
		self.bg_color=(230,230,230)

		self.ship_limit=3

		self.bullet_width=10
		self.bullet_height=20
		self.bullet_color=60,60,60
		self.bullets_allowed=50 

		self.fleet_drop_speed=1
		self.alien_updown_speed=1

		# 加快节奏
		self.speedup_scale=1.1
		self.score_scale=10

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""初始化随游戏进行而变化的设置"""
		self.bullet_speed_factor=10
		self.ship_speed_factor=30
		self.alien_speed_factor=7
		
		# # fleet_direction为1表示向右移，为-1表示向左移
		# self.fleet_direction=1
		self.alien_points=50

	def increase_speed(self):
		self.ship_speed_factor*=self.speedup_scale
		self.bullet_speed_factor*=self.speedup_scale
		self.alien_speed_factor*=self.speedup_scale
		self.bullets_allowed*=self.speedup_scale
		self.alien_points=int(self.alien_points*self.score_scale)


