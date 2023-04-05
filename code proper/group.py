import pygame 

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

	def custom_draw(self):
		for sprite in [sprite for sprite in self.sprites() if hasattr(sprite, 'draw_below')]:
			self.display_surface.blit(sprite.image, sprite.rect)

		for sprite in [sprite for sprite in self.sprites() if not hasattr(sprite, 'draw_below')]:
			self.display_surface.blit(sprite.image, sprite.rect)