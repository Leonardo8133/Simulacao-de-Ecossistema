import pygame
from pygame.locals import *
import sys
import ha
pygame.init()

DISPLAYSURF = pygame.display.set_mode((640, 480), DOUBLEBUF)    #set the display mode, window title and FPS clock
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

map_data = [
[1, 1, 1, 1, 1],
[1, 1, 0, 1, 1]
]               #the data for the map expressed as [row[tile]].

wall = pygame.image.load('wall.png').convert_alpha()  #load images
grass = pygame.image.load('grass.png').convert_alpha()
tileset = pygame.image.load('tileset.png').convert_alpha()

TILEWIDTH = 64  #holds the tile width and height
TILEHEIGHT = 64
TILEHEIGHT_HALF = TILEHEIGHT /2
TILEWIDTH_HALF = TILEWIDTH /2
offsetx=100
offsety=200


for row_nb, row in enumerate(map_data):
	for col_nb, tile in enumerate(row):
		if tile == 1:
        	tileImage = wall
        	else:
			tileImage = grass
		cart_y = row_nb * TILEWIDTH_HALF
		cart_x = col_nb * TILEHEIGHT_HALF 
		iso_x = (cart_x)
		iso_y = (cart_y)
		DISPLAYSURF.blit(tileImage, (cart_x + offsetx, cart_y + offsety)) #display the actual tile

		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
					if event.type == KEYUP:
						if event.key == K_ESCAPE:
							pygame.quit()
							sys.exit()
							pygame.display.flip()
							FPSCLOCK.tick(30)