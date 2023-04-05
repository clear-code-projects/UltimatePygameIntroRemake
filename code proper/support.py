import pygame, os

def import_folder(path):
	frames = []
	for folder_path, _, image_data in os.walk(path):
		for file_name in sorted(image_data, key = lambda path: int(path.split('.')[0])):
			full_path = os.path.join(folder_path, file_name)
			frames.append(pygame.image.load(full_path).convert_alpha())
	return frames