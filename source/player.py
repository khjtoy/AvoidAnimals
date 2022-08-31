import pygame 
from settings import *
from entity import Entity
from support import import_folder

class Player(Entity):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('../image/player/Idle/idle01.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, (200, 200))
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

		# graphics setup
		self.import_player_assets()
		self.status = 'Move'

		# damage timer
		self.isDamage = False
		self.hurt_time = None
		self.invulnerability_duration = 500
	
	def import_player_assets(self):
		character_path = '../image/player/'
		self.animations = {'Idle': [], 'Move': []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path) 

	def input(self):
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

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.image = pygame.transform.scale(self.image, (200, 200))
		self.rect = self.image.get_rect(center = self.hitbox.center)

		# flicker
		if self.isDamage:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def update(self):
		self.input()
		self.cooldowns()
		self.animate()
		self.move(5)
		print()
