from cmath import rect
import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
	def __init__(self,groups):
		super().__init__(groups)
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = pygame.math.Vector2()
		self.hitbox_offset = (0,0)
	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		#self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		#self.collision('vertical')

		self.rect.center = self.hitbox.center

	def bezierMove(self, speed):
		self.path_positions = [(self.rect.x,self.rect.y), (self.rect.x - 100, self.rect.y - 200), (self.rect.x - 200, self.rect.y - 200), (self.rect.x - 300, self.rect.y)]
		t = 0

		p0 = self.path_positions[0]
		p1 = self.path_positions[1]
		p2 = self.path_positions[2]
		p3 = self.path_positions[3]

		while t < 1:
			t += speed

			p0_x = pow((1-t), 3) * p0[0]
			p0_y = pow((1-t), 3) * p0[1]

			p1_x = 3 * pow((1-t), 2) * t * p1[0]
			p1_y = 3 * pow((1-t), 2) * t * p1[1]

			p2_x = 3 * (1-t) * pow(t, 2) * p2[0]
			p2_y = 3 * (1-t) * pow(t, 2) * p2[1]

			p3_x = pow(t,3) * p3[0]
			p3_y = pow(t,3) * p3[1]

			formular = ((p0_x + p1_x + p2_x + p3_x), (p0_y + p3_y + p2_y + p1_y))
			x, y = formular

			self.hitbox.x = round(x)
			self.hitbox.y = round(y)

			self.rect.center = self.hitbox.center



	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: 
			return 255
		else: 
			return 0