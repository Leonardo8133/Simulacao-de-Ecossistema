import noise as noise
import numpy as np
import matplotlib.pyplot as plt
#import sys


blue = [65,105,225]
green = [34,139,34]
dark = [20,120,20]
sand = [238,214,175]

def generate_terrain(shape,scale,octaves=1,persistence=0.5, seed=np.random.randint(10000000)):
	ot = np.random.randint(seed*2)
	np.random.seed()
	world = np.zeros(shape)
	world= noise.generate_bnoise(shape,scale,octaves,persistence)
	output=world
	path=np.zeros(shape)
	new_world = np.zeros(world.shape+(3,))
	amb_world = np.zeros(world.shape)
	for i in range(shape[0]):
	    for j in range(shape[1]):
	        new_world[i][j]=setcolor(i,j, world)
	        path[i][j]=setcolor(i,j,world,"path")
	        output[i][j]=setcolor(i,j, world, "out")
	        
	output=output.astype(int)
	new_world=new_world*(1/255)
	amb_noise=noise.generate_bnoise(shape,(1,1),6,0.7)
	amb_world=generate_ambient(world,amb_noise,shape)
	path = get_path(path, amb_world)
	# fig=plt.figure(figsize=(8, 4))	
	# # fig.add_subplot(1, 2, 2)
	# # plt.imshow(output)
	# fig.add_subplot(1, 2, 1)
	# plt.imshow(path)
	# plt.show()	
	# print(output)
	np.random.seed(ot)
	return output, amb_world, new_world, path, seed


def get_path(path, amb_world):
	for i in range(len(path[0])):
	    for j in range(len(path)):
	    	if amb_world[i][j]!=-1:
	    		path[i][j]=0

	return path

def generate_ambient(world, amb_noise,shape):
	amb= ((amb_noise+0.6)**1)# 1.5 - 0
	temp_world=np.zeros(world.shape) - 1 
	
	for i in range(shape[0]):
	    for j in range(shape[1]):
	    	temp_world[i][j]=place_objects(world,'tree',i,j,amb,temp_world[i][j])
	    	temp_world[i][j]=place_objects(world,'brush',i,j,amb,temp_world[i][j])
	# plt.imshow(temp_world)
	# plt.show()
	#plt.show()
	return temp_world
	
def place_objects(world,obj,i,j,amb,cur):
	cc=world[i][j]
	if obj=='tree':
		if amb[i][j]>=0.25:
			if cc==4 or cc==0:
				if np.random.randint(0,100)<5:					
					return np.random.randint(0,2)	#0 a 1	

		return -1
	if obj=='brush':
		if amb[i][j]>=0.15:
			if cc==4 or cc==0:
				if cur==-1:
					if np.random.randint(0,100)<14:
						return 2	
				return cur
		return -1

def setcolor(i,j, world, en="color"):
    val = world[i][j]
    temp=dark
    walk=1
    output=4
    if val<-0.15: 
      temp=blue
      output=2 
      walk=0
    elif val<-0.05:
      temp=sand
      output=3
      walk=1
    elif val<0.25:
      temp=green
      output=0
      walk=1
    elif val<0.6:
      temp=dark
      output=4
      walk=1
    if en=="color":
    	return np.array(temp)
    elif en=="out":
    	return output
    elif en=="path":
    	return walk

#generate_terrain((128,128), (4, 4), 5)
