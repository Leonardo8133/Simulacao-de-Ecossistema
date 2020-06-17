#hud

import pygame
import texts as tx
import ha
import entities as en
from sys import exit
from graf import *
from settings import Setting
import time





class HUD:
	def __init__(self, display):
		self.tab = "grf"
		self.ntfpos = (30, 560)
		self.ntf_maxsize= 100
		self.display= display
		self.spr = self.load_sprites()
		self.fonts = tx.load_font()
		self.pos = self.load_elements()
		self.ent_list = []
		self.current_slot = 0
		self.file=False
		self.delete=False
		self.day=0
		for x in range(20):
			strs='data{}.txt'.format(x)
			try:				
				file2 = open(strs, 'r')				
				file2.close()
				# print("Looking for next file: ", x)				
			except:
				self.file=strs
				break
		self.sblue = (127, 118, 200)
		self.white = pygame.Color(117, 115, 128, 100)
		self.orange = pygame.Color(104, 63, 46, 100)
		self.addb=False
		self.grafs= {'pop': Grafs("Total Population"), 'bunny':Grafs("Bunny Population"), 'fox':Grafs("Fox Population")}
		Grafs.data=HUD.wdata
		Grafs.num=0
		Grafs.spr=[self.spr['sht']['graf'], self.spr['sht']['grafzoom'], self.spr['sht']['grafslide']]
		xy, size = self.pos['ent_slots']		
		for x in range(0,6):
			self.pos['rects_pos'].append(pygame.Rect(xy[0], xy[1] + (-5 + xy[1])*x, *size))

	@staticmethod
	def reset():
		HUD.ntf = []
		HUD.fonts = tx.load_font()
		HUD.ntf_maxsize=100
		HUD.bools={'ntf':False, 'grf':False, 'ent':False, 'set':False}
		HUD.update_back=True
		HUD.bdraw=True
		HUD.day=0
		HUD.time= time.time()
		HUD.deadt={'bunny':[], 'fox':[]}
		HUD.lovet={'bunny':[], 'fox':[]}
		HUD.wdata={
			'lpop':{'bunny':[], 'fox':[]},
			'start':{'rates':[], 'ent':[]},
			'pop':{'bunny':[],'fox':[],'total':[]},
			'dead':{'bunny':[], 'fox':[]},
			'love':{'bunny':[],'fox':[],'total':[]},
			'meds':[],
			'base':[]}

	@staticmethod
	def print(text, *args):
		HUD.update_back=True
		try:
			for x in args:
				text=str(text) + " " + str(x)			
			text = HUD.fonts['calibri_15'].render(str(text), False, (63, 63, 113)),
			HUD.ntf.append(text)
			if len(HUD.ntf)==HUD.ntf_maxsize:
				HUD.ntf.pop(0)
				HUD.ntf.pop(1)
		except:
			print('Could not print a text')
		HUD.bools['ntf']=True

	@staticmethod
	def calc(elist, tick, self):
	
		HUD.wdata['pop']['bunny']=[]
		HUD.wdata['pop']['fox']=[]
		med= {"bunny":{'speed': [], 'hungry': [], 'thirst': [], 'love': [], 'rest': []}, "fox":{'speed': [], 'hungry': [], 'thirst': [], 'love': [], 'rest': []}}
		base={"bunny":{'hungry': [], 'thirst': [], 'love': [], 'rest': []}, "fox":{'hungry': [], 'thirst': [], 'love': [], 'rest': []}}
		#fin= {"bunny":{'speed': [], 'hungry': [], 'thirst': [], 'love': [], 'rest': []}, "fox":{'speed': [], 'hungry': [], 'thirst': [], 'love': [], 'rest': []}}
		temp={'bunny':[], 'fox':[]}

		if tick%7200:
			HUD.wdata['dead']['bunny'].append(HUD.deadt['bunny'])
			HUD.wdata['dead']['fox'].append(HUD.deadt['fox'])
			HUD.wdata['love']['bunny'].append(HUD.lovet['bunny'])
			HUD.wdata['love']['fox'].append(HUD.lovet['fox'])
		
		for x in elist:
			HUD.wdata['pop'][x.specie].append((x.specie, x.id, x.cord, x.inf['age'], x.score))
			if tick%1200==0:
				#print("Id : ", x.id, ' Current Cord/Scord: ', x.cord, " ", x.scord)				
				temp[x.specie].append((x.id, x.specie, x.cord.copy(), x.scord, x.inf['age'], x.score))				

			if tick%1200==0:				
				for r in med[x.specie].keys():
					if r=='speed':
						med[x.specie][r].append(round(x.inf[r],3))
					else:
						med[x.specie][r].append(round(x.inc[r],3))

				for r in base[x.specie].keys():
					base[x.specie][r].append(x.base[r])

		if tick%1200==0:
			HUD.day+=1
			print("\nStoring data")
			print("Writing to File....")
			HUD.wdata['lpop']['bunny'].append(temp['bunny'])
			HUD.wdata['lpop']['fox'].append(temp['fox'])	
			HUD.wdata['meds'].append(med)
			HUD.wdata['base'].append(base)
			self.get_datas()
			if self.file == False:
				self.file='last_run.txt'
			file2 = open(self.file, 'w')					
			file2.write(str(HUD.wdata))
			file2.close()					
			print("Stored.\n")
			print("Time Taken", time.time() - HUD.time)
			HUD.time=time.time()
		
		if tick%7200:
			HUD.deadt['bunny']= []
			HUD.deadt['fox']=   []
			HUD.lovet['bunny']= []
			HUD.lovet['fox']=   []

		# if len(elist)==0 or HUD.day==150:
		# 	pygame.quit()
		# 	exit()
		# if tick%1200==0:		
		# 	for t in med.keys():
		# 		for r in med[t].keys():					
		# 			if len(med[t][r]):
		# 				fin[t] = sum(med[t])/len(med[t])	
		# 				HUD.wdata['meds'][t].append([fin[t]])
		# 	for t in base.keys():
		# 		if len(base[t]):
		# 			fin[t] = sum(base[t])/len(base[t])	
		# 			HUD.wdata['base'][t].append([fin[t]])
		# 	# except:
		# 	print("Error in HUD.calc(elist)")


		#------------- Loading Stuff -----------------------#
	def load_sprites(self):
		size_41 = (41, 0, 41, 41, False)
		size_82 = (41, 0, 82, 41, False)
		size_20 = (20, 0, 20, 50, False)
		sizes={
		'tools':(1, 1, 47, 348, False),
		'up_dw':(49, 1, 22, 49, False),
		'round':(72, 1, 63, 70, False),
		'ntf':  (49, 51, 10, 8, False),
		'ent':  (60, 51, 10, 8, False),
		'trash':(137, 34, 31, 27, False),
		'inf':  (192, 24, 77, 94, False),
		'addent':   (49, 75, 31, 53, False),
		'graf':     (81, 72, 101, 28, False, 3),
		'grafzoom': (137, 62, 20, 9, False, 2),
		'grafslide':(158, 62, 20, 9, False, 2),
		'setslide': (66, 129, 186, 9, False, 1.7),
		'setball':  (49, 129, 16, 15, False, 1.2),
		'play':	    (81, 101, 27, 27, False)
		#'arrow':(49, 51, 8, 10)
		}
		sl = ha.SpriteSheet('data/ui_selected.png')
		bt = ha.SpriteSheet('data/buttons.png')
		sh = ha.SpriteSheet('data/colect1.png')
		hd = pygame.image.load('data/UI background.png')
		bx = pygame.image.load('data/box_1.png')
		dd = pygame.image.load('data/dead.png').convert()

		hspr = {
		'tab':[],
		'hud':hd,
		'bx1':bx,
		'ded':dd,
		'bts':[],
		'sht':{}}
		for x in range(2):
			hspr['bts'].append(self.setid(x, bt, size_20))
		for x in range(4):
			hspr['tab'].append(self.setid(x, sl, size_41))

		hspr['tab'].append(self.setid(4, sl, size_82))

		for k, v in sizes.items():
			hspr['sht'][k] = (self.setid(1, sh, v))

		Setting.spr={
			'slide':hspr['sht']['setslide'],
			'ball' :hspr['sht']['setball']}
		return hspr


	def load_elements(self):
		pos = {'tabs' : {
					'ntf' :  [(11, 19), (41 ,41), pygame.Rect(11,19,41,41)],
					'grf' :  [(75, 19), (41, 41), pygame.Rect(75,19,41,41)],
					'ent' :  [(266, 19), (82, 41),pygame.Rect(266,19,82,41)],
					'set' :  [(137, 19), (82, 41),pygame.Rect(137,19,41,41)]},
				'ent_slots': ((20, 90), (315, 75)),
				'graf_slot': ((20, 90)),
				'rects_pos': [],
				'up_dw':{
					'frame': [(352,80),(0,0),   pygame.Rect(0, 0, 0, 0)],
					'ent_up':[(352,80),(20,25), pygame.Rect(352, 80, 20, 25)],
					'ent_down':[(0,0),(0,0),    pygame.Rect(352, 105, 20, 25)]},
				'tools':{
					'frame': [(352,201),(47,348), pygame.Rect(0, 0, 0, 0)],
					'add':   [(0,0),(0,0), pygame.Rect(361, 213, 31, 21), "self.bchange('addb')"],
					'remove':[(0,0),(0,0), pygame.Rect(361, 249, 31, 21), "self.del_state(game)"],
					'chunk': [(0,0),(0,0), pygame.Rect(361, 355, 31, 21), "game.chunk_exec()"],
					'map':   [(0,0),(0,0), pygame.Rect(361, 390, 31, 21), "game.open_map()"]},
				'round':{
					'frame': [(366, 7),(0,0), pygame.Rect(0, 0, 0, 0)],
					'plus':  [(0, 0),(0,0), pygame.Rect(407, 67, 13, 10), "game.change_scale(0.25)"],
					'minus': [(0, 0),(0,0), pygame.Rect(378, 67, 13, 10), "game.change_scale(-0.25)"],
					'south': [(0, 0),(0,0), pygame.Rect(403, 44, 15, 15), "game.addcord(0,1)"],
					'east':  [(0, 0),(0,0), pygame.Rect(403, 21, 15, 15), "game.addcord(1,-1)"],
					'north': [(0, 0),(0,0), pygame.Rect(380, 21, 15, 15), "game.addcord(0,-1)"],
					'west':  [(0, 0),(0,0), pygame.Rect(380, 44, 15, 15), "game.addcord(1,1)"]
				},
				'misc':{
					'play':[(160, 524), pygame.Rect(160, 524, 27, 27), "game.start()"],
					'ntf': [(28, 59)],
					'ent': [(298, 59)],
					'trash':[(400,251)],
					'box_bunny':[False, pygame.Rect(25, 70, 15, 12), "self.bchange('box_bunny')"],
					'box_fox':[False, pygame.Rect(45, 70, 15, 12), "self.bchange('box_fox')"],						
				},
				'addent':{
					'frame':[(400, 250)],
					'bunny':[(0, 0), (0, 0), pygame.Rect(403, 255, 25, 20), "game.add_entitie('bunny')"],
					'fox':[(0, 0), (0, 0), pygame.Rect(403, 282, 25, 20), "game.add_entitie('fox')"]
				}
			}
		return pos
