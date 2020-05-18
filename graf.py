from pygame import Rect
import pygame.draw
from pygame import quit
import numpy as np
import texts as tx
from sys import exit

class Grafs:
	num=0
	def __init__(self, name):
		self.tick = 0
		self.name = name
		self.fonts = tx.load_font()
		self.id = Grafs.num
		self.pos = (20, 100 + (105*self.id))
		self.val = []
		self.color = {"red":[230, 40, 40], 'sblue':[127, 118, 200]}
		self.last = 0		
		self.nscale = 0.25
		self.border = 105 + 100*self.id
		self.load_text()
		self.zlevel = 1
		self.zpoints = 90
		self.zinterval = 10
		self.zslide=0
		self.button={'in' :[Rect(self.pos[0]+200, self.pos[1], 20, 20), 'self.zoom(+1)'],
					 'out':[Rect(self.pos[0]+220, self.pos[1], 20, 20), 'self.zoom(-1)'],
					 'left': [Rect(self.pos[0]+250, self.pos[1], 20, 20), 'self.slide(-1)'],
					 'right':[Rect(self.pos[0]+270, self.pos[1], 20, 20), 'self.slide(+1)']
					 }

		Grafs.num += 1

	def load_text(self):
		self.txt = {
		'name': tx.new_text(self.fonts, 'calibri_12', self.name, self.color['sblue']),
		'val':  tx.new_text(self.fonts, 'calibri_8', '-', self.color['sblue'])
		}
	def update_text(self):
		self.txt['min'] = tx.new_text(self.fonts, 'calibri_8', int(self.val[-1]*0.5), self.color['sblue'])
		self.txt['max'] = tx.new_text(self.fonts, 'calibri_8', int(self.val[-1]*1.5), self.color['sblue'])
		self.txt['val'] = tx.new_text(self.fonts, 'calibri_8', self.val[-1], self.color['sblue'])
		self.txt['slc'] = tx.new_text(self.fonts, 'calibri_8', '[{}:{}]'.format(-self.zpoints+self.zslide, self.zslide), self.color['sblue'])

	def update_tick(self):
		self.tick += 1

	def update_pop(self, num):		
		self.val.append(num)
		self.nscale = self.last/70
		self.zinterval = 260/self.zpoints
		self.update_text()
		if self.nscale == 0: self.nscale = 0.25
		# if num<=2:
		# 	quit()
		# 	exit()

	def click(self, pos):
		for bt in self.button.values():
			if Rect.collidepoint(bt[0], pos):
				eval(bt[1])

	def slide(self,num):
		if self.zslide <=0:
			if num<0:
				self.zslide  -=4				
			else:
				self.zslide  +=4
				


		if self.zslide<-len(self.val):
			self.zslide=-len(self.val)
		if self.zslide>=0:
			self.zslide=0

	def zoom(self, num):
		if num<0:
			if self.zpoints<400:
				self.zpoints+=20
			else:
				self.zlevel+=20
				self.zpoints=390
		else:
			if self.zpoints>6:
				self.zpoints-=20
				self.zlevel=1
			else:
				return

	def draw_pop(self, display):
		display.blit(Grafs.spr[0], self.pos)
		display.blit(Grafs.spr[1], (self.pos[0]+200, self.pos[1]))
		display.blit(Grafs.spr[2], (self.pos[0]+250, self.pos[1]))
		pygame.draw.line(display,   self.color['sblue'], (self.pos[0]-7, self.pos[1]+15), (self.pos[0]-7, self.pos[1]+65), 1)
		x, y = self.pos
		y = y + 110		
		if self.zslide==0:
			slc = None
		else:
			slc=self.zslide

		for l, k in enumerate(self.val[(-self.zpoints+self.zslide)*self.zlevel : slc : self.zlevel]):			
			m, n = (x + self.zinterval*l,     y - (self.last)/self.nscale)
			b, v = (x + self.zinterval*(l+1), y - (k)/self.nscale)
			self.last=k
			if n < self.border:	n = self.border
			if n > self.border+72:	n = self.border+72
			if v < self.border:	v = self.border
			if v > self.border+72:	v = self.border+72
			if l:
				pygame.draw.line(display,   self.color['red'], (m,n), (b,v), 1)
				if self.zpoints<100:
					pygame.draw.circle(display, self.color['red'], (b,v), 1.5)
		self.draw_inf(display)

	def draw_inf(self, display):
		try:
			display.blit(self.txt['name'], (self.pos[0]+20, self.pos[1]-15 ))
			display.blit(self.txt['val'],  (self.pos[0]+305, self.pos[1]+35))
			display.blit(self.txt['max'],  (self.pos[0]-10, self.pos[1]+1  ))
			display.blit(self.txt['min'],  (self.pos[0]-10, self.pos[1]+70 ))
			display.blit(self.txt['slc'],  (self.pos[0]+255, self.pos[1]-11 ))
		except:
			pass