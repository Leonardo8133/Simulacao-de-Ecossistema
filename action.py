from numpy import random
from hud import HUD
from copy import copy
import neat

class Action:
	def eat(self):
		check, ids = self.box_search("food")
		if check:
			x, y = check
			if Action.data['obj'][self.cord[0] + x][self.cord[1] + y]==7:
				Action.data['obj'][self.cord[0] + x][self.cord[1] + y]=2 #<<<<< change for 2
				Action.update=True
				self.genome.fitness += (self.needs['hungry'][0]/self.needs['hungry'][1]-0.65)*20
				self.eat_counter+=1
				return True
		return False

	def drink(self):
		check, ids = self.box_search("water")
		if check:
			x, y= check
			if Action.data['map'][self.cord[0] + x][self.cord[1] + y]==2:
				
				return True
		return False

	def love(self):
		check, ids = self.box_search("love")
		if check:
			x, y = check
			if Action.data['ent'][self.cord[0] + x][self.cord[1] + y][0]:
				for i, n in enumerate(Action.ent_list):
					if n.id==ids:
						self.upqueue.append(["set_love", ids])
						self.current=['empty']
						self.queue=[]
						self.love_counter+=1
						
						return True
		return False

	def hunt(self):
		check, ids = self.box_search("hunt", True)
		if check:
			x, y = check
			if Action.data['ent'][self.cord[0] + x][self.cord[1] + y][0]:
				for i, n in enumerate(Action.ent_list):
					if n.id==ids and n.specie!='fox':
						del(Action.ent_list[i])
						Action.sdraw=True
						self.score+=20
						self.genome.fitness += (self.needs['hungry'][0]/self.needs['hungry'][1]-0.5)*35	
						self.data['ent'][n.cord[0]][n.cord[1]].remove(n.id)
						HUD.bdraw=True
						self.queue=[]
						HUD.deadt[n.specie].append(("hunt", n.specie, n.id, n.cord, n.score))
						HUD.print("{} Id {}, died from {}". format(n.name, n.id, 'Hunted'))
						self.eat_counter+=1
						return True
		return False		

	def walk(self,xy):	
		x, y = xy
		self.queue.append(('walk', x, y))
		
	def reproduce(self):
		self.b_counter=300
		self.birth=True

	def give_birth(self, game):
		#print(f"{self.name} Borned")
		gene = {'inf': self.inf, 'inc': self.inc, 'base': self.base}
		game.add_entitie(self.name, self.cord, gene)		
		for x in range(Action.database[self.specie]['inf']['maxchild']):
			if random.randint(100)<40:
				game.add_entitie(self.name, self.cord, gene)
		self.birth=False
		HUD.print("A {}, id : {}, given birth.".format(self.name, self.id ))

	
	def ident_run(self, pos=False):
		ident=[]
		vw = self.inf['view']
		slcx, slcy = self.get_slice(vw)	
		for row_nb, row in enumerate(Action.data['ent'][slcx[0]:slcx[1]+1]):
			for col_nb, tile in enumerate(row[slcy[0]:slcy[1]+1]):
				if tile:
					for x in tile:
						if x != self.id:
							for y in Action.ent_list:
								if y.id == x and y.specie=='fox':
									ident.append(y.cord)
		if ident:
			self.upqueue.append(['run', ident])
			return True
		return False
			
	def meds(self, di):
			c1, c2 = (0, 0)
			for x in di:
				c1+=x[0]
				c2+=x[1]
			return [int(c1/len(di))*-1 + self.cord[0],int(c2/len(di))*-1 + self.cord[1]]

	def path_run(self, ident):			
		av = self.meds([self.diff(x, self.cord) for x in ident])
		# print("sv: ", av)
		self.queue=[]
		if self.path(self, av):
			return True
		for x in range(4): 
			# print("looking for tile to flee")
			if self.path(self, (av[0] + random.randint(-4-x,4+x), random.randint(-4-x,4+x))):
				return
		self.rand_path(self)	


	def search_for(self, typ):
		if   typ == 'food':
			return self.search_resource('obj', 7, 'food')
		elif typ == "water":
			return self.search_resource('map', 2, "water")
		elif typ == "love":
			return self.search_love()
		elif typ == "hunt":
			return self.search_hunt()
		return False

	def search_resource(self, typ, num, res):
		clist = [] # coordinates list
		slcx, slcy = self.get_slice(self.inf['view'])
		for row_nb, row in enumerate(Action.data[typ][slcx[0]:slcx[1]+1]):
				for col_nb, tile in enumerate(row[slcy[0]:slcy[1]+1]):
					if tile==num:
							clist+=self.box_search_sliced('map', self.walkeable, (row_nb, col_nb), slcx[0], slcy[0])
		if clist:
			val, ind = self.get_min([self.calc_dist(self.cord, m) for m in clist]) # Get Min Distance in cord list
			if res == "food":
				if self.path(self, clist[ind]):
					self.queue.append(['cmd', 'self.eat()', 'eat'])
				else:
					if clist[ind] not in self.lasterror:
						self.lasterror.append(clist[ind])
			elif res == "water":
				if self.path(self, clist[ind]):				
					self.queue.append(['cmd', 'self.drink()', 'drink'])
				else:
					if clist[ind] not in self.lasterror:
						self.lasterror.append(clist[ind])
			self.read_queue()
			return True
		return False

	def search_hunt(self):
		clist = [] # coordinates list
		slcx, slcy = self.get_slice(self.inf['view'])
		for row_nb, row in enumerate(Action.data['ent'][slcx[0]:slcx[1]+1]):
				for col_nb, tile in enumerate(row[slcy[0]:slcy[1]+1]):
					if tile:
						if self.id not in tile:
							for x in Action.ent_list:
								if x.id in tile and x.specie!='fox':
									clist+=self.box_search_sliced('map', self.walkeable, (row_nb, col_nb), slcx[0], slcy[0], 'hunt')
		if clist:
			val, ind = self.get_min([self.calc_dist(self.cord, m) for m in clist]) # Get Min Distance in cord list
			if self.path(self, clist[ind], True):
					self.queue.append(['cmd', 'self.hunt()', 'hunt'])	
			self.read_queue()
			return True
		return False

	def search_love(self):
		clist = [] # coordinates list
		elist =[]
		v1=[]
		slcx, slcy = self.get_slice(self.inf['view'])
		for row_nb, row in enumerate(Action.data['ent'][slcx[0]:slcx[1]+1]):
				for col_nb, tile in enumerate(row[slcy[0]:slcy[1]+1]):
					if tile and self.id not in tile:						
						for x in Action.ent_list:
							if x.id in tile and x.inf['gender']!=self.inf['gender'] and x.inf['age']>=12 and x.specie==self.specie and x.lovedelay<5 and self.lovedelay<5:
								clist+=self.box_search_sliced('map', self.walkeable, (row_nb, col_nb), slcx[0], slcy[0], 'love')
								elist+=self.box_search_sliced('map', self.walkeable, (row_nb, col_nb), slcx[0], slcy[0], 'hunt')
								v1.append(x.id)
						
		if clist:
			try:
				val, ind = self.get_min([self.calc_dist(self.cord, m) for m in clist])
				val2, ind2 = self.get_min([self.calc_dist(self.cord, m) for m in elist]) # Get Min Distance in cord list
				v1 = Action.data['ent'][elist[ind2][0]][elist[ind2][1]][0]
				if self.path(self, clist[ind]):
					self.upqueue.append(['set_wait', v1])
					self.queue.append(['cmd', 'self.love()', 'love'])
				self.read_queue()
				return True
			except:
				return False
		return False




	# def search_for(self, res, num=0, spos=False):
	# 	try:
			
	# 		elif res=="love":
	# 			typ="ent"
	# 			num=1
	# 		may=list()
	# 		bay=list()
	# 		vw = self.inf['view']
	# 		slcx, slcy = self.get_slice(vw, spos)	
	# 		for row_nb, row in enumerate(Action.data[typ][slcx[0]:slcx[1]+1]):
	# 			for col_nb, tile in enumerate(row[slcy[0]:slcy[1]+1]):
	# 				if res=="love" or res=="hunt":
	# 					if tile:
	# 						if tile[0]!=self.id:								
	# 								for x in Action.ent_list:
	# 									if x.id==tile[0]:
	# 										if x.specie==self.specie:
	# 											may = may + self.box_search_sliced('map', self.walkeable, (row_nb, col_nb), slcx[0], slcy[0], res)
	# 											bay = bay + self.box_search_sliced('map', self.walkeable, (row_nb, col_nb), slcx[0], slcy[0], "hunt")
	# 											bele = tile[0]								
	# 		if spos and len(may)>0:
	# 			return True
	# 		if len(may)>0:			
	# 			ney = list()
	# 			for m in may:
	# 				ney.append(self.calc_dist(self.cord, m))				
	# 			blk=list()
	# 			for m in bay:
	# 				blk.append(self.calc_dist(self.cord, m))
	# 			val, ind = self.get_min(ney)
	# 			val2, ind2 = self.get_min(blk)
				
	# 			if res == "food" and self.path(self, may[ind]):
	# 				self.queue.append(['cmd', 'self.eat()', 'eat'])
	# 			elif res == "water" and self.path(self, may[ind]):				
	# 				self.queue.append(['cmd', 'self.drink()', 'drink'])	
	# 			elif res=="hunt":
	# 				nid = Action.data['ent'][may[0][0]][may[0][1]][0]
	# 				for x in Action.ent_list:
	# 					if x.id==nid:
	# 						if x.specie.lower()!='fox' and self.path(self, may[ind], True):
	# 							self.queue.append(['cmd', 'self.hunt()', 'hunt'])	
	# 			self.read_queue()
	# 			return True
	# 	except:
	# 		return False	