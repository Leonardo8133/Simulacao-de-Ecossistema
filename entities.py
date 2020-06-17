import numpy.random
from numpy import abs 
from path import *
from hud import HUD
import texts as tx
import pygame.transform
import ha
import pickle as pc
from settings import Setting
from action import Action


class Gg:
	def __init__(self):
		self.fitness=0

class Ent(Action):	
	@staticmethod
	def reset():
		Ent.next_id = 0
		Ent.status = "idle"
		Ent.current = ['empty']
		Ent.cam_pos = [0, 0]
		Ent.counter = -1
		Ent.sdraw = False
		Ent.fonts= tx.load_font()
		Ent.sblue = (127, 118, 200)
		Ent.nn = {'bunny':None, 'fox':None}
		Ent.training = False
		Ent.add=0
		Ent.database={
			'bunny':{
				'inc':{
					'hungry':0.02,#002
					'thirst':0.025,#025
					'love'  :0.02,#002
					'rest'  :0.025#0025
					  	},
				'base':{
					'hungry':100,
					'thirst':100,
					'love'  :100,
					'rest'  :100
						},
				'inf':{
					'speed': 0,
					'view':6,
					'maxchild':8
						}
					},
			'fox':{
				'inc':{
					'hungry':0.03,
					'thirst':0.03,
					'love'  :0.02,
					'rest'  :0.03
					  	},
				'base':{
					'hungry':200,
					'thirst':200,
					'love'  :100,
					'rest'  :200
						},
				'inf':{
					'view':10,
					'speed': 0,
					'maxchild':2
						}
				}
			}
				
		Ent.update=False
		Ent.reg=list()
		Ent.Sett= Setting(Ent.database)
		#file= open("cmds.pkl", 'ab')
		Action.update = Ent.update
		Action.sdraw  = Ent.sdraw
		Action.database = Ent.database


	def __init__(self,game,name,cord="rand", gene=False, genome=False, nn=False, gid=False):
		Ent.next_id += 1
		self.id = Ent.next_id
		self.name = name				
		self.cord = list(self.spawn(cord, self.name))
		self.scord = self.cord.copy()
		self.lasterror= [-1,-1]
		if genome:
			self.genome = genome
			self.nn = nn
			self.gid = gid
		else:
			self.genome = Gg()
			self.nn = Ent.nn[self.name]
	
		self.load_varables(game, gene)				
		self.needs={
		'hungry':[50, self.base['hungry'], (106, 190, 48), (158, 18, 130, 7)],
		'thirst':[50, self.base['thirst'], (91, 110, 225), (158, 31, 130, 7)],
		'love':  [50, self.base['love'],   (172, 50, 50 ), (158, 44, 130, 7)],
		'rest':  [0, self.base['rest'],   (182, 177, 74), (158, 58, 130, 7)]
		}
		if self.inf['gender']=='male':
			self.global_inc['love']=0
			self.needs['love'][0]=0
		if cord!='rand':
			HUD.lovet[self.specie].append((self.specie, self.id, self.cord.copy()))

		
	def __str__(self):
		return "{} n: {} pos {}, current: {}, with queue: {}".format(self.name, self.id, self.pos, self.current, self.queue[:5])
