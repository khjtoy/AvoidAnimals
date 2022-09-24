from calendar import day_name
import random
from turtle import Screen
import pygame 
import math
from player import Player
from enemy import Enemy
from settings import *
from upgrade import Upgrade
from debug import debug

class stage():
	def __init__(self, screen):
		# get the display surface 
		self.display_surface = pygame.display.get_surface() # 아직까지는 미사용
		self.game_paused = False
		
		# sprite group setup
		self.visible_sprites = YSortCameraGroup(screen)

		self.attackable_entity = list()
        # player
		self.player = Player((WIDTH / 5, HEIGTH / 4), [self.visible_sprites])

		# user interface
		self.upgrade = Upgrade(self.player)


		# 1 Enemy Stage 클래스 에서 생성
		# 2 생성된 에너미를 리스트 관리 - 삭제 리스트에서 빼기
		# 3 플레이어 이미지 교체
		
		
	def create_background(self):
		pass

	def damage_player(self):
		if not self.player.isDamage:
			self.player.isDamage = True
			self.player.hurt_time = pygame.time.get_ticks()

	def item_panel(self):
		self.game_paused = not self.game_paused
		self.fade = pygame.Surface((WIDTH, HEIGTH))
		self.fade.fill((0,0,0))
		self.fade.set_alpha(150)
		self.display_surface.blit(self.fade, (0, 0))
		self.upgrade.display()

	def run(self):
		self.visible_sprites.custom_draw(self.player, self.game_paused)
		
		if self.game_paused:
			self.upgrade.drawPanel()
		else:
			self.visible_sprites.spawn_enemy(self.damage_player)
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)

			# debug
			debug('Player', self.player.hitbox.top,self.player.hitbox.left,self.player.hitbox.width,self.player.hitbox.height)
		

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

		# timer
		self.timer = pygame.time.get_ticks()
		self.setTime = random.randint(1, 5) * 500

		# random pos
		self.enemyPos = [0,100,-100]
		
		self.bg_speed = 5

	def scroll_background(self):
		# draw scroll background
		for i in range(0, self.tiles):
			self.myscreen.blit(self.floor_surf, (i * self.bg_width + self.scroll, 0))

		# scroll background
		self.scroll -= self.bg_speed

		# reset scroll
		if abs(self.scroll) > self.bg_width:
			self.scroll = 0

	def custom_draw(self, player, isPaused):
		# drawing the floor

		if not isPaused:
			self.scroll_background()
		#floor_offset_pos = self.floor_rect.topleft - self.offset
		#self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft
			self.display_surface.blit(sprite.image,offset_pos)
			
	def spawn_enemy(self, damage_player):
		if pygame.time.get_ticks() - self.timer > self.setTime:
			self.timer = pygame.time.get_ticks()
			self.setTime = random.randint(1, 5) * 500
			self.randomIndex = random.randint(0, 2)
			self.enemy = Enemy("pig",(WIDTH  + 300, (HEIGTH / 2) - self.enemyPos[self.randomIndex]), [self], damage_player)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)
