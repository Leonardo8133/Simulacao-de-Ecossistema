from pygame.locals import *
import pygame
import numpy as np
import entities as en
import ha
import texts as tx
import path
from random import choice
from hud import HUD
from os import environ
from settings import Setting
from action import Action
import pickle as pk
import neat
import os



class Camera:
	'''Camera Configuration class'''

	def __init__(self, size, scale, game, cord=[10, 10]):
		self.tile_w = game.TILEWIDTH
		self.size = size
		self.cord = cord
		self.scale = scale
		self.curchunk=[0,0]		
		self.follow={'x':0, 'y':0}
		self.addcord(0, 0)		

	def addcord(self, eixo, val):
		self.cord[eixo] = self.cord[eixo]+(val/self.scale)
		self.cord[eixo] = self.check_border(eixo)
		self.x = 	   (-self.cord[0] * self.tile_w * self.scale + self.cord[1] * self.tile_w * self.scale)/2 #- self.follow['x']
		self.y = 	   (-self.cord[1] * (self.tile_w/2) * self.scale - self.cord[0] * (self.tile_w/2) * self.scale)/2 #- self.follow['y']
		self.curchunk = [int(int(self.cord[0]/8)),int(int(self.cord[1]/8))]
		pp = int(np.floor(3 / self.scale))
		self.slices = [(self.curchunk[0]-pp)*8,(self.curchunk[1]-pp)*8]
		if self.slices[0]<0: self.slices[0]=0
		if self.slices[1]<0: self.slices[1]=0
		self.slices[0]= (self.slices[0], (self.curchunk[0]+pp+1)*8)
		self.slices[1]= (self.slices[1], (self.curchunk[1]+pp+1)*8)

	def check_border(self, eixo):
		'''check axix border'''
		if self.cord[eixo] < 0:		return 0
		if self.cord[eixo] > self.size[eixo]:
			return int(self.size[eixo])
		return int(self.cord[eixo])

	def update_follow(self, ent=False, spd= 1):
		if ent:
			self.follow['x']=ent.pos[0] 
			self.follow['y']=ent.pos[1]
			spd = ent.inf['speed']		
		inc= np.ceil((8 / spd) / self.scale)		
		self.x = self.x - (self.follow['x']/inc)
		self.y = self.y - (self.follow['y']/inc)

	def __str__(self):
		return "Cam: ({}, {}), Cord: {}".format(self.x, self.y, self.cord)