#----------------------------------------------------------------------------------------------------------#
	def get_datas(self):
		HUD.wdata['hist']={"total" : self.grafs["pop"].val, "bunny" : self.grafs["bunny"].val, "fox" : self.grafs["fox"].val}

	def refresh_list(self, lista):
		self.ent_list = lista

	def bchange(self, val):
		if val=='addb':
			self.addb=True if self.addb==False else False
		elif val=='box_bunny':
			self.pos['misc']['box_bunny'][0]=True if self.pos['misc']['box_bunny'][0]==False else False
		elif val=='box_fox':
			self.pos['misc']['box_fox'][0]=True if self.pos['misc']['box_fox'][0]==False else False

#---- Key And Mouse Events -----#
	def key_event(self, event_type, event_key):
		if event_type ==pygame.KEYDOWN:
			if event_key == pygame.K_TAB:
				self.change_tab()

	def mouse_event(self, event_type, event_button, pos, game):
		if event_type == pygame.MOUSEBUTTONDOWN:
			if event_button == 1:
				self.check_click(event_type, event_button, pos, game)


	def check_click(self, event_type, event_button, pos, game):
		if self.tab=='grf':
			for grf in self.grafs.values():
				grf.click(pos)
		if self.tab=='set':
			en.Ent.Sett.click(pos)
		for x, y in self.pos['tabs'].items():
			if pygame.Rect.collidepoint(y[2], pos):
				self.tab=x
				self.bools[x]=False
				HUD.update_back=True
				return

		for k, v in self.pos['round'].items():
			if pygame.Rect.collidepoint(v[2], pos):
				eval(v[3])

		for k, v in self.pos['tools'].items():
			if pygame.Rect.collidepoint(v[2], pos) and v[3]:
				eval(v[3])
				if len(v)==5:
					exec(v[4])

		if self.tab=='ent':
			self.ent_tab(pos, game)

		for x in ["box_bunny","box_fox"]:
			if pygame.Rect.collidepoint(self.pos['misc'][x][1], pos):
				eval(self.pos['misc'][x][2])

		if self.addb:
			for k, v in self.pos['addent'].items():
				if k != 'frame':
					if pygame.Rect.collidepoint(v[2], pos):
						eval(v[3])

		if self.tab=='set' and game.started==False:
			if pygame.Rect.collidepoint(self.pos['misc']['play'][1], pos):
				eval(self.pos['misc']['play'][2])

	
	def del_state(self,game):
		self.delete=True if self.delete==False else False
		HUD.print("Deleting is ", self.delete)
		en.Ent.sdraw=True
