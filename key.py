import pygame
from pygame.locals import *
import sys


from hud import HUD as HUD
from entities import Ent


'''<Event(4-MouseMotion {'pos': (994, 60), 'rel': (43, 9), 'buttons': (0, 0, 0), 'window': None})>'''

def k_event(game):
	for event in pygame.event.get():
			if event.type == QUIT:				
				pygame.quit()
				sys.exit()

			
			if event.type == pygame.MOUSEBUTTONDOWN:
				game.hud.mouse_event(event.type, event.button, event.pos, game)

			if event.type == KEYDOWN:
				game.hud.key_event(event.type, event.key)
				if event.key == K_ESCAPE:
					
					pygame.quit()
					sys.exit()



				if event.key == 45 and game.scale>0.25:
					# #print(game.cam)
					# game.change_scale(-0.25)
					pass
				if event.key == 61:
					# #print(game.cam)
					# game.change_scale(0.25)
					pass
				if event.key == K_m:
					reset_run()
				if event.key == K_n:
					for x in game.ent_list:
						print(x)
				if event.key == K_UP: #eixo x=0 eixo y=1
					game.addcord(1,-4)					
				if event.key == K_DOWN:
					game.addcord(1,4)					
				if event.key == K_RIGHT:
					game.addcord(0,4)
				if event.key == K_LEFT:
					game.addcord(0,-4)
				if event.key == K_q:					
					Ent.add=2
				if event.key == K_SPACE:
					pass
				if event.key == K_c:
					pass
				if event.key == K_z:					
					game.ent_list=[]
				if event.key == K_x:
					game.config.fitness_threshold-=50
					print(game.config.fitness_threshold)
				if event.key == K_w:
					game.config.fitness_threshold+=50
					print(game.config.fitness_threshold)
				if event.key == K_r:
					print(HUD.wdata)
				if event.key == K_y:
					pass