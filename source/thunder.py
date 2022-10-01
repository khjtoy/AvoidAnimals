from email.mime import image
import pygame
from entity import Entity

from support import import_folder

class Thunder(Entity):
    def __init__(self, pos, groups):

        super().__init__(groups)

        self.image = pygame.image.load('../image/particle/thunder/0.png').convert_alpha()

        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * 1), (int(height * 1))))

        self.rect = self.image.get_rect(topleft = pos)

        self.status = 'thunder'
        self.animations_speed = 0.15
        self.import_assets()

    def import_assets(self):
        self.animations = {'thunder': []}
        charcter_path = '../image/particle/'

        for animation in self.animations.keys():
            full_path = charcter_path + animation
            self.animations[animation] = import_folder(full_path)

        print("Deb")

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.kill()
            return

        # set the image
        self.image = animation[int(self.frame_index)]
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (int(width * 1), (int(height * 1))))
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        self.animate()

