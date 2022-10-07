import pygame 
from settings import *
from entity import Entity
from support import import_folder

class Player(Entity):
	def __init__(self, pos, groups):
		super().__init__(groups)
		self.image = pygame.image.load('../image/player/Idle/idle01.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (200, 200))
		self.rect = self.image.get_rect(topleft = pos)

		self.hitbox = self.rect.inflate(-140,-130)
		self.hitbox_offset = (0,30)
		self.hitbox_origin = self.rect

		self.scale = (200, 200)
		self.inputFlag = True

		# graphics setup
		self.import_player_assets()
		self.status = 'Move'

		# damage timer
		self.isDamage = False
		self.hurt_time = None
		self.invulnerability_duration = 500

		self.hp = 3
		self.god_mode = False
		self.big_flag = False
		
		self.show_item = [False, False, False, False]
		self.alphabet_count = 0

		self.distance = 0
		self.distance_timer = pygame.time.get_ticks()

		# high score
		try:
			self.highestScore = (int)(self.getHeightScore())
		except:
			self.highestScore = 0
	
	def import_player_assets(self):
		character_path = '../image/player/'
		self.animations = {'Idle': [], 'Move': [], 'Die': []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path) 

	def input(self):
		if(not self.inputFlag):
			return
		mouse = pygame.mouse.get_pressed()

		# movement input
		if mouse[0] and self.rect.y > 45:
			self.direction.y = -1
		elif self.rect.y < 370:
			self.direction.y = 1
		else:
			self.direction.y = 0

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.isDamage:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.isDamage = False

	def god_moding(self):
		if self.god_mode:
			if pygame.time.get_ticks() - self.god_time >= 5000:
				self.god_mode = False
		else:
			self.god_time = pygame.time.get_ticks()

	def big_moding(self):
		if not self.inputFlag:
			if pygame.time.get_ticks() - self.big_time >= 5000:
				self.small_mode()
		else:
			self.big_time = pygame.time.get_ticks()
 

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.image = pygame.transform.scale(self.image, (self.scale[0], self.scale[1]))
		self.rect = self.image.get_rect(center = self.get_hitbox().center)

		# flicker
		if self.isDamage:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def big_mode(self, origin_speed):
		self.scale = (650, 650)
		self.inputFlag = False
		self.god_mode = True
		self.big_flag = True
		self.direction.y = 0
		self.hitbox_origin = self.hitbox 
		self.hitbox = self.rect.inflate(0,200)
		self.origin_speed = origin_speed

	def small_mode(self):
		self.scale = (200, 200)
		self.inputFlag = True
		self.god_mode = False
		self.big_flag = False
		self.hitbox = self.hitbox_origin
		self.origin_speed()

	def big_update(self):
		self.rect.center = (self.rect.center[0], 250)
		self.hitbox.center = self.rect.center

	def add_score(self):
		if(pygame.time.get_ticks() - self.distance_timer >= 1000):
			self.distance_timer = pygame.time.get_ticks()

			self.distance += 1 
			if self.big_flag:
				self.distance += 2

			if self.highestScore < self.distance:
				self.highestScore = self.distance
			with open("highest score.txt", "w") as f:
				f.write(str(self.highestScore))

	def getHeightScore(self):
		with open("highest score.txt", "r") as f:
			return f.read()

	def update(self):
		self.input()
		self.cooldowns()
		self.god_moding()
		self.big_moding()
		self.animate()
		self.move(5)
		# score
		self.add_score()
		if not self.inputFlag:
			self.big_update()
