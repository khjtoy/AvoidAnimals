from email.mime import image
from turtle import width
import pygame

from entity import Entity
from settings import HITBOX_OFFSET;

class Alphabet(Entity):
    def __init__(self, pos, index, groups):
        
        super().__init__(groups)
        self.index = index
        alphabets_string = ("i", "t", "e", "m")
        full_path = f'../image/ui/{alphabets_string[self.index]}_alphabet.png'

        self.image = pygame.image.load(full_path).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * 8), (int(height * 8))))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6, -26)
        self.direction.x = -1

        self.speed = 15

    def update(self):
        self.move(self.speed)