# ------------------------------------------------------ #	
	def ent_click(self, display):
		pos = pygame.mouse.get_pos()
		for n, ent in enumerate(self.ent_list[self.current_slot:self.current_slot+6]):
			x, y = self.pos['ent_slots'][0]
			y = y + 85*n
			if pygame.Rect.collidepoint(self.pos['rects_pos'][n],pos):
				display.blit(self.spr['sht']['inf'], (x+320, y))
				display.blit(ent.astxt['speed'], (x+330, y+10))
				display.blit(ent.astxt['hungry'], (x+330, y+25))
				display.blit(ent.astxt['thirst'], (x+330, y+40))
				display.blit(ent.astxt['love'], (x+330, y+55))
				display.blit(ent.astxt['rest'], (x+330, y+70))
				display.blit(ent.astxt['fitness'], (x+330, y+85))


	def ent_tab(self, pos, game):
		try:
			for x, y in enumerate(self.pos['rects_pos'][0:len(self.ent_list)]):
				if pygame.Rect.collidepoint(y,pos):
					if self.delete==False:
						HUD.print("Viewing Ent n ", int(x+1))
						x= x+ self.current_slot
						ex, ey = self.ent_list[x].cord
						cx, cy = tuple(game.cam.cord)
						game.addcord(0 , (ex - cx) * game.scale)
						game.addcord(1 , (ey - cy) * game.scale)
						game.update_text(game)
						game.ent_list[x].get_followed(game)
					else:
						x= x+ self.current_slot
						game.kill(game.ent_list[x], "Removed")
		except:
			HUD.print("Slot Error")
			
		if pygame.Rect.collidepoint(self.pos['up_dw']['ent_up'][2], pos):
			self.current_slot=self.current_slot -3 if self.current_slot > 0 else 0
		if pygame.Rect.collidepoint(self.pos['up_dw']['ent_down'][2], pos):
			if self.current_slot + 6 <=len(self.ent_list) and len(self.ent_list)>6:
				self.current_slot+=3


	def ent_slot_draw(self,display):
		string = "Entities Alive: {}  Showing  {} - {}".format(len(self.ent_list), self.current_slot + 1, self.current_slot + 6)
		qnt = tx.new_text(self.fonts, "calibri_10", string, self.sblue)
		display.blit(qnt, (100, 70))

		# if self.pos['misc']['box_bunny'][0]:
		# 	pygame.draw.rect(display, self.white, self.pos['misc']['box_bunny'][1], width=0)
		# else:
		# 	pygame.draw.rect(display, self.white, self.pos['misc']['box_bunny'][1], 1)
		# if self.pos['misc']['box_fox'][0]:
		# 	pygame.draw.rect(display, self.orange, self.pos['misc']['box_fox'][1], 0)
		# else:
		# 	pygame.draw.rect(display, self.orange, self.pos['misc']['box_fox'][1], 1)
		self.ent_slot_draw_list(display)
	
	def ent_slot_draw_list(self, display):
			for n, ent in enumerate(self.ent_list[self.current_slot:self.current_slot+6]):
				x, y = self.pos['ent_slots'][0]
				y = y + 85*n
									
				
				for v in ent.needs.values():
					a,s,d,f = v[3]
					pc = (v[0]/v[1])
					pygame.draw.rect(display, v[2], (x + a, y + s, int(d*pc), f))
					if HUD.bdraw:				
						display.blit(self.spr['bx1'], (x, y))
						display.blit(ent.astxt['id'], (x + 26, y+3))
						display.blit(ent.astxt['age'], (x + 60, y+23))
						display.blit(ent.astxt['name_10'], (x + 72, y+3))
						display.blit(ent.astxt[str(ent.status)], (x + 214, y+3))
						display.blit(en.Ent.min[int(ent.sprid/2)], (x+ 5, y - 40))
					cord = tx.new_text(self.fonts, "calibri_10", ent.cord, self.sblue)
					display.blit(cord, (x+ 265, y + 58))			
					if ent.death>0:
						self.spr['ded'] = self.spr['ded'].convert()
						self.spr['ded'].set_alpha(int(ent.death*(0.5)))
						display.blit(self.spr['ded'], (x, y))
					#pygame.draw.rect(display, (150, 150, 150), self.pos['rects_pos'][n], 1)

	def change_tab(self):
		if self.tab=='ntf':
			self.tab='grf'
		elif self.tab=='grf':
			self.tab='set'
		elif self.tab=='set':
			self.tab='ent'
		elif self.tab=="ent":
			self.tab='ntf'
		HUD.update_back=True

	def draw(self,display, tdraw, tick, ent_list):
		if tick%300==0 and HUD.started==True:
			#HUD.calc(ent_list, tick, self)
			self.grafs['pop'].update_pop(len(self.ent_list))
			self.grafs['bunny'].update_pop(len(HUD.wdata['pop']['bunny']))
			self.grafs['fox'].update_pop(len(HUD.wdata['pop']['fox']))
		if HUD.started==False:
			HUD.update_back=True
		if tdraw:
			if HUD.update_back==True:
				display.blit(self.spr['hud'], (0, 0))
				HUD.update_back=False
				HUD.bdraw=True
			if self.delete:
				display.blit(self.spr['sht']['trash'],self.pos['misc']['trash'][0])
			#display.blit(self.spr['hud'], (0, 0))
			for k, v in self.spr['sht'].items():
				if k=='up_dw':
					if self.tab=='ent':				
						display.blit(v, self.pos[k]["frame"][0])
				else:
					if k not in ['ntf', 'ent', 'trash', 'inf', 'graf', 'grafzoom', 'grafslide', 'setslide', 'setball', 'play']:
						if k == "addent":
							if self.addb:
								display.blit(v, self.pos[k]["frame"][0])							
						else:
							display.blit(v, self.pos[k]["frame"][0])
			#------------Red/Green Dot--------#
			HUD.bools[self.tab]=False
			for m, n in self.pos['misc'].items():
				if m == 'ent' or m == 'ntf':
					if HUD.bools[m]:
						display.blit(self.spr['sht'][m], n[0])
		#-----------------------------------#
		
			if self.tab == 'ntf':
				self.draw_ntf(display)
				display.blit(self.spr['tab'][0],self.pos['tabs']['ntf'][0])
			if self.tab == 'grf':
				display.blit(self.spr['tab'][1],self.pos['tabs']['grf'][0])
				self.draw_grf(display)
			if self.tab == 'set':
				display.blit(self.spr['tab'][2],self.pos['tabs']['set'][0])
				self.draw_set(display)
		if self.tab == 'ent':
			if tdraw:
				display.blit(self.spr['tab'][4],self.pos['tabs']['ent'][0])
				self.ent_slot_draw(display)
			self.ent_click(display)

	def draw_ntf(self, display):
		for x, txt in enumerate(HUD.ntf[:-30:-1]):
			display.blit(txt[0], (self.ntfpos[0], self.ntfpos[1] -16 * x))

	def draw_grf(self, display):
		for graf in self.grafs.values():
			graf.update_tick()
			graf.draw_pop(display)

	def draw_set(self, display):
		display.blit(self.spr['sht']['play'], self.pos['misc']['play'][0])
		en.Ent.Sett.draw(display)
