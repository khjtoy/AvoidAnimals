from turtle import distance
import pygame 
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):
    def __init__(self,pos,groups):

        super().__init__(groups)
        self.sprite_type = 'enemy'

        self.image = pygame.image.load('../image/test_enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])
        self.direction.x = -1

        # graphics setup
        self.import_enemy_assets()
        self.status = 'Move'

    def import_enemy_assets(self):
        charcter_path = '../image/enemy/'
        self.animations = {'Move': []}

        for animation in self.animations.keys():
            full_path = charcter_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (70, 70 - 13))
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def OncollisionEnter(self, player):
        collide = pygame.Rect.colliderect(player.rect, self.rect)

        # collision with the player
        if collide:
            self.kill()

    def update(self):
        self.animate()
        self.move(10)


    def enemy_update(self, player):
        self.OncollisionEnter(player)