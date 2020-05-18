import texts as tx
from pygame import Rect

class Setting:
	fonts=tx.load_font()
	def __init__(self, database):
		Bar.idd=0
		Bar.offs=0
		self.name= "Tweakeables Variables"		
		self.glist = []
		self.blist = []
		self.flist = []
		self.btext = tx.new_text(Setting.fonts, 'calibri_15', "Bunny Rates", (127, 118, 200))
		self.ftext  = tx.new_text(Setting.fonts, 'calibri_15', "Fox Rates", (127, 118, 200))
		self.ptext  = tx.new_text(Setting.fonts, 'calibri_15', "Start Simulation", (127, 118, 200))
		self.receive_db(database)
		

	def print(self):
		print("Global Var")
		for x in self.glist:
			print(x)
		print("Bunny Var")
		for x in self.blist:
			print(x)
		print("Fox Var")
		for x in self.flist:
			print(x)

	def receive_db(self, db):
		Setting.database= db
		self.db = Setting.database
		self.bunnydb= {
		'Hungry Rate':  [self.db['bunny']['inc']['hungry'], "self.db['bunny']['inc']['hungry']"],
		'Thirst Rate':  [self.db['bunny']['inc']['thirst'], "self.db['bunny']['inc']['thirst']"],
		'Love Rate':	[self.db['bunny']['inc']['love'],   "self.db['bunny']['inc']['love']"],
		'Rest Rate':	[self.db['bunny']['inc']['rest'],   "self.db['bunny']['inc']['rest']"]}

		self.foxdb= {
		'Hungry Rate':  [self.db['fox']['inc']['hungry'], "self.db['fox']['inc']['hungry']"],
		'Thirst Rate':  [self.db['fox']['inc']['thirst'], "self.db['fox']['inc']['thirst']"],
		'Love Rate':	[self.db['fox']['inc']['love'],   "self.db['fox']['inc']['love']"],
		'Rest Rate':	[self.db['fox']['inc']['rest'],   "self.db['fox']['inc']['rest']"]}


	def create_bars(self):
		

		for key, value in self.bunnydb.items():
			self.blist.append(Bar(key, value))

		for key, value in self.foxdb.items():
			self.flist.append(Bar(key, value))

		for key, value in {'Food Spawn Rate': [self.gdb['spawn'], "self.gdb['spawn']"], 'Starting Bunny':[self.gdb['nbunny'], "self.gdb['nbunny']"], 'Starting Fox':[self.gdb['nfox'], "self.gdb['nfox']"]}.items():
			self.glist.append(Bar(key, value))

	def click(self, pos):
		for x in self.blist:
			exec(x.click(pos))
				
		for x in self.flist:
			exec(x.click(pos))

		for x in self.glist:
			exec(x.click(pos))
				
				

	def draw(self, display):
		display.blit(self.btext, (143, 75))
		display.blit(self.ftext, (148, 230))
		display.blit(self.ptext, (135, 555))
		for x in self.blist:
			x.draw(display)
		for x in self.flist:
			x.draw(display)
		for x in self.glist:
			x.draw(display)



class Bar:
	
	def __init__(self, name, value):
		self.id = Bar.idd
		Bar.offs=Bar.offs + 30 if self.id % 4==0 else Bar.offs
		self.name = name		
		self.max = 1
		self.min = 0
		self.cur = 0.5
		self.pointer = value[1]
		self.org = value[0]		
		self.val = value[0] * (self.cur/0.5)		
		self.pos = (15 , 80 + 30 * self.id + Bar.offs)				
		self.config_anm()		
		self.rect = Rect(self.pos[0], self.pos[1], self.total, 16)
		self.mult=1 if self.id in [8, 9, 10] else 10
		self.update_text()
		Bar.idd += 1

	def update_text(self):
		self.nametext = tx.new_text(Setting.fonts, 'calibri_10', self.name, (127, 118, 200))
		self.valtext = tx.new_text(Setting.fonts, 'calibri_10', ('{:.2f}').format(self.val*self.mult), (127, 118, 200))

	def config_anm(self):
		self.total = 318
		self.bpos = self.total * self.cur + 7

	def __str__(self):
		return ('{} \n {} ---{}--- {} val: {} \n'.format(self.name, self.min, self.cur, self.max, self.val))

	def click(self, pos):
		if Rect.collidepoint(self.rect, pos):
			x= pos[0] -15 
			self.cur= x/self.total
			self.val = self.org * (self.cur/0.5)
			self.config_anm()
			self.update_text()
			return("{} = {:.3f}".format(self.pointer, self.val))
		return 'False'



	def draw(self, display):
		display.blit(self.nametext, (self.pos[0], self.pos[1] - 10))
		display.blit(self.valtext, (self.pos[0]+ 150, self.pos[1] - 10))
		display.blit(Setting.spr['slide'], self.pos)
		display.blit(Setting.spr['ball'], (self.bpos, self.pos[1]))



