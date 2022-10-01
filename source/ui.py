from mimetypes import init
import pygame

from settings import UI_FONT

class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.heart_image = pygame.image.load('../image/ui/heart.png').convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (int(self.heart_image.get_width() * 5), (int(self.heart_image.get_height() * 5))))
        self.empty_heart_image = pygame.image.load('../image/ui/empty_heart.png').convert_alpha()
        self.empty_heart_image = pygame.transform.scale(self.empty_heart_image, (int(self.empty_heart_image.get_width() * 5), (int(self.empty_heart_image.get_height() * 5))))
        self.offset = (20, 0)
        self.player = player

        self.font = pygame.font.Font(UI_FONT, 70)
        self.m_text = self.font.render(f'{self.player.distance}m', True, (0,0,0))

        # Alphabet load
        self.alphabets = []
        self.empty_alphabets = []
        self.import_alphabet()
    
    def import_alphabet(self):
        alphabets_string = ("i", "t", "e", "m")

        for i in range(0, 4):
            full_path = f'../image/ui/{alphabets_string[i]}_alphabet.png'
            e_full_path = f'../image/ui/e{alphabets_string[i]}_alphabet.png'
            self.alphabets.append(pygame.image.load(full_path).convert_alpha())
            self.empty_alphabets.append(pygame.image.load(e_full_path).convert_alpha())

            width = self.alphabets[i].get_width()
            height = self.alphabets[i].get_height()

            self.alphabets[i] = pygame.transform.scale(self.alphabets[i], (int(width * 8), (int(height * 8))))
            self.empty_alphabets[i] = pygame.transform.scale(self.empty_alphabets[i], (int(width * 8), (int(height * 8))))

    def show_heart(self,player):
        self.current_hp = player.hp

        for i in range(0, 3):
            if self.current_hp > 0:
                self.set_image = self.heart_image
            else:
                self.set_image = self.empty_heart_image

            self.display_surface.blit(self.set_image, (self.offset[0] + (i * 90), self.offset[1]))  
            self.current_hp -= 1

    def show_itempanel(self, player):
        for i in range(0, 4):
            if player.show_item[i]:
                self.display_surface.blit(self.alphabets[i], (1080 + (i * 40), 10))
            else:
                self.display_surface.blit(self.empty_alphabets[i], (1080 + (i * 40), 10))
    
    def display(self,player):
        self.show_heart(player)
        self.show_itempanel(player)
        self.m_text = self.font.render(f'{self.player.distance}m', True, (0,0,0))
        self.display_surface.blit(self.m_text, (600, 10))
        #bg_rect = pygame.Rect(550,5,180,60)
        #pygame.draw.rect(self.display_surface,'#222222',bg_rect)
