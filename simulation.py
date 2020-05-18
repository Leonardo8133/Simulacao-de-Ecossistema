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



#import data_visu as dt



def run(config_file):
	# # Load configuration.
	# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
	# 					 neat.DefaultSpeciesSet, neat.DefaultStagnation,
	# 					 config_file)

	# # fl = open('bunny_neat_1.pkl', 'rb')
	# # winner = pk.load(fl)
	# # fl.close()
	# # # print('\nBest genome:\n{!s}'.format(winner))
	# # Create the population, which is the top-level object for a NEAT run.
	# #p = neat.Checkpointer.restore_checkpoint('new_run99')

	# p = neat.Population(config)
	# # winner.fitness=0
	# # for x in range(10):
	# # 	p.population[x+1].connections = copy(winner.connections)
	# # 	p.population[x+1].nodes = copy(winner.nodes)
	
	
	# p.add_reporter(neat.StdOutReporter(True))
	# stats = neat.StatisticsReporter()

	# p.add_reporter(stats)
	# pe = neat.ParallelEvaluator(4, main)
	# checkpointer = neat.Checkpointer(20, None, 'fx_run')
	
	# p.add_reporter(checkpointer)
	# winner = p.run(reset_run, 101)
	# # pe.stop()

	#   # Display the winning genome.
	# print('\nBest genome:\n{!s}'.format(winner))

	# print("Thread Finished")
	# file= open("bsf.pkl", 'wb')
	# pk.dump(winner, file)
	# file.close()
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
	game.fastmode=True
	
	tick = 60
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
