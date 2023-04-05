import pygame 

class Player(pygame.sprite.Sprite):
	def __init__(self, groups, start_pos, create_laser):
		
		# setup 
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/player.png').convert_alpha()
		self.rect = pygame.FRect(self.image.get_rect())
		self.rect.center = start_pos

		# movement
		self.direction = pygame.math.Vector2()
		self.speed = 400

		# laser 
		self.create_laser = create_laser
		self.laser_ready = True
		self.laser_cooldown = 600
		self.laser_shoot_time = None

	def input(self):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_RIGHT]: 
			self.direction.x = 1
		elif keys[pygame.K_LEFT]: 
			self.direction.x = -1
		else: 
			self.direction.x = 0

		if keys[pygame.K_DOWN]: 
			self.direction.y = 1
		elif keys[pygame.K_UP]: 
			self.direction.y = -1
		else: 
			self.direction.y = 0

		if keys[pygame.K_SPACE] and self.laser_ready:
			self.create_laser(self.rect.midtop, pygame.math.Vector2(0,-1))
			self.laser_ready = False
			self.laser_shoot_time = pygame.time.get_ticks()

	def laser_timer(self):
		if not self.laser_ready:
			if pygame.time.get_ticks() - self.laser_shoot_time >= self.laser_cooldown:
				self.laser_ready = True

	def move(self,dt):
		self.rect.center += self.direction * self.speed * dt
		
		# clamps to keep player on screen
		self.rect.centerx = max(self.rect.width / 2,min(1280 - self.rect.width / 2, self.rect.centerx))
		self.rect.centery = max(self.rect.height / 2,min(720 - self.rect.height / 2, self.rect.centery))

	def update(self,dt):
		self.input()
		self.move(dt)

		self.laser_timer()
