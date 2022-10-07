from turtle import distance
import pygame
from settings import *
from entity import Entity
from support import import_folder
from debug import debug, debug_r

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,enemys, player):

        super().__init__(groups)
        self.sprite_type = 'enemy'

        self.image = pygame.image.load('../image/test_enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(40,40)
        self.hitbox_offset = (10, 0)
        self.direction.x = -1
        self.monster_name = monster_name
        self.player = player

        self.orginSpeed = 10 + ((self.player.distance / 10) * (5 / 10))
        if int(self.orginSpeed) > 15:
            self.orginSpeed = 15 
        self.speed = self.orginSpeed

        # graphics setup
        self.import_enemy_assets(self.monster_name)
        self.status = 'Move'

        # timer
        self.timer = pygame.time.get_ticks()
        self.enemyList = enemys 

        # sound
        if monster_name == "pig":
            self.main_sound = pygame.mixer.Sound("../audio/pig_sound.mp3")
        elif monster_name == "chicken":
            self.main_sound = pygame.mixer.Sound("../audio/chicken_sound.mp3")
        self.main_sound.set_volume(0.5)
        self.main_sound.play()
        
            
    def import_enemy_assets(self, name):
        self.animations = {'Move': []}
        charcter_path = f'../image/enemy/{name}/'

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

    def update(self):
        self.animate()
        if self.monster_name == "pig":
            self.move(self.speed + ((self.player.distance // 10) * (5 / 10)))
        elif self.monster_name == "chicken":
            self.bezierMove(0.02)

        # debug
        #ohit = self.get_hitbox()
        #debug_r('Enemy', ohit)
        