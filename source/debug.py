import pygame
pygame.init()
font = pygame.font.Font(None,30)

def debug(info,y = 10, x = 10, w = 10, h = 10):
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'Black')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	debug_rect.width = w
	debug_rect.height = h
	pygame.draw.rect(display_surface,(255,0,0,0),debug_rect,2)
	display_surface.blit(debug_surf,debug_rect)
