import time
class bullet_class:
	b_id=0 # class variable, 
	def __init__(self, current_pos): #current its a list with current [xcord, ycord]
		# WARNING -- Dont name /\ (current_pos parameter) as current, because current is already a variable outside loop
		self.id= bullet_class.b_id # Identity variable to each bullet
		bullet_class.b_id += 1 #Next bullet will have id = id + 1


		self.current = current_pos # current[0] = xcord // current[1]= ycord

		

		self.counter = 0
		self.posx=0 #set bullet direction to 0
		self.poxy=0 #set bullet direction to 0
		self.check_side() #check what direction bullet will have
		

	def check_side(self):
		if right:
			self.posx=1
			self.posy=0
		if left:
			self.posx=-1
			self.posy=0
		if up:
			self.posx=0
			self.posy=-1
		if down:
			self.posx=0
			self.posy=1
		#now, bullet have a direction 

	def update(self): #function that will be called inside game loop to update bullet
		self.update_postion() 
		self.update_counter()

	def update_counter(self):
		self.counter= self.counter + 1

	def update_postion(self):
		#update bullet position
		self.current[0] = self.current[0] + self.posx 
		self.current[1] = self.current[1] + self.posy 

	def print_bullet(self):
		print("Current", self.current, "Id ", self.id)
		print("Counter", self.counter)



bullet_list=[] #list with all player bullets

current = [100, 125] #player current cords [xcord, ycord]

right=True
left=False
up=False
down=False
def shot(current):
	if len(bullet_list)<10:
		dely=100
		bullet_list.append(bullet_class(current.copy())) #\/
		#                           REMEMBER: doing self.current = current in class, makes those variables point to the same place in memory, so, when we change self.current, current will change also, because they are the same ( you can test it by doing print(self.current=current))




x=0
while x<10: ## main loop ( I limited in 10 loops )
	x=x+1
	time.sleep(1)
	##player pressed space####
	
	shot(current) #call shot sending current position
	for bullet in bullet_list[:-1]: #for each bullet in bullet list [:-1] makes "for" read list backwards (just to looks nice in print) 
		bullet.update()
		bullet.print_bullet()

	print("---------------\nNext Frame\n\n")