#-----------------------------Init Functions--------------------------#
	def load_varables(self, game, gene):
		#--- Sprites----#
		self.eat_counter   = 0
		self.drink_counter = 0
		self.love_counter  = 0
		self.flp_f = self.load_sprites(game, False)
		self.flp_t = self.load_sprites(game, True)
		self.spr = self.flp_f
		self.buf_flpf = self.flp_f.copy()
		self.buf_flpt = self.flp_t.copy()
		self.lovedelay=4000
		sh = ha.SpriteSheet('data/colect1.png')
		self.icon_spr={}
		self.icons={
		'resting' :(137, 1, 31, 32, False),
		'loving'  :(169, 1, 22, 22, False),
		'eating'  :(192, 1, 18, 22, False),
		'drinking':(211, 1, 18, 22, False),
		'walking' :(230, 1, 32, 22, False),
		'waiting' :(0, 0, 0, 0, False),
		'idle'    :(0, 0, 0, 0, False)}
		for x, y in self.icons.items():
			self.icon_spr[x] = game.setid(1, sh, y)		
		#---------------#
		gender=('male','female')
		if gene==False:
			self.inf={
						'age': 15,#numpy.random.randint(5,16),
						'speed': numpy.random.randint(-10,10)*0.015625 + 1 + Ent.database[self.specie]['inf']['speed'],
						'view': Ent.database[self.specie]['inf']['view'],
						'gender':gender[numpy.random.randint(2)],
						'type':"log"}
			self.inc={
						'hungry':numpy.random.randint(-20, 20)/100 +1,
						'thirst':numpy.random.randint(-20, 20)/100 +1,
						'love':  numpy.random.randint(-20, 20)/100 +1,
						'rest':  numpy.random.randint(-20, 20)/100 +1}
			self.base={
						'hungry':numpy.random.randint(-20, 20)/100 +1 * Ent.database[self.specie]['base']['hungry'],
						'thirst':numpy.random.randint(-20, 20)/100 +1 * Ent.database[self.specie]['base']['thirst'],
						'love':  numpy.random.randint(-20, 20)/100 +1 * Ent.database[self.specie]['base']['love'],
						'rest':  numpy.random.randint(-20, 20)/100 +1 * Ent.database[self.specie]['base']['rest']}
		if gene:
			self.inf={
						'age':0,
						'speed': numpy.random.randint(-10,10)*0.015625 + 1 * gene['inf']['speed'],
						'view': Ent.database[self.specie]['inf']['view'],
						'gender':gender[numpy.random.randint(2)],
						'type':"log"}
			self.inc={
						'hungry': numpy.random.randint(-8, 8)/100 + 1 *gene['inc']['hungry'],
						'thirst': gene['inc']['thirst'],
						'love':   numpy.random.randint(-8, 8)/100 + 1 *gene['inc']['love'],
						'rest':   gene['inc']['rest']}

			self.base={
						'hungry':numpy.random.randint(-5, 5)/100 +1 * gene['base']['hungry'],
						'thirst':numpy.random.randint(-5, 5)/100 +1 * gene['base']['thirst'],
						'love':  numpy.random.randint(-5, 5)/100 +1 * gene['base']['love'],
						'rest':  numpy.random.randint(-5, 5)/100 +1 * gene['base']['rest']}



		self.inc={
						'hungry':self.inc['hungry'] * ((self.inf['speed']/2) +0.5),
						'thirst':self.inc['thirst'] * ((self.inf['speed']/2) +0.5) / (self.inc['hungry']**2),
						'love':  self.inc['love']   * self.inf['speed']**2,
						'rest':  self.inc['rest']   * ((self.inf['speed']/2) +0.5) / (self.inc['hungry']/2 +0.5)} 


		self.global_inc={
						'hungry': Ent.database[self.specie]['inc']['hungry'] * self.inc['hungry'] * ((self.inc['love']/2) +0.5),
						'thirst': Ent.database[self.specie]['inc']['thirst'] * self.inc['thirst'] * ((self.inc['love']/2) +0.5),
						'love'  : Ent.database[self.specie]['inc']['love']   * self.inc['love'],
						'rest'  : Ent.database[self.specie]['inc']['rest']   * self.inc['rest']
		}

		


		self.stp_scale= 2 * self.inf['speed'] * game.scale	
		game.data["ent"][self.cord[0]][self.cord[1]].append(self.id)
		self.walkeable = [0, 3, 4]
		self.water = [2, 1]
		self.queue = list()	
		self.upqueue=list()	
		self.path = set_path
		self.rand_path = random_path
		self.validate =  value_tile
		self.steps=0
		self.lovedelay=0
		self.score = 0 
		self.buf=0
		self.pos=[0,0]
		self.followed=False
		self.death=0		
		self.birth=False
		self.b_counter=-1
		self.ticks=0
		self.tries=[0,0,0]

										
		self.astxt={'name_10' : tx.new_text(self.fonts, 'calibri_10', ('{} {}').format(self.inf['gender'], self.name), self.sblue),
					'id'      : tx.new_text(self.fonts, 'calibri_10', self.id, self.sblue),
					'walking' : tx.new_text(self.fonts, 'calibri_10', 'walking',self.sblue),
					'idle'    : tx.new_text(self.fonts, 'calibri_10', 'idle', self.sblue),
					'eating'  : tx.new_text(self.fonts, 'calibri_10', 'eating', self.sblue),
					'drinking': tx.new_text(self.fonts, 'calibri_10', 'drinking', self.sblue),
					'resting' : tx.new_text(self.fonts, 'calibri_10', 'resting', self.sblue),
					'waiting' : tx.new_text(self.fonts, 'calibri_10', 'waiting', self.sblue),
					'loving'  : tx.new_text(self.fonts, 'calibri_10', 'loving', self.sblue),
					'view'    : tx.new_text(self.fonts, 'calibri_15', 'Viewing {}, with ID: {}, Fitness: {:.2f}'.format(self.name, self.id, self.genome.fitness), (171, 191, 200)),
					'speed'   : tx.new_text(self.fonts, 'calibri_10', ('Speed:  {:.2f}').format(self.inf['speed']), self.sblue),
					'hungry'  : tx.new_text(self.fonts, 'calibri_10', ('Hungry: {:.2f}').format(self.inc['hungry']), self.sblue),
					'thirst'  : tx.new_text(self.fonts, 'calibri_10', ('Thirst: {:.2f}').format(self.inc['thirst']), self.sblue),
					'love'    : tx.new_text(self.fonts, 'calibri_10', ('Love:   {:.2f}').format(self.inc['love']), self.sblue),
					'rest'    : tx.new_text(self.fonts, 'calibri_10', ('Rest:   {:.2f}').format(self.inc['rest']), self.sblue),
					'fitness' : tx.new_text(self.fonts, 'calibri_10', ('Fit:    {:.2f}').format(self.genome.fitness), self.sblue),
					'age'     : tx.new_text(self.fonts, 'calibri_10', ('Age:   {}').format(self.inf['age']), self.sblue)
				   }

	def spawn(self, cord, name):
		if cord == "rand":
			for n in range(20):
				x = numpy.random.randint(1, 127, size = (2))
				if self.data['path'][x[0]][x[1]] == 1:
					HUD.print("New {} Spawned at Cord: {}".format(name, x))
					return x
		return cord

	def diff(self, l1, l2):
		return [l1[0]-l2[0], l1[1]-l2[1]]

	def load_sprites(self, game, flip = False):		
		
		if self.name.upper() == 'BUNNY':
			self.specie="bunny"
			self.sprid=0
			self.spw =-1
			if flip == False:
				return pygame.transform.scale(game.crt[0], (int(64 * game.scale), int(128 * game.scale)))
			else:
				return pygame.transform.scale(game.crt[1], (int(64 * game.scale), int(128 * game.scale)))
		elif self.name.upper() == 'FOX':
			self.spw=1
			if flip == False:
				self.specie="fox"
				self.sprid=8
				return pygame.transform.scale(game.crt[8], (int(64 * game.scale), int(128 * game.scale)))
			else:
				return pygame.transform.scale(game.crt[9], (int(64 * game.scale), int(128 * game.scale)))


