import pygame

class start():
    def __init__(self, screen):
        self.display_surface = pygame.display.get_surface()

        # Load Background
        self.floor_surf = pygame.image.load('../image/bg/bg.png').convert()
        self.bg_width = self.floor_surf.get_width()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        self.myscreen = screen

        self.display_surface.blit()


        