import random
import pygame;
from settings import *
import button

class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.basic_pos = (WIDTH / 10, (HEIGTH / 6) + 30)
        self.panels = [0 for i in range(3)]
        self.indexs = [0 for i in range(3)]
        #self.clicked = False

        self.item_names = ("recoverIcon", "placeIcon", "pupspeed", "lightning", "InvincibleIcon", "adownspeed")
        self.text1 = ("        HP를 +1", "    15초동안 적의", "  자이언트가 되어", "화면에 있는 적에게", "    5초동안 적의", "    5초동안 적의")
        self.text2 = ("     회복합니다.", "위치를 미리 압니다.", "5초동안 돌진합니다.", "  번개를 내립니다.", "충돌을 무력화한다.", "속도가 느려집니다.")
        self.path = "../image/ui/"

        self.useItem = False
        self.useIndex = 0

    def display(self):
        self.image = pygame.image.load('../image/ui/panel.png').convert_alpha()
        self.font = pygame.font.Font(UI_FONT, 32)
        self.title_font = pygame.font.Font(UI_FONT, 100)
        self.title_text = self.title_font.render("아이템 선택!!", True, (0,0,255))
        if pygame.mouse.get_pressed()[0] == 1:
            self.originClick = True
        else:
            self.originClick = False
        for i in range(0, 3):
            self.panels[i] = button.Button(self.basic_pos[0] + (i * 350), self.basic_pos[1], self.image, 3, self.originClick)
            self.indexs[i] = random.randint(0, 5)
            self.rect = self.image.get_rect()

    def drawPanel(self):
        self.display_surface.blit(self.title_text, (360, 40))
        for i in range(0, 3):
            self.rect.topleft = (210 + (350 * i), 210)
            self.item_image = pygame.image.load(self.path + self.item_names[self.indexs[i]] + ".png").convert_alpha()
            width = self.item_image.get_width()
            height = self.item_image.get_height()
            self.item_image = pygame.transform.scale(self.item_image, (int(width * 8), (int(height * 8))))
            self.pos_text1 = self.font.render(self.text1[self.indexs[i]], True, (255,255,255))
            self.pos_text2 = self.font.render(self.text2[self.indexs[i]], True, (255,255,255))

            self.isClicked = self.panels[i].draw(self.display_surface)
            self.display_surface.blit(self.item_image, (self.rect.x, self.rect.y))
            self.display_surface.blit(self.pos_text1, (140 + (350 * i), 380))
            self.display_surface.blit(self.pos_text2, (140 + (350 * i),420))

            if self.isClicked:
                self.useIndex = self.indexs[i]
                self.useItem = True

