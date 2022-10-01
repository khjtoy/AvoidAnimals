import pygame

from entity import Entity

class Button:
    def __init__(self, x, y, image, scale, originClick):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.originClock = originClick

    def draw(self, surface):
        action = False

        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked condition
        if self.originClock:
            self.clicked = False
        else:
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

        if self.originClock and pygame.mouse.get_pressed()[0] == 0:
            self.originClock = False
        
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
        