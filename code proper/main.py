import pygame, sys 
from settings import *
from player import Player
from objects import Laser, Meteor
from animations import AnimatedStar, Explosion
from random import randint
from support import import_folder
from overlay import Overlay
from group import AllSprites
from random import choice

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode(SCREEN_SIZE)
		pygame.display.set_caption('Ultimate intro')
		self.clock = pygame.time.Clock()

		self.all_sprites = AllSprites()
		self.lasers = pygame.sprite.Group()
		self.meteors = pygame.sprite.Group()
		self.player = Player(self.all_sprites, (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] - 100), self.create_laser)
	
		# imports 
		self.star_frames = import_folder('..\graphics\star')
		self.explosion = import_folder('..\graphics\explosion')
		self.meteor_surfaces = import_folder('..\graphics\meteors')

		self.broken_surf = pygame.image.load('../graphics/broken.png').convert_alpha()
		self.broken_rect = self.broken_surf.get_rect(center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 - 100))

		# timer 
		self.meteor_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.meteor_timer, 150)
		
		# bg stars 
		for i in range(randint(50,70)):
			AnimatedStar(self.all_sprites, self.star_frames)

		# overlay
		self.overlay = Overlay()

		# score 
		self.score = 0
		self.lifes = 3
		self.start_time = 0
		self.game_over = False

		# font
		self.font = pygame.font.Font(None, 40)

		# restart button 
		self.restart_surf = self.font.render('Restart', True, TEXT_COLOR)
		self.restart_rect = self.restart_surf.get_rect(center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] - 100))
		self.restart_surf_dark = self.font.render('Restart', True, BG_COLOR)

		# music 
		self.game_music = pygame.mixer.Sound('../audio/game_music.wav')
		self.title_music = pygame.mixer.Sound('../audio/title_music.wav')
		self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
		self.damage_sound = pygame.mixer.Sound('../audio/damage.ogg')

		if not self.game_over:
			self.game_music.play()
		else:
			self.title_music.play()

	def create_laser(self, pos, direction):
		
		Laser((self.all_sprites, self.lasers), pos, direction)
		self.laser_sound.play()

	def collisions(self):
		
		# laser -> meteor
		for laser in self.lasers:
			if pygame.sprite.spritecollide(laser, self.meteors, True, pygame.sprite.collide_mask):
				Explosion(self.all_sprites, self.explosion, laser.rect.midtop)
				laser.kill()
				self.explosion_sound.play()

		# meteor -> player 
		if pygame.sprite.spritecollide(self.player, self.meteors, True, pygame.sprite.collide_mask):
			self.lifes -= 1
			self.damage_sound.play()

			if self.lifes <= 0:
				self.score = pygame.time.get_ticks() - self.start_time
				self.game_over = True
				for meteor in self.meteors:
					meteor.kill()
				self.player.rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] - 100)

				self.game_music.stop()
				self.title_music.play() 

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == self.meteor_timer and not self.game_over and pygame.time.get_ticks() > 1_500:
					Meteor((self.all_sprites, self.meteors), choice(self.meteor_surfaces))

			self.display_surface.fill(BG_COLOR)
			
			if self.game_over:
				
				self.display_surface.blit(self.broken_surf,self.broken_rect)	
				# text 
				text_surf = self.font.render(f'Your score: {self.score}', True, TEXT_COLOR)
				text_rect = text_surf.get_rect(center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 + 50))
				self.display_surface.blit(text_surf, text_rect)

				# button 
				if self.restart_rect.collidepoint(pygame.mouse.get_pos()):
					pygame.draw.rect(self.display_surface, TEXT_COLOR, self.restart_rect.inflate(30,30),0,3)
					self.display_surface.blit(self.restart_surf_dark, self.restart_rect)

					if pygame.mouse.get_pressed()[0]:
						self.game_over = False
						self.lifes = 3
						self.start_time = pygame.time.get_ticks()

						self.title_music.stop() 
						self.game_music.play()
				else:
					self.display_surface.blit(self.restart_surf, self.restart_rect)

				pygame.draw.rect(self.display_surface, TEXT_COLOR, self.restart_rect.inflate(30,30), 5,3)
			else:
				dt = self.clock.tick() / 1000

				self.score = pygame.time.get_ticks() - self.start_time
				self.overlay.display_score(self.score)

				self.all_sprites.update(dt)
				self.all_sprites.custom_draw()

				self.collisions()

				self.overlay.display_lifes(self.lifes)

			pygame.display.update()
			

game = Game()
game.run()