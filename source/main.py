import pygame, sys
from settings import *

from stage import stage
from upgrade import Upgrade

class Game:
    def __init__(self):
        # general setup 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        self.stage = stage(self.screen)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.stage.item_panel()
                    if event.key == pygame.K_1:
                        self.stage.player.big_mode()
                        self.stage.visible_sprites.bg_speed = 20

            self.stage.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