# --------------------------- Draw Functions --------------------------------#
	def resize_sprites(self, scale):	
		self.stp_scale= 4*scale	
		self.spr   = pygame.transform.scale(self.buf_flpf, (int(64 * scale), int(128 * scale)))
		self.flp_f = pygame.transform.scale(self.buf_flpf, (int(64 * scale), int(128 * scale)))
		self.flp_t = pygame.transform.scale(self.buf_flpt, (int(64 * scale), int(128 * scale)))
		self.stp_scale = 2 * self.inf['speed'] * scale

	def flip(self):
		xy = (self.current[1], self.current[2])
		if xy == (1, 0) or xy == (0, -1) or xy == (1, -1):
			self.spr = self.flp_t
		if xy == (0, 1) or xy == (-1, 0) or xy == (-1, 1):
			self.spr = self.flp_f

	def draw(self, game):	
		self.tick(game)			
		try:
			cord_x = self.data["cord"][self.cord[0]][self.cord[1]][0] + game.cam.x
			cord_y = self.data["cord"][self.cord[0]][self.cord[1]][1] + game.cam.y
		except:
			print(self)
		if game.tdraw:
			if self.followed==True:
				self.display.blit(self.icon_spr[self.status], (cord_x + self.pos[0] +25, cord_y + self.pos[1] + 45))
				self.display.blit(self.spr, (cord_x + self.pos[0], cord_y + self.pos[1]))
				self.display.blit(self.astxt['view'], (800, 50))
			else:	
				self.display.blit(self.icon_spr[self.status], (cord_x + self.pos[0] + 25 +  Ent.cam_pos[0]/4, cord_y + self.pos[1] + 45 + Ent.cam_pos[1]/4))
				self.display.blit(self.spr, (cord_x + self.pos[0] + Ent.cam_pos[0]/4, cord_y + self.pos[1] + Ent.cam_pos[1]/4))

		if self.status != 'idle':
			self.update_pos(game)
			HUD.update_back=True
