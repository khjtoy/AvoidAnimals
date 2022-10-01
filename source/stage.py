from calendar import day_name
import random
import this
from turtle import Screen, distance
import pygame 
import math
from player import Player
from enemy import Enemy
from settings import *
from upgrade import Upgrade
from ui import UI
from arrowItem import ArrowItem
from thunder import Thunder
from alphabet import Alphabet
from debug import debug
import util

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

		# timer
		self.timer = pygame.time.get_ticks()
		self.setTime = random.randint(1, 5) * 500

		# alphabet
		self.alphabet_timer = pygame.time.get_ticks()
		self.alphabet_setTime = random.randint(2, 10) * 500
		self.alphabets = []

		# enemy
		self.enemys = []
		self.enemy_arrows = []
		self.enemyPos = [0,100,-100]

		# user interface
		self.ui = UI(self.player)
		self.upgrade = Upgrade(self.player)

		self.slow_mode = False
		self.push_arrow = False
		self.arrow_mode = False		
		
	def create_background(self):
		pass

	def damage_player(self):
		if self.player.god_mode: 
			return
		if not self.player.isDamage:
			self.player.isDamage = True
			self.player.hp -= 1
			self.player.hurt_time = pygame.time.get_ticks()

	def slow_enemy(self):
		for i in enumerate(self.enemys):
			self.enemys[i[0]].speed = 8.0

	def slowing_enemy(self):
		if self.slow_mode:
			if pygame.time.get_ticks() - self.slow_time >= 5000:
				for i in enumerate(self.enemys):
					self.enemys[i[0]].speed = 10
				self.slow_mode = False
		else:
			self.slow_time = pygame.time.get_ticks()

	def spawn_enemy(self):
		if pygame.time.get_ticks() - self.timer > self.setTime:
			self.timer = pygame.time.get_ticks()
			self.spawn_speed = 500 - ((self.player.distance // 10) * 20)
			if(self.spawn_speed < 200):
				self.spawn_speed = 200
			self.setTime = random.randint(1, 5) * self.spawn_speed
			random_index = random.randint(0, 1)
			if random_index == 0 or self.player.distance < 25:
				randomPos = random.randint(200, 480)
				self.enemy = Enemy("pig",(WIDTH  + 300, randomPos), [self.visible_sprites], self.enemys, self.player)
			else:
				randomPos = random.randint(250, 500)
				self.enemy = Enemy("chicken",(WIDTH  + 300, randomPos), [self.visible_sprites], self.enemys, self.player)

			if self.arrow_mode:
				self.arrow = ArrowItem(1200, (randomPos) - 10)
				self.enemy_arrows.append(self.arrow)
			self.enemys.append(self.enemy)

	def spawn_alphabet(self):
		if pygame.time.get_ticks() - self.alphabet_timer > self.alphabet_setTime:
			self.alphabet_timer = pygame.time.get_ticks()
			self.alphabet_setTime = random.randint(2, 10) * 500
			self.alphabet_index  = random.randint(0, 3)
			randomIndex = random.randint(0, 2)
			self.alphabet = Alphabet((WIDTH  + 300, (HEIGTH / 2) - self.enemyPos[randomIndex]), self.alphabet_index, [self.visible_sprites])
			self.alphabets.append(self.alphabet)


	def spawn_arrow(self):
		for i in enumerate(self.enemy_arrows):
			self.enemy_arrows[i[0]].draw(self.display_surface)

		if len(self.enemy_arrows) > 1 and not self.push_arrow:
			self.arrow_time = pygame.time.get_ticks()
			self.push_arrow = True
		
		if self.push_arrow and pygame.time.get_ticks() - self.arrow_time >= 100:
			if len(self.enemy_arrows):
				del self.enemy_arrows[0]
				self.push_arrow = False

	def arrowing_mode(self):
		if self.arrow_mode:
			self.spawn_arrow()
			if pygame.time.get_ticks() - self.arrowing_time >= 15000:
				self.arrow_mode = False
				self.enemy_arrows.clear()
		else:
			self.arrowing_time = pygame.time.get_ticks()

	def thunder_mode(self):
		for i in enumerate(self.enemys):
			self.thunder = Thunder((self.enemys[i[0]].rect.x - 50, self.enemys[i[0]].rect.y - 50), [self.visible_sprites])
			self.enemys[i[0]].kill()

		self.enemys.clear()
			
	def OncollisionEnterEnemys(self):
		for i in enumerate(self.enemys):
			collide = pygame.Rect.colliderect(self.player.hitbox, self.enemys[i[0]].rect)
			# collision with the player
			if collide:
				self.damage_player()
				self.enemys[i[0]].kill()
				del self.enemys[i[0]]
				

	def OncollisionEnterAlphabets(self):
		for i in enumerate(self.alphabets):
			collide = pygame.Rect.colliderect(self.player.hitbox, self.alphabets[i[0]].rect)
			# collision with the player
			if collide:
				if not self.player.show_item[self.alphabets[i[0]].index]:
					self.player.show_item[self.alphabets[i[0]].index] = True
					self.player.alphabet_count += 1
				self.alphabets[i[0]].kill()
				del self.alphabets[i[0]]

				if(self.player.alphabet_count >= 4):
					self.item_panel()
					self.player.alphabet_count = 0
					self.player.show_item = [False, False, False, False]
		
	def item_panel(self):	
		self.game_paused = not self.game_paused
		self.fade = pygame.Surface((WIDTH, HEIGTH))
		self.fade.fill((0,0,0))
		self.fade.set_alpha(150)
		self.display_surface.blit(self.fade, (0, 0))
		self.upgrade.display()

	def play_item(self):
		self.game_paused = False
		if self.upgrade.useIndex == 0:
			if self.player.hp < 3:
				self.player.hp += 1
		elif self.upgrade.useIndex == 1:
			self.arrow_mode = True
		elif self.upgrade.useIndex == 2:
			self.player.big_mode()
			self.visible_sprites.bg_speed = 20
		elif self.upgrade.useIndex == 3:
			self.thunder_mode()
		elif self.upgrade.useIndex == 4:
			self.player.god_mode = True
		elif self.upgrade.useIndex == 5:
			self.slow_mode = True

		self.upgrade.useItem = False

	def run(self):
		self.visible_sprites.custom_draw(self.player, self.game_paused)
		self.ui.display(self.player)

		if self.slow_mode:
			self.slow_enemy()
		
		if self.game_paused:
			self.upgrade.drawPanel()
			if self.upgrade.useItem:
				self.play_item()
		else:
			self.spawn_enemy()
			self.spawn_alphabet()
			self.visible_sprites.update()
			self.OncollisionEnterEnemys()
			self.OncollisionEnterAlphabets()
			self.slowing_enemy()
			self.arrowing_mode()
		
			#self.visible_sprites.enemy_update(self.player)

			# debug
			ohit = self.player.get_hitbox()
			debug('Player', ohit.top,ohit.left,ohit.width,ohit.height)
		

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

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)