class Game:
	def __init__(self, size, scale, map, obj_map, new_map, path_map, seed, genomes=False, config=False):
		#--Maps--#
		self.data = {"map" : map,
					 "obj" : obj_map,
					 "new" : new_map,
					 'path': path_map,
					 "ent" : np.zeros(map.shape+(1,)).astype("int").tolist(),
					 'bush': []}
		
		self.seed=seed
		self.ent_list = list()
		self.width, self.height = size
		self.scale = scale
		self.tick=0
		environ['SDL_VIDEO_WINDOW_POS'] = "center"
		self.DISPLAYSURF = pygame.display.set_mode((self.width, self.height), HWSURFACE)    #set the display mode, window title and FPS clock
		self.screenx = 1000
		self.screeny = 600
		pygame.display.set_caption('Map Rendering Demo')
		pygame.key.set_repeat(1, 100)
		self.FPSCLOCK = pygame.time.Clock()
		self.TILEWIDTH = 64
		self.TILEHEIGHT = 64
		self.TILEHEIGHT_HALF = (self.TILEHEIGHT / 2) * self.scale
		self.TILEWIDTH_HALF = (self.TILEWIDTH / 2) * self.scale
		#--Others--#
		self.len_x = len(map)
		self.len_y = len(map[0])
		self.chunk = False
		self.nfps=0
		self.colors = {'black':(0, 0, 0), 'RED' : pygame.Color(255, 0, 0)}
		self.data["cord"] = self.c_map(True)
		self.cam = Camera(map.shape, scale, self)		
		self.load_text = tx.load_text
		self.update_text = tx.update_text
		self.db, self.fonts = self.load_text(self)	
		self.rand_food()
		HUD.reset()
		en.Ent.reset()
		en.Ent.data = self.data
		en.Ent.display = self.DISPLAYSURF
		en.Ent.load_log_model()
		en.Ent.ent_list = self.ent_list
		Action.data=en.Ent.data
		Action.ent_list = en.Ent.ent_list

		
		self.nb_list=[]
		self.nbred_list=[]
		for x in range(9):
			self.nb_list.append(tx.new_text(self.fonts, 'calibri_15', x, (255, 255, 255)))
			self.nbred_list.append(tx.new_text(self.fonts, 'calibri_15', x, (164, 1, 0)))
		self.load_spr()
		self.surf_draw()
		HUD.setid = self.setid
		HUD.ent_list = self.ent_list
		self.hud = HUD(self.DISPLAYSURF)
		self.hud.print("Game Started")
		self.hud.print("Sprites Loaded")
		self.print = self.hud.print
		self.tdraw=True
		self.started=False
		self.srate = 30
		HUD.started=False
		self.jumpgen=False
		self.rates =  {
		'spawn':  self.srate,
		'nbunny': 30,
		'nfox':   10
		}
		
		Setting.globaldb = self.rates
		en.Ent.Sett.gdb = Setting.globaldb
		en.Ent.Sett.create_bars()

		local_dir = os.path.dirname(__file__)
		config_file = os.path.join(local_dir, 'config.txt')	
		config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
							 neat.DefaultSpeciesSet, neat.DefaultStagnation,
							 config_file)


		file1 = open('trained/best_bunny.pkl', 'rb')
		file2 = open('trained/best_fox.pkl', 'rb')
		
		self.bunny_genome = pk.load(file1)
		self.fox_genome   = pk.load(file2)

		file1.close()
		file2.close()
		#---------------------------------------------------
		self.training=False  
		en.Ent.training = self.training
		#---------------------------------------------------
		self.config = config
		if self.training:
			self.neat_apply(bunny, config)
			self.start_training()
		

	def start(self, config):

		bunny_net = neat.nn.FeedForwardNetwork.create(self.bunny_genome, config)
		fox_net   = neat.nn.FeedForwardNetwork.create(self.fox_genome, config)
		en.Ent.nn = {'bunny':bunny_net, 'fox':fox_net}

		for _ in range(self.rates['nbunny']):
			self.add_entitie('bunny')

		for _ in range(self.rates['nfox']):
			self.add_entitie('fox')

		HUD.calc(self.ent_list, 1, 0)
		self.started=True
		HUD.started=True
		HUD.wdata['start']['rates'] = self.rates
		HUD.wdata['start']['seed'] = self.seed
		HUD.wdata['start']['ent'] = en.Ent.database

	def start_training(self):
		for genome_id, genome in self.genomes:
			net = neat.nn.FeedForwardNetwork.create(genome, self.config)
			genome.fitness = 0
			a+=1
			if a<35:
				self.add_entitie("fox", genom=genome, nn=net, gid = genome_id)	

		for x in range(40):
			self.add_entitie("bunny")

	def neat_apply(self, genomes, config):
		if genomes==False: return
		self.nets = []
		self.ge   = []
		self.genomes= genomes
		self.config = config

	def addcord(self,eixo,val, auto=False):
		'''add cord to cam'''
		if auto==False:
			self.cam.follow['x']=0
			self.cam.follow['y']=0
			self.cam.update_follow()
			for x in self.ent_list:
				x.followed=False
		self.cam.addcord(eixo,val)
		en.Ent.sdraw=True
		self.update_text(self)

	def load_spr(self, init=True):
		'''load sprs'''
		self.fps = False
		size_64 = (64, 0, 64, 128, True)
		ss = ha.SpriteSheet('data/tileseta.png')
		sa = ha.SpriteSheet('data/objset.png')
		sd = ha.SpriteSheet('data/creature_set.png')
		self.spr = []
		self.obj = []
		en.Ent.min=[]
		
		for x in range(8):
			self.spr.append(self.setid(x, ss, size_64))
			self.obj.append(self.setid(x, sa, size_64))
		if init:
			self.crt = []
			for x in range(6):
				self.crt.append(self.setid(x, sd, size_64))
				self.crt.append(self.setid(x, sd, size_64, True))
				en.Ent.min.append((self.setid(x, sd, (64, 0, 64, 128, False), True)))
							
	def setid(self, ide, ss, size, flip = False, colorkey = (0, 0, 0)):
		'''load sprite partial'''
		scale=1
		try:
			x, y, w, h, sca, scale = (size)
		except:
			x, y, w, h, sca = (size)
		surface = ss.image_at((x * ide, y, w, h), colorkey).convert()
		if scale!=1:
			surface = pygame.transform.scale(surface, (int(w * scale), int(h * scale))).convert()
		if sca:
			surface = pygame.transform.scale(surface, (int(64 * self.scale * scale), int(128 * self.scale * scale))).convert()
		if flip:
		  surface = pygame.transform.flip(surface, True, False).convert()
		return surface

	def add_entitie(self, name, cord='rand', gene=False, genom=False, nn=False, gid = False):
		if genom:
			self.nets.append(nn)			
			self.ge.append(genom)
			genom.fitness=0
			self.ent_list.append(en.Ent(self, name, cord, gene, genom, nn, gid))
		else:
			self.ent_list.append(en.Ent(self, name, cord, gene))
		self.hud.refresh_list(self.ent_list)
		HUD.bdraw=True

	def kill(self, num, string="unknow"):		
		for nb, x in enumerate(self.ent_list):
			if num.id == x.id:
				if self.training:
					for ab, y in enumerate(self.ge):
						if y == x.genome:
							x.genome.fitness-=5
							del(self.ge[ab])
							del(self.nets[ab])
				del(self.ent_list[nb])
				en.Ent.sdraw=True	
				# print(f"Gen : {len(self.ge)}, NN : {len(self.nets)}")			
				self.data['ent'][num.cord[0]][num.cord[1]].remove(num.id)
				HUD.bdraw=True
				return HUD.print("{} Id {}, died from {}, Fit: {}". format(num.name, num.id, string, num.genome.fitness))


	def chunk_exec(self):
		self.chunk = False if self.chunk else True
		HUD.print("Chunk Activated/Desactivated")
		en.Ent.sdraw=True

	def open_map(self):
		fig=plt.figure(figsize=(12, 6))
		fig.add_subplot(1, 2, 1)
		plt.imshow(self.data['obj'])
		fig.add_subplot(1, 2, 2)		
		plt.imshow(self.data["new"])
		plt.show()	
		HUD.print("Map Opened")

	def c_map(self, auto=False):
		'''load map coordinates'''
		cord_map = np.zeros(self.data["map"].shape+(2,)).astype("int").tolist()
		for row_nb in range(self.len_x):
			for col_nb in range(self.len_y):
				cart_y = row_nb * self.TILEWIDTH_HALF
				cart_x = col_nb * self.TILEHEIGHT_HALF
				iso_x = (cart_x - cart_y)
				iso_y = (cart_x + cart_y)/2
				cord_map[col_nb][row_nb] = (iso_x + (self.screenx / 2) + 350 , iso_y + self.height / 2)		
				if auto ==True:
					self.data['ent'][col_nb][row_nb]=[]
					if self.data['obj'][col_nb][row_nb] in [2, 7]:
						self.data["bush"].append((col_nb,row_nb))
					self.len_food=len(self.data['bush'])
		return cord_map

	def change_scale(self, nscale):
		print("Need Fixing")
		return False
		'''change cam scale'''
		self.scale = self.scale + nscale
		self.scale = 0.25 if self.scale==0 else self.scale
		self.cam.__init__(self.cam.size, self.scale, self, self.cam.cord)
		self.TILEHEIGHT_HALF = int((self.TILEHEIGHT /2) * self.scale)
		self.TILEWIDTH_HALF = int((self.TILEWIDTH /2) * self.scale)
		self.load_spr(False)
		self.data["cord"] = self.c_map()
		self.hud.print("New scale", self.scale)
		self.surf_draw()
		for x in self.ent_list:
			x.resize_sprites(self.scale)


	def surf_draw(self):
		self.DISPLAYSURF.fill(self.colors["black"])
		for row_nb, row in enumerate(self.data["map"][self.cam.slices[0][0]:self.cam.slices[0][1]]):  
			row_nb=row_nb+self.cam.slices[0][0]	
			for col_nb, tile in enumerate(row[self.cam.slices[1][0]:self.cam.slices[1][1]]):
				col_nb = self.cam.slices[1][0] +col_nb
				cord_x = self.data["cord"][row_nb][col_nb][0]+self.cam.x
				cord_y = self.data["cord"][row_nb][col_nb][1]+self.cam.y
				ent_id=0
				if self.data['ent'][row_nb][col_nb]:
					ent_id=1
				if cord_x > -80 + 350 and cord_x < 1032 + 350 and cord_y > -200 and cord_y < 632:
					self.DISPLAYSURF.blit(self.spr[tile], (cord_x, cord_y))
					obj_id = int(self.data["obj"][row_nb][col_nb])					
					if obj_id + 1:
						self.DISPLAYSURF.blit(self.obj[obj_id], (cord_x, cord_y))
					if self.chunk:
						self.DISPLAYSURF.blit(self.nb_list[tile], (cord_x + 25, cord_y + 75))
						self.DISPLAYSURF.blit(self.nbred_list[ent_id], (cord_x + 33, cord_y + 67))
		HUD.update_back=True


	def map_update(self):
		if en.Ent.update == True:
			self.data = en.Ent.data
			en.Ent.update = False
			en.Ent.sdraw=True
			

	def rand_food(self):
		for row_nb, row in enumerate(self.data["obj"]):  
			for col_nb, tile in enumerate(row):
				if tile == 2:
					if np.random.randint(100)<18:
						self.data["obj"][row_nb][col_nb]=7

	def spawn_food(self):		
		for n in range(10):
			x, y = choice(self.data['bush'])
			if self.data['obj'][x][y]==2: 
				self.data['obj'][x][y]=7
				return

	def draw_chunks(self):
		'''draw chunks and red circles'''
		pygame.draw.circle(self.DISPLAYSURF, self.colors["RED"], (int(self.data["cord"][0][0][0] + 32 * self.scale), int(self.data["cord"][0][0][1] + 86 *self.scale)), 10, 1) 
		for row_nb in range(0, self.len_x, 8):
			for col_nb in range(0, self.len_y, 8):
				cord_x = self.data["cord"][row_nb][col_nb][0] + self.cam.x
				cord_y = self.data["cord"][row_nb][col_nb][1] + self.cam.y
				points = [[cord_x + (32     ) * self.scale, cord_y  +  (70       ) * self.scale],
						  [cord_x + (64+32*7) * self.scale, cord_y  +  (87 + 16*7) * self.scale],
						  [cord_x + (32     ) * self.scale, cord_y  +  (103+ 32*7) * self.scale],
						  [cord_x - (32*7   ) * self.scale, cord_y  +  (87 + 16*7) * self.scale]]
				pygame.draw.polygon(self.DISPLAYSURF, self.colors["RED"], points,1)   

	def info_draw(self):
		'''Draw Text on Screen'''
		self.DISPLAYSURF.blit(self.db["cords"], (self.screenx/2 -16 + 350, 5))
		#self.DISPLAYSURF.blit(self.db["ent_num"], (self.screenx/2 + 50, 5))
		if self.fps:
			self.nfps=self.FPSCLOCK.get_fps()
			#pygame.draw.rect(self.DISPLAYSURF, self.colors['black'],((0,0),(5,5)))
			self.DISPLAYSURF.blit(self.db["fps"], (5, 5))

	def bestfollow(self):
		a=0
		for y in self.ent_list:
			if y.genome.fitness>a:
				a=y.genome.fitness
				y.get_followed(self)

			


	def draw(self):
		mtime=pygame.time.get_ticks()
		
		if self.fastmode:
			if self.tick%50==0:
				self.tdraw=True
			else:
				self.tdraw=False
		if self.started:		
			if (self.tick%self.srate)==0:
				self.spawn_food()
				 
		en.Ent.cam_pos = [0, 0]
		self.map_update()
		if self.tdraw:
			if en.Ent.sdraw:
				en.Ent.sdraw = False
				self.surf_draw()
				HUD.bdraw=False
		
		for ent in self.ent_list:
			ent.action(self)
			ent.draw(self)	

		if self.chunk:
			self.draw_chunks()	

		self.hud.draw(self.DISPLAYSURF, self.tdraw, self.tick, self.ent_list)
		self.info_draw()
		self.tdraw=True
		if pygame.time.get_ticks() - mtime>37:
			self.tdraw=False
			#print(pygame.time.get_ticks() - mtime)
		if self.started:
			if len(self.ent_list)==0 or len(self.ent_list)>150 :
				self.started=False
				self.run=False
						
						