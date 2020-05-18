def box_draw(self,game,cam): #Not being used
		for y in range(-1,2,1):
			for x in range(-1,2,1):
				row_nb=self.cord[0]+y
				col_nb=self.cord[1]+x
				cord_x=game.cord_map[row_nb][col_nb][0]+cam.x
				cord_y=game.cord_map[row_nb][col_nb][1]+cam.y
				if cord_x>-64 and cord_x<1032 and cord_y>-128 and cord_y<632:
					game.DISPLAYSURF.blit(game.spr[game.data["map"][row_nb][col_nb]],(cord_x,cord_y))
		for y in range(-3,4,1):
			for x in range(-3,4,1):				
				row_nb=self.cord[0]+y
				col_nb=self.cord[1]+x
				obj_id=int(game.obj_map[row_nb][col_nb])
				cord_x=game.cord_map[row_nb][col_nb][0]+cam.x
				cord_y=game.cord_map[row_nb][col_nb][1]+cam.y
				if obj_id>=0:
					game.DISPLAYSURF.blit(game.obj[obj_id],(cord_x, cord_y))
		