from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.best_first import BestFirst
import entities as ent
import numpy as np

finder = BestFirst(diagonal_movement=DiagonalMovement.never)
def sub(a,b):
	n=a[0]-b[0]
	c=a[1]-b[1]
	nc=(n,c)
	return nc


def set_path(self, dest, maxi=False):
	if dest in self.lasterror:
		return
	try:
		slicex, slicey = get_slice(self)
		dx, dy = dest
		sx, sy =  tuple(self.cord)
		sx = sx - slicex[0]
		sy = sy - slicey[0]
		dx = dx - slicex[0]
		dy = dy - slicey[0]
		map = self.data['path'].transpose()
		grid = Grid(matrix=map[slicey[0]:slicey[1], slicex[0]:slicex[1]])		
		start = grid.node(sx,sy)	
		end = grid.node(dx, dy)
	except:

		# print("error seeking for path")
		#print("Cord: {} Dest: {}".format(self.cord, dest))
		if dest not in self.lasterror:
			self.lasterror.append(dest)
		return
	
	path, runs = finder.find_path(start, end, grid)
	# a= np.array(grid.grid_str(path=path, start=start, end=end))
	for num, p in enumerate(path):
		if num<len(path)-1:			
			self.walk(sub(path[num+1],path[num]))
			if self.specie=='bunny' and num==5:
				self.queue.append(['cmd', 'self.lookrun()', 'look'])
			if maxi==True:
				if num ==2:	self.queue.append(['cmd', 'self.hunt()', 'hunt'])									
				if num >=4:
					self.queue.append(['cmd', 'self.hunt()', 'hunt'])				
					break
			if num==15:
				break
	self.read_queue()
	if path:
		return True	
	return False
	
	

def get_slice(self):
	#print("Slicing")
	size=10
	sx, sy =  tuple(self.cord)
	slicex = [sx-size, sx+size]
	slicey = [sy-size, sy+size]
	slicex[0] = 0 if slicex[0]<0 else slicex[0]
	slicey[0] = 0 if slicey[0]<0 else slicey[0]
	slicex[1] = 127 if slicex[1]>127 else slicex[1]
	slicey[1] = 127 if slicey[1]>127 else slicey[1]
	return slicex, slicey

def random_path(self, size=3, border=False, typ=False):
	#print("Searching for Path\n\n")
	for x in range(4):	
		if border:
			ar = np.random.randint(size*2, size=(2))-size
			if np.abs(ar[0])>size/2 or np.abs(ar[1])>size/2:
				rnd=ar
			else:
				continue
		else:
			rnd = np.random.randint(size*2, size=(2))-size
		dest = (self.cord[0]+rnd[0],self.cord[1]+rnd[1])
		if dest[0]>=0 and dest[1]>=0 and dest[0]<=127 and dest[1]<=127:
			if value_tile(self, dest):
				if border:
					if not self.search_for(typ, 0, dest):
						continue
				self.path(self, dest)
				return
	if border:
		self.rand_path(self, size)
	

def value_tile(self, xy, status="tile"):
	slicex, slicey = get_slice(self)
	x, y = xy
	#print(xy, slicex, slicey)
	if x >= slicex[0] and x<slicex[1]:
		if y>= slicey[0] and y<slicey[1]:
			if status=="tile" or status=="both":
				if self.data['map'][x][y] in [0, 3, 4]:
					if status=="tile":
						#print("Tile Found: ", self.data['map'][x][y])
						return True
					else:
						if self.data['obj'][x][y]==-1:
							return True
	return False


			