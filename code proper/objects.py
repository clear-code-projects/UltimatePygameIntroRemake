import pygame 
from settings import *
from random import randint, uniform

class Laser(pygame.sprite.Sprite):
	def __init__(self, groups, pos, direction):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/laser.png').convert_alpha()
		self.rect = pygame.FRect(self.image.get_rect())
		self.rect.midbottom = pos
		self.direction = direction
		self.speed = 600
		self.mask = pygame.mask.from_surface(self.image)

	def move(self, dt):
		self.rect.center += self.direction * self.speed * dt

	def update(self,dt):
		self.move(dt)

		if self.rect.top < -100:
			self.kill()

class Meteor(pygame.sprite.Sprite):
	def __init__(self, groups, surface):
		super().__init__(groups)
		
		# image setup 
		self.original = surface
		if randint(0,1):
			self.original = pygame.transform.scale2x(self.original)
		self.image = self.original
		self.rotation = 0
		
		# position
		x, y = randint(-100, SCREEN_SIZE[0] -100), randint(-300,-100)
		self.rect = pygame.FRect(self.image.get_rect(center = (x,y)))
		
		self.direction = pygame.math.Vector2(uniform(0.1, 0.4),1)
		self.speed = randint(300,600)
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, dt):

		# move
		self.rect.center += self.direction * self.speed * dt

		# rotate
		self.rotation += 30 * dt
		self.image = pygame.transform.rotate(self.original, self.rotation)
		self.mask = pygame.mask.from_surface(self.image)

		# destory
		if self.rect.bottom > SCREEN_SIZE[1] + 500:
			self.kill()