#--------------------------Queue Functions--------------------------#
	def read_queue(self):
		if len(self.queue):
			if self.current == ['empty']:
				self.current = self.queue[0]
				self.queue.pop(0)
				self.status='idle'					
			if self.current[0] == 'walk' and self.status == "idle":
				self.status = 'walking'	
				self.counter = numpy.ceil(16/self.inf['speed'])
				self.flip()
			self.read_cmd()			
		else:		
			if self.current == ["empty"]:
				self.status='idle'
				Ent.update=True

	def read_cmd(self):
		
		if self.current[0]=='cmd' and self.status == "idle":
			if self.current[2]=="eat":
				if eval(self.current[1]):
					self.score+=10
					self.status="eating"
					self.counter=230
			if self.current[2]=="look":
				if self.specie=='bunny':
					self.ident_run()
					self.counter=0
					self.status='waiting'
				
			elif self.current[2]=="drink":					
				if eval(self.current[1]):
					self.score+=10
					self.status="drinking"
					self.counter=220
					self.drink_counter+=1
					self.genome.fitness += (self.needs['thirst'][0]/self.needs['thirst'][1]-0.5)*40
				
			elif self.current[2]=="rest":
				self.status="resting"
				self.counter=300
				self.genome.fitness += (self.needs['rest'][0]/self.needs['rest'][1]-0.5)*40

			elif self.current[1]=='self.love()':
				if eval(self.current[1]):
					self.status="loving"
					self.counter=130
					self.lovedelay=2400
			elif self.current[2]=='hunt':
				if eval(self.current[1]):
					
					self.status='eating'
					self.counter=120
				else:
					self.status='waiting'
					self.counter=0			
					
			self.current = ['empty']

			#Ent.register_cmd(self)
		elif self.current[0]=='path' and self.status == "idle":
			self.path(self, self.current[1])
			self.current = ['empty']			

	@staticmethod
	def register_cmd(ent):
		c=0
		if ent.current[2] in ["eat", "love", "drink", "rest"]:
			temp = []
			for x in ent.needs.values():
				temp.append(x[0]/x[1])
			if ent.current[2] == "eat":	c=1
			if ent.current[2] == "drink": c=2
			if ent.current[2] == "love":c=3
			if ent.current[2] == "rest":c=4
			temp.append(c)
			pc.dump(temp, Ent.file)
			print(temp)
		
	@staticmethod
	def decision_log(ent):
		temp=[]
		for x in ent.needs.values():
				temp.append(x[0]/x[1])
		return Ent.model.predict([[temp[0],temp[1],temp[2],temp[3]]])	

	@staticmethod
	def load_log_model():
		file = open("logs.pkl", "rb")
		Ent.model = pc.load(file)
		HUD.print("IA Loaded")
		file.close()		

	def getin(self):
		in1 = (self.needs['hungry'][0]/(self.needs['hungry'][1]-20)*2)-1
		in2 = (self.needs['thirst'][0]/(self.needs['thirst'][1]-20)*2)-1
		in3 = (self.needs['love'][0]/(self.needs['love'][1])*2)-1
		in4 = (self.needs['rest'][0]/(self.needs['rest'][1]-20)*2)-1
		return in1, in2, in3, in4


	def action(self, game):
		self.astxt['fitness'] = tx.new_text(self.fonts, 'calibri_10', ('Fit:    {:.2f}').format(self.genome.fitness), self.sblue)
		if self.status=="idle" and len(self.queue)==0 and self.current==['empty']:
			dec=[5]
			#if self.specie=='bunny' and self.ident_run():return
			# dec = Ent.decision_log(self)
			in1, in2, in3, in4= self.getin()
			output = self.nn.activate((in1, in2, in3, in4))
			dec[0]= np.argmax(output)+1
			if dec[0]==1:
				if self.specie.lower()=='bunny':
					if not self.search_for('food'):
						if self.tries[0]<3:
							self.rand_path(self, 4)
							self.tries[0]+=1
						else:
							self.rand_path(self, 24, True, 'food')
							self.tries[0]==0
				else:
					if not self.search_for('hunt'):
						if self.tries[0]<3:
							self.rand_path(self, 4)
							self.tries[0]+=1
						else:
							self.rand_path(self, 24, True, 'food')
							self.tries[0]==0					
			elif dec[0]==2:
				if not self.search_for('water'):
					if self.tries[1]<3:
						self.rand_path(self, 4)
						self.tries[1]+=1
					else:
						self.rand_path(self, 24, True, 'water')
						self.tries[1]==0
				return

			elif dec[0]==3 and self.tries[2]<5:
				
				self.needs['love'][0]=0
				if not self.search_for('love'):
					if self.tries[2]<2:
						self.rand_path(self, 4)
						self.tries[2]+=1
					else:
						self.rand_path(self, 24, True, 'love')
						self.tries[2]==0
				return

			elif dec[0]==4:
				self.queue.append(("cmd", "self.rest()", "rest"))	
				self.read_queue()
				return

			elif dec[0]==5:
				
				if self.needs['thirst'][0]/self.needs['thirst'][1]<0.5 and self.needs['hungry'][0]/self.needs['thirst'][1]<0.5:
					self.rand_path(self, 24, True, 'love')

					return
				if self.needs['thirst'][0]>self.needs['hungry'][0]:
					self.rand_path(self, 24, True, 'water')
				else:
					if self.specie=='fox':
						self.rand_path(self, 32, True, 'hunt')
					else:
						self.rand_path(self, 24, True, 'food')
				
		
		if self.status=='idle' and len(self.queue)!=0:
			self.read_queue()

