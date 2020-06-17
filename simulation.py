# from multiprocessing import freeze_support
# freeze_support()
from __future__ import print_function
import pygame 
import classes as cl
import generate as gn
import key as ky
import os
import neat
import pickle as pk
from copy import copy
from game_config import *



#import data_visu as dt



def run(config_file):
	pass
	


def main(genomes=False, config=False):
	run=True
	pygame.init()
	SCALE = 1
	SCREENSIZE = (1280, 600)
	SIZE = (128, 128)
	MAP_DATA, OBJ_DATA, NEW_DATA, PATH, seed = gn.generate_terrain(SIZE, (4, 4), 5)
	# dt.visualizator(NEW_DATA)
	# \/ Neat Training
	#game = cl.Game(SCREENSIZE, SCALE, MAP_DATA, OBJ_DATA, NEW_DATA, PATH, seed, genomes, config)

	game = cl.Game(SCREENSIZE, SCALE, MAP_DATA, OBJ_DATA, NEW_DATA, PATH, seed)
	game.run=True
	game.fastmode=G_FASTMODE
	
	tick = G_SPEED
	if game.fastmode:
		tick=3000
	while game.run:
		ky.k_event(game)
		
		game.draw()
		game.tick+=1
		pygame.display.update()
		game.FPSCLOCK.tick(tick)


def reset_run(genomes, config):
	main(genomes, config)

def load_neat():
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config.txt')
	run(config_path)

if __name__=="__main__":
	main()		
	#load_neat()
