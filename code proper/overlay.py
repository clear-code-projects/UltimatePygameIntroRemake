import pygame 
from settings import * 

class Overlay:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(None, 40)
		self.icon_surf = pygame.image.load('../graphics/icon.png').convert_alpha()


	def display_score(self, time_passed):
		
		# text data
		text_surf = self.font.render(str(time_passed // 1000), False, 'white')
		text_rect = text_surf.get_rect(center = (SCREEN_SIZE[0] / 2, 100))

		# score display
		self.display_surface.blit(text_surf, text_rect)

		# frame
		pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(32,32),4,5)

	def display_lifes(self, num_lifes):
		for life in range(num_lifes):
			x = 20 + life * (self.icon_surf.get_width() + 4) 
			y = SCREEN_SIZE[1] - 20
			icon_rect = self.icon_surf.get_rect(bottomleft = (x,y))
			self.display_surface.blit(self.icon_surf, icon_rect)