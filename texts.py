#text database#
import pygame.font

def load_font():
	pygame.font.init()
	
	fonts={"arial" :      pygame.font.SysFont('Arial Rounded', 20),
		   "calibri_15" : pygame.font.SysFont('Calibri', 14),
		   "calibri_12" : pygame.font.SysFont('Calibri', 14),
		   "calibri_10" : pygame.font.SysFont('Calibri', 12),
		   "calibri_8" :  pygame.font.SysFont('Calibri', 11)}
	return  fonts

def new_text(fonts, font, text, color=(255,255,255), italic=False):
	return fonts[str(font)].render(str(text), italic, color)

def load_text(self):
	pygame.font.init()
	fonts={"arial" : pygame.font.SysFont('Arial Rounded', 20),
		   "calibri_15" : pygame.font.SysFont('Calibri', 12)}		  
	db={
	"cords" : fonts['arial'].render(str(tuple(self.cam.cord)), False, (63, 63, 100)),
	"fps" : fonts['arial'].render(str(int(self.nfps)), False, (255, 255, 255)),
	"ent_num" : fonts['arial'].render("Entities: {}".format((len(self.ent_list))), False, (255, 255, 255))}
	return db, fonts

def update_text(self):
	try:
		self.db={
		"cords" : self.fonts['arial'].render(str(self.cam.cord), False, (63, 63, 100)),
		"fps" : self.fonts['arial'].render(str(int(self.FPSCLOCK.get_fps())), False, (255, 255, 255)),
		"ent_num" : self.fonts['arial'].render("Entities: {}".format((len(self.ent_list))), False, (255, 255, 255))}
	except:
		pass