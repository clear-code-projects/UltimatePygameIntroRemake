import pygame
from settings import *
from random import randint
from support import import_folder

class Explosion(pygame.sprite.Sprite):
	def __init__(self, groups, frames, pos):
		super().__init__(groups)

		self.path = '..\graphics\explosion'
		self.frames = frames
		self.frame_index = 0

		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def update(self, dt):
		self.frame_index += 40 * dt
		if self.frame_index < len(self.frames):
			self.image = self.frames[int(self.frame_index)]
		else:
			self.kill()

class AnimatedStar(pygame.sprite.Sprite):
	def __init__(self, groups, frames):
		super().__init__(groups)
		self.frames = frames
		self.frame_index = randint(0,len(self.frames) - 1)

		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = (randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1])))

		self.draw_below = True

	def update(self, dt):
		self.frame_index += 20 * dt
		self.image = self.frames[int(self.frame_index) % len(self.frames)]