import pygame 
from settings import *
from entity import Entity

class Enemy(Entity):
    def __init__(self,pos,groups,):
        super().__init__(groups)
        self.image = pygame.image.load('../image/test_enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])
        self.direction.x = -1
    
    def update(self):
        self.move(5)