#-----------------Update Functions-------------------------#
	def update_pos(self, game):		
		if self.counter > 0:
			self.counter -= 1
			self.update_status()
			if self.status=='walking':
				if self.needs['rest'][0]<self.needs['rest'][1]:
					self.needs['rest'][0]+= (self.global_inc['rest'] * 3)
				Ent.sdraw = True				
				self.pos[0] = self.pos[0] + self.stp_scale * self.current[1] - (self.stp_scale * self.current[2])
				self.pos[1] = self.pos[1] + (self.stp_scale/2) * self.current[1] + ((self.stp_scale/2) * self.current[2])

				if self.followed==True:
					Ent.cam_pos = self.pos
					game.cam.update_follow(self)	

		elif self.counter == 0:
			if self.status=='walking':
				self.reset_pos(game)
				self.score+=0.5
			self.counter -= 1
			self.current = ["empty"]
			self.read_queue()	

	def update_status(self):
		if self.status=='eating':
			self.needs['hungry'][0]-= 2
			if self.needs['hungry'][0]<0: self.needs['hungry'][0]=0
			self.needs['rest'][0]-= 0.02 + self.global_inc['rest']
			if self.needs['rest'][0]<0: self.needs['rest'][0]=0
			if self.needs['love'][0] <= self.needs["love"][1]:
				if self.inf['age']>=12 and self.lovedelay<5:
					self.needs['love'][0] += (self.global_inc['love']*4 + self.global_inc['love']**0.8)
		if self.status=='drinking':
			self.needs['thirst'][0]-= 2.5
			if self.needs['thirst'][0]<0: self.needs['thirst'][0]=0
			self.needs['rest'][0]-= 0.02 + self.global_inc['rest']
			if self.needs['rest'][0]<0: self.needs['rest'][0]=0
		if self.status=='resting':
			self.needs['rest'][0]-= 0.6
			if self.needs['rest'][0]<0: self.needs['rest'][0]=0
		if self.status=="loving":
			self.needs['love'][0]-= 2
			if self.needs['love'][0]<0: self.needs['love'][0]=0
			self.needs['rest'][0]-= 0.02 + self.global_inc['rest']
			if self.needs['rest'][0]<0: self.needs['rest'][0]=0


	def reset_pos(self, game):
		
		try:
			game.data["ent"][self.cord[0]][self.cord[1]].remove(self.id)
		except:
			pass


		self.cord[0] += self.current[1]
		self.cord[1] += self.current[2]
		if self.cord[0]==128:
			self.cord[0]-=self.current[1]
			self.queue=[]
			self.current=["empty"]
			print("WARNING -- CORD X 128 FOR ID: ", self.id, "Something is wrong")
		if self.cord[1]==128:
			self.cord[1] -= self.current[2]
			self.queue=[]
			self.current=["empty"]
			print("WARNING -- CORD Y 128 FOR ID: ", self.id, "Something is wrong")

		

		game.data["ent"][self.cord[0]][self.cord[1]].append(self.id)
		# except:
		# 	HUD.print("Error reset_pos Id: ", self.id)
		self.pos = [0, 0]			
		if self.followed==True:
			game.cam.update_follow(self)
			game.addcord(0, self.current[1], True)
			game.addcord(1, self.current[2], True)
		
	def up_queue(self, game):
		if self.upqueue:
			if self.upqueue[0][0]=='set_wait':
				#print("Trying to set wait", self.id, self.upqueue[0][1])
				for x in game.ent_list:
					if x.id==self.upqueue[0][1] and x.inf['gender']=='male' and self.specie==x.specie:
						x.upqueue.append(["wait", 100])
						#print("setted to wait", x.id)

			if self.upqueue[0][0]=='run':
				self.queue=[]
				self.path_run(self.upqueue[0][1])
				self.upqueue=[]	

				return		
			elif self.upqueue[0][0]=="set_love":
				for x in game.ent_list:
					if x.id==self.upqueue[0][1] and x.inf['gender']=='male' and self.specie==x.specie:
						if x.status=="waiting":
							self.status="loving"
							x.status="loving"
							self.counter=200
							self.score+=100
							self.lovedelay=2000/self.inc['love']
							x.lovedelay=2000/x.inc['love']
							x.score+=100							
							self.genome.fitness += (self.needs['love'][0]/self.needs['love'][1]-0.8)*70
							x.counter=200
							x.current=['empty']
							x.queue=[]
							x.upqueue=[]
							self.reproduce()
			elif self.upqueue[0][0]=='wait':
				self.status="waiting"
				self.counter=self.upqueue[0][1]
				self.upqueue=[]
				self.current=['empty']
				return
			self.upqueue.pop(0)

	def preg(self, game):
		if self.birth:			
			if self.b_counter==0:
				self.give_birth(game)
			self.b_counter-=1

	def tick(self, game, n=True):
		self.up_queue(game)
		self.preg(game)
		self.ticks+=1
		if self.lovedelay>0:
			self.lovedelay-=1
		if self.ticks%600==0:
			self.inf['age']+=1
			self.genome.fitness+=Ent.add
			if self.inf['age']>=50:
				game.kill(self, 'Old')
			self.astxt['age']=tx.new_text(self.fonts, 'calibri_10', ('Age:   {}').format(self.inf['age']), self.sblue)
		if self.needs['hungry'][0] <= self.needs['hungry'][1]:
			self.needs['hungry'][0] += self.global_inc['hungry']
		if self.needs['thirst'][0] <= self.needs["thirst"][1]:
			self.needs['thirst'][0] += self.global_inc['thirst']
		if self.needs['love'][0] <= self.needs["love"][1]:
			if self.inf['age']>=12 and self.lovedelay<5:
				self.needs['love'][0] += self.global_inc['love']/2
		if self.needs['rest'][0] <= self.needs["rest"][1]:
			self.needs['rest'][0] += self.global_inc['rest']
		for b,  x in self.needs.items():
			if x[0]>=x[1]:
				if b != "love":
					self.death+=0.5
					self.motive=b
					n=False
		if n:
			self.death-=1
			if self.death<0: self.death=0
		if self.death>=300:
			self.score-=100
			game.kill(self, self.motive)
			HUD.deadt[self.specie].append((self.motive, self.specie, self.id, self.cord, self.score))	
