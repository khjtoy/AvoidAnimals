from turtle import Screen
import pygame 
import math
from player import Player
from settings import *

class stage():
	def __init__(self, screen):
		# get the display surface 
		self.display_surface = pygame.display.get_surface() # 아직까지는 미사용
		self.game_paused = False
		
		# sprite group setup
		self.visible_sprites = YSortCameraGroup(screen)
		
        # player
		self.player = Player((0,0), [self.visible_sprites])
		
	def create_background(self):
		pass

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		#self.visible_sprites.scroll_background()
		

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self, screen):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# Load Background
		self.floor_surf = pygame.image.load('../image/bg/bg.png').convert()
		self.bg_width = self.floor_surf.get_width()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
		self.myscreen = screen

		# define game variables
		self.scroll = 0
		self.tiles = math.ceil(WIDTH / self.bg_width) + 1

	def scroll_background(self):
		# draw scroll background
		for i in range(0, self.tiles):
			self.myscreen.blit(self.floor_surf, (i * self.bg_width + self.scroll, 0))

		# scroll background
		self.scroll -= 5

		# reset scroll
		if abs(self.scroll) > self.bg_width:
			self.scroll = 0

	def custom_draw(self,player):

		# getting the offset 
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)

	#def enemy_update(self,player):
	#	enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
	#	for enemy in enemy_sprites:
	#		enemy.enemy_update(player)
