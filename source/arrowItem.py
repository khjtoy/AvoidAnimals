from email.mime import image
from turtle import width
import pygame;

class ArrowItem:
    def __init__(self, x, y):
        self.arrow = pygame.image.load('../image/ui/arrow.png').convert_alpha()
        width = self.arrow.get_width()
        heigth = self.arrow.get_height()
        self.arrow = pygame.transform.scale(self.arrow, (int(width * 5), (int(heigth * 5))))
        self.rect = self.arrow.get_rect()
        self.rect.topleft = (x, y)
        
        # timer
        self.timer = pygame.time.get_ticks()

    def draw(self, surface):
            surface.blit(self.arrow, (self.rect.x, self.rect.y))