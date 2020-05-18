class Inventory:
	def __init__(self):
		self.buttons ={
		'1': Rect(......),
		'2': Rect(......),
		'3': Rect(......),
		'4': Rect(......),
		'5': Rect(......)
		}

		self.states ={
		'1': False,
		'2': False,
		'3': False
		}

	def check_button(self):
		''' checks if mouse clicked in button'''
		for index, rect in self.buttons.items():
			#if mouse colliding button 
				self.states[index]=True

	def draw_inv(self):
		if self.states['1']==True:
			#draw something