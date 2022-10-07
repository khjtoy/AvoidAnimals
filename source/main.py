import pygame, sys
from settings import *

from stage import stage
from upgrade import Upgrade

class Game:
    def __init__(self):
        # general setup 
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Avoid Animals')
        self.clock = pygame.time.Clock()

        self.stage = stage(self.screen, self.reset)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.stage.run()

            pygame.display.update()
            self.clock.tick(FPS)
            

    def reset(self):
        del self.stage
        self.stage = stage(self.screen, self.reset)

if __name__ == '__main__':
    game = Game()
    game.run()
