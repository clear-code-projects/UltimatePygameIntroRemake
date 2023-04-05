import pygame, sys
from random import randint, uniform

def get_input(vector):
	keys = pygame.key.get_pressed()
	vector.update((0,0))
	if keys[pygame.K_RIGHT]:
		vector.x = 1
	elif keys[pygame.K_LEFT]:
		vector.x = -1
	if keys[pygame.K_DOWN]:
		vector.y = 1
	elif keys[pygame.K_UP]:
		vector.y = -1
	return vector.normalize() if vector.magnitude() != 0 else pygame.math.Vector2()

def display_score(time_passed):
		# text data
		text_surf = font.render(str(time_passed // 1000), False, 'white')
		text_rect = text_surf.get_rect(center = (SCREEN_SIZE[0] / 2, 100))

		# score display
		display_surface.blit(text_surf, text_rect)

		# frame
		pygame.draw.rect(display_surface, 'white', text_rect.inflate(32,32),4,5)

def display_lifes(num_lifes):
	for life in range(num_lifes):
		x = 20 + life * (icon_surf.get_width() + 4) 
		y = SCREEN_SIZE[1] - 20
		icon_rect = icon_surf.get_rect(bottomleft = (x,y))
		display_surface.blit(icon_surf, icon_rect)

# init
pygame.init()
SCREEN_SIZE = (1280,720)
display_surface = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Spaceship')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

# bg stars
star_bg_surf = pygame.image.load('../graphics/star_bg.png').convert_alpha()

# spaceship 
player_surf = pygame.image.load('../graphics/player.png').convert_alpha()
player_rect = pygame.FRect(player_surf.get_rect(center = (640,360)))
player_direction = pygame.math.Vector2()
player_speed = 400

# laser 
laser_surf = pygame.image.load('../graphics/laser.png').convert_alpha()
laser_speed = 600
laser_data = []

# meteor 
meteor_surf = pygame.image.load('../graphics/meteor.png').convert_alpha()
meteor_data = []
meteor_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteor_timer, 150)

# life system
icon_surf = pygame.image.load('../graphics/icon.png').convert_alpha()
lifes = 3

# score system
score = 0
start_time = 0
game_over = False

# title
broken_surf = pygame.image.load('../graphics/broken.png').convert_alpha()
broken_rect = broken_surf.get_rect(center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2 - 100))
restart_surf = font.render('Restart', True, 'White')
restart_surf_dark = font.render('Restart', True, '#3a2e3f')
restart_rect = restart_surf.get_rect(center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] - 100))

# audio 
game_music = pygame.mixer.Sound('../audio/game_music.wav')
title_music = pygame.mixer.Sound('../audio/title_music.wav')
laser_sound = pygame.mixer.Sound('../audio/laser.wav')
explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
damage_sound = pygame.mixer.Sound('../audio/damage.ogg')

game_music.play()

while True:
	# get delta time 
	dt = clock.tick() / 1000

	# event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if not game_over:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				laser_frect = pygame.FRect(laser_surf.get_rect(midbottom = player_rect.center - pygame.math.Vector2(0,30)))
				laser_data.append({'rect':laser_frect, 'dokill': False})
				laser_sound.play()
			if event.type == meteor_timer:
				x,y  = randint(-100, SCREEN_SIZE[0] -100), randint(-300,-100)
				meteor_frect = pygame.FRect(meteor_surf.get_rect(center = (x, y)))
				meteor_direction = pygame.math.Vector2(uniform(0.1,0.4),1)
				meteor_speed = randint(300,600)
				meteor_data.append({'rect': meteor_frect, 'direction': meteor_direction, 'speed': meteor_speed, 'dokill': False})

	# bg color 
	display_surface.fill('#3a2e3f')

	# title screen
	if game_over:
		display_surface.blit(broken_surf,broken_rect)	
			
		# text 
		text_surf = font.render(f'Your score: {score}', True, 'White')
		text_rect = text_surf.get_rect(center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2 + 50))
		display_surface.blit(text_surf, text_rect)

		# button 
		if restart_rect.collidepoint(pygame.mouse.get_pos()):
			pygame.draw.rect(display_surface, 'white', restart_rect.inflate(30,30),0,3)
			display_surface.blit(restart_surf_dark, restart_rect)

			if pygame.mouse.get_pressed()[0]:
				game_over = False
				lifes = 3
				start_time = pygame.time.get_ticks()

				title_music.stop() 
				game_music.play()
		else:
			display_surface.blit(restart_surf, restart_rect)

		pygame.draw.rect(display_surface, 'white', restart_rect.inflate(30,30), 5,3)
	
	# game logic
	else:
		display_surface.blit(star_bg_surf,(0,0))

		score = pygame.time.get_ticks() - start_time
		display_score(score)

		# display laser 
		if laser_data:
			for laser_dict in laser_data:
				laser_dict['rect'].y -= laser_speed * dt
				display_surface.blit(laser_surf, laser_dict['rect'])
			laser_data = [laser_dict for laser_dict in laser_data if laser_dict['rect'].y > -100]

		# display meteor 
		if meteor_data:
			for meteor_dict in meteor_data:
				meteor_dict['rect'].center += meteor_dict['direction'] * meteor_dict['speed'] * dt
				display_surface.blit(meteor_surf, meteor_dict['rect'])
			meteor_data = [meteor_dict for meteor_dict in meteor_data if meteor_dict['rect'].y < 800]

		# display spaceship
		player_direction = get_input(player_direction)
		player_rect.center += player_direction * player_speed * dt
		display_surface.blit(player_surf, player_rect)

		# collision
		if meteor_data:
			for meteor_dict in meteor_data:
				
				# player -> meteor  
				if player_rect.colliderect(meteor_dict['rect']):
					meteor_dict['dokill'] = True
					lifes -= 1
					damage_sound.play()

					if lifes <= 0:
						game_over = True
						meteor_data = []
						laser_data = []
						game_music.stop()
						title_music.play() 

				# laser -> meteor 
				if laser_data:
					for laser_dict in laser_data:
						if meteor_dict['rect'].colliderect(laser_dict['rect']):
							meteor_dict['dokill'] = True
							laser_dict['dokill'] = True
							explosion_sound.play()
			
			meteor_data = [meteor_dict for meteor_dict in meteor_data if not meteor_dict['dokill']]
			laser_data = [laser_dict for laser_dict in laser_data if not laser_dict['dokill']]

		# display lifes 
		display_lifes(lifes)

	# update frame 
	pygame.display.update()