#---------------------Math Functions ---------------------------#

	def calc_dist(self, start, end):
		x = abs((start[0]-end[0]))
		y = abs((start[1]-end[1]))
		return (x+y)

	def get_min(self, li, mini=1000, ind=0):	
		for k, v in enumerate(li):
			if v<mini:
				mini=v
				ind=k
		return mini, ind

	def get_slice(self, vw, spos=False):
		if spos:
			cs, cy = spos
		else:
			cs, cy = self.cord
		slcx = [cs-vw, cs+vw]
		slcy = [cy-vw, cy+vw]
		if slcx[0]<0:
			slcx[0]=0
		if slcy[0]<0:
			slcy[0]=0
		if slcx[1]>=127:
			slcx[1]=127
		if slcy[1]>=127:
			slcy[1]=127

		return slcx, slcy

#--------------------------- ACTION FUNCTIONS --------------------------------#
	def get_followed(self, game):
		for x in game.ent_list:
			x.followed=False


		ex, ey = self.cord
		cx, cy = tuple(game.cam.cord)
		game.addcord(0 , (ex - cx) * game.scale)
		game.addcord(1 , (ey - cy) * game.scale)
		self.followed=True
		self.astxt['view'] = tx.new_text(self.fonts, 'calibri_15', 'Viewing {}, with ID: {}, Fitness: {:.2f}'.format(self.name, self.id, self.genome.fitness), (221, 221, 250))

	def box_search(self, typ, diag=False):
		pos = self.cord
		may = False
		mb  = False
		if typ == "water":
			typ = 'map'
			num = 2
		if typ == 'food':
			typ = 'obj'
			num = 7
		if typ =='love':
			typ = 'ent'
		if typ == 'hunt':
			typ='ent'
		for x in range(-1,2,1):
			for y in range(-1,2,1):
				px = (pos[0]+x, pos[1]+y)
				if px[0]> 127 : continue
				if px[0]< 0   : continue
				if px[1]> 127 : continue
				if px[1]< 0   : continue	
				if not diag:	
					if x == 0 or y == 0:						
							if typ=='ent':
								if Ent.data[typ][px[0]][px[1]]:
									if Ent.data[typ][px[0]][px[1]][0]!=self.id:
										may=(x,y)
										mb=Ent.data[typ][px[0]][px[1]][0]
										break
							else:
										
								if Ent.data[typ][px[0]][px[1]] == num:
									may=(x,y)
				else:
					if typ=='ent':	
							if Ent.data[typ][px[0]][px[1]]:
								if Ent.data[typ][px[0]][px[1]][0]!=self.id:
									may=(x,y)
									mb=Ent.data[typ][px[0]][px[1]][0]
									break
					else:				
						if Ent.data[typ][px[0]][px[1]] == num:
							may=(x,y)
		return may, mb

	def box_search_sliced(self, typ, num, pos, slx, sly, res='love'):
		may = list()
		if res=='love':
			for x in range(-1,2,1):
				for y in range(-1,2,1):		
					if x == 0 or y == 0:	
						psx, psy = (pos[0]+ x + slx, pos[1]+ y +sly)
						if psx <0: continue
						if psy <0: continue
						if psx>126: continue
						if psy>126: continue
						if Ent.data['path'][psx][psy]==1:
							if (psx, psy) in self.lasterror:
								continue
							else:
								may.append((psx, psy))
		else:
			if Ent.data['path'][pos[0] + slx ][pos[1] + sly]==1:

							may.append((pos[0] + slx, pos[1] + sly))				
		return may
			
			
#-------------------------------Commands Functions-----------------------------------------#


