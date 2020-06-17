from numpy import array
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from ast import literal_eval
import seaborn as sea
import generate as gn


t=1
def pdc(data):
			return pd.DataFrame.from_dict(data)
class visualizator:
	def __init__(self, maps=[]):
		datafile = open("data_example[data].txt", "r")
		data = datafile.readline()
		datafile.close()
		data = literal_eval(data)
		self.map = maps
		self.seed = data['start']['seed']
		

		

		
		self.pop_map(data)
		self.population(data)
		self.death_map(data)
		self.meds(data)
		self.agescore(data)
		self.ageday(data)
		self.bases(data)

	def bases(self, data):
		
		pc = {'hungry':[], 'thirst':[], 'love':[], 'rest':[]}
		bc = pdc(data['base'])['bunny']
		for y, x in enumerate(bc):
			for k in x.keys():
				pc[k].append(sum(x[k])/len(x[k]))
				bc[y][k] = sum(x[k])/len(x[k])
		
		hdb, ddb, ldb, rdb = zip(pc.values())
		fig, (ax, ay)=  plt.subplots(2, figsize=(10,7))
		ax.plot(hdb[0], 'k-', color="green", label='hungry')
		ax.plot(ddb[0], 'k', color="blue", label='thirst')
		ax.plot(ldb[0], 'k', color="cyan", label='love')
		ax.plot(rdb[0], 'k', color="red", label='rest')
		ax.set_xlabel('Time', x=0.9, labelpad=-10)
		ax.set_ylabel('Meds')
		ax.legend()
		ax.grid()
		ax.set_title("Median Genes")

		pc = {'hungry':[], 'thirst':[], 'love':[], 'rest':[]}
		bc = pdc(data['base'])['fox']
		for y, x in enumerate(bc):
			for k in x.keys():
				pc[k].append(sum(x[k])/len(x[k]))
				bc[y][k] = sum(x[k])/len(x[k])
		
		hdb, ddb, ldb, rdb = zip(pc.values())
		ay.plot(hdb[0], 'k-', color="green", label='hungry')
		ay.plot(ddb[0], 'k', color="blue", label='thirst')
		ay.plot(ldb[0], 'k', color="cyan", label='love')
		ay.plot(rdb[0], 'k', color="red", label='rest')
		ay.set_xlabel('Time')
		ay.set_ylabel('Meds')
		ay.legend()
		ay.grid()
		ay.set_title("Median Genes")
		plt.show()

	def ageday(self, data):
		fig, (ax, ay)=  plt.subplots(2, figsize=(9,8))
		self.dayscore(data, ay)
		lista = [pdc(x) for x in data['lpop']['bunny']]
		flista= [pdc(x) for x in data['lpop']['fox']]
		for x, y in enumerate(lista):
			if y.empty:
				flista[x]= (0) 
			else:	
				y.columns = ["Id", "Species", "Cord", "StartCord", "Age", "Score"]
				lista[x] = (y.sum(axis=0)['Age']/len(y["Age"]))
		for x, y in enumerate(flista):
			if y.empty:
				flista[x]= (0) 
			else:
				y.columns = ["Id", "Species", "Cord", "StartCord", "Age", "Score"]
				flista[x] = (y.sum(axis=0)['Age']/len(y["Age"]))

		ax.plot(lista, color='g', linewidth=5, label="Bunny")
		ax.plot(flista, color='r', linewidth=5, label="Fox")
		ax.set_title("Age Mean / Day")
		ax.set_xlabel("Day", labelpad=-10)
		ax.set_ylabel("Age Mean()")
		ax.legend()
		plt.show()
		
	def dayscore(self, data, ay):		
		lista = [pdc(x) for x in data['lpop']['bunny']]
		flista= [pdc(x) for x in data['lpop']['fox']]
		for x, y in enumerate(lista):
			if y.empty:
				flista[x]= (0) 
			else:
				y.columns = ["Id", "Species", "Cord", "StartCord", "Age", "Score"]
				lista[x] = (y.sum(axis=0)['Score']/len(y["Score"]))
		for x, y in enumerate(flista):
			if y.empty:
				flista[x]= (0) 
			else:
				y.columns = ["Id", "Species", "Cord", "StartCord", "Age", "Score"]
				flista[x] = (y.sum(axis=0)['Score']/len(y["Score"]))
		
		ay.plot(lista, color='g', linewidth=5, label="Bunny")
		ay.plot(flista, color='r', linewidth=5, label="Fox")
		ay.set_title("Score Mean / Day")
		ay.set_xlabel("Day")
		ay.set_ylabel("Score Mean()")
		ay.legend()
		
	def agescore(self, data):	#update to Bunny/fox in same plot
		lines = []
		print(data.keys())
		lpd = pd.DataFrame.from_dict(data['lpop']['bunny'])
		for x in data['lpop']['bunny']:
			b =  pd.DataFrame.from_dict(x)
			b.columns = ["Id", "Species", "Cord", "StartCord", "Age", "Score"]
			lines.append(b)
		for x, y  in enumerate(lines):
			lines[x] =  y.drop(columns = ['Id']).groupby('Age').mean()
			
		fig, ax=  plt.subplots(figsize=(10,5))

		def animate(i):
			ax.clear()
			lines[i].plot( kind='bar', ax=ax, colormap="tab20")
			plt.xlabel('Day {} - Age'.format(i))
			plt.ylabel('Score')
			plt.title('Age/Score')
		ani = FuncAnimation(fig, animate, frames=len(lines), interval=900) 
		plt.show()
		
	def pop_map(self, data):
		MAP_DATA, OBJ_DATA, NEW_DATA, PATH, _ = gn.generate_terrain((128, 128), (4, 4), 5, seed= self.seed)
		fig, ax=  plt.subplots(figsize=(10, 10))
		bdb = {}
		fdb = {}
		lp = []
		fp = []
		for k, v in enumerate(data['lpop']['bunny']):
			if v:
				bdb[k] = (pd.DataFrame.from_dict(v))
				bdb[k] = bdb[k][2]
				x, y =	zip(*bdb[k])
				lp.append([x,y])
		for k, v in enumerate(data['lpop']['fox']):
			if v:
				fdb[k] = (pd.DataFrame.from_dict(v))
				fdb[k] = fdb[k][2]
				x, y =	zip(*fdb[k])
				fp.append([x,y])
			
		def animate(i):
			ax.clear()
			ax.imshow(NEW_DATA)
			if i< len(lp):
				ax.scatter(lp[i][1], lp[i][0], s=10, color='red', label="Bunny")
			if i< len(fp):
				ax.scatter(fp[i][1], fp[i][0], s=10, color='black', label="Fox")
			ax.legend()
			plt.xlabel('Day {}'.format(i))
			plt.ylabel('Postion')
			plt.title(f'Population Map Day [{i} , {len(lp)}]')
			
			
		ani = FuncAnimation(fig, animate, frames=len(lp), interval=800) 
		plt.show()
		

	def population(self, data):
		hdb = pd.DataFrame.from_dict(data['hist'])[:400]
		ax = hdb.plot.area(stacked=False, title="Population/Time").set_ylabel("Population")
		plt.show()

	
	def meds(self, data):
		pc = {'speed':[], 'hungry':[], 'thirst':[], 'love':[], 'rest':[]}
		bc = pdc(data['meds'])['bunny']
		for y, x in enumerate(bc):
			for k in x.keys():
				if x[k]:
					pc[k].append(sum(x[k])/len(x[k]))
					bc[y][k] = sum(x[k])/len(x[k])
		
		sdb, hdb, ddb, ldb, rdb = zip(pc.values())
		fig, (ax, ay)=  plt.subplots(2, figsize=(10,5))
		ind = ['speed', 'hungry', 'thirst', 'love', 'rest']
		ax.plot(sdb[0], 'r--', color="purple", label='speed')
		ax.plot(hdb[0], 'k-', color="green", label='hungry')
		ax.plot(ddb[0], 'k', color="blue", label='thirst')
		ax.plot(ldb[0], 'k', color="cyan", label='love')
		ax.plot(rdb[0], 'k', color="red", label='rest')
		#ax.scatter(len(sdb[0])-1, sdb[0], s=10, color="purple")
		ax.set_xlabel('Time', x=0.8)
		ax.set_ylabel('Meds')
		#ax.set_ylim(top=1.25, bottom=0.75)
		ax.legend()  # Add a legend.
		ax.grid()
		ax.set_title("Bunny Median Genes")

		pc = {'speed':[], 'hungry':[], 'thirst':[], 'love':[], 'rest':[]}
		bc = pdc(data['meds'])['fox']
		for y, x in enumerate(bc):
			for k in x.keys():
				if x[k]:
					pc[k].append(sum(x[k])/len(x[k]))
					bc[y][k] = sum(x[k])/len(x[k])
		
		sdb, hdb, ddb, ldb, rdb = zip(pc.values())
		
		ay.plot(sdb[0], 'r--', color="purple", label='speed')
		ay.plot(hdb[0], 'k-', color="green", label='hungry')
		ay.plot(ddb[0], 'k', color="blue", label='thirst')
		ay.plot(ldb[0], 'k', color="cyan", label='love')
		ay.plot(rdb[0], 'k', color="red", label='rest')
			#ax.scatter(len(sdb[0])-1, sdb[0], s=10, color="purple")
		ay.set_xlabel('Time')
		ay.set_ylabel('Meds')
			#ax.set_ylim(top=1.25, bottom=0.75)
		ay.legend()  # Add a legend.
		ay.grid()
		ay.set_title("Fox Median Genes")
		plt.show()	


	def death_map(self, data):
	
		ab=[]
		af=[]
		for x in data["dead"]['bunny']:
			for y in x:
				ab.append(y)
		for x in data["dead"]['fox']:
			for y in x:
				ab.append(y)
		dead_df =  pd.DataFrame.from_dict(ab)		
		dead_df.columns = ["Reason", "Specie", "Id", "Cord", "Score"]
		datas=dead_df
		MAP_DATA, OBJ_DATA, NEW_DATA, PATH, _ = gn.generate_terrain((128, 128), (4, 4), 5, seed = self.seed)
		ddb = datas
		fg, (asx) = plt.subplots(1, 2)

		self.bunny_deaths(datas, asx[1])
		
		self.fox_deaths(datas, asx[0])
		ddb.index = ddb["Reason"]
		mn =  ddb.groupby(ddb.index)
		ddb = {}
		for key, item in mn:
			ddb[key] = mn.get_group(key)
		   # print(mn.get_group(key), "\n\n")
		NEW_DATA = NEW_DATA+(0.3,0.3,0.3)
		
		fig, ax = plt.subplots()
		ax.imshow(NEW_DATA)
		try:
			x, y = zip(*ddb['hungry']["Cord"].tolist())
			ax.scatter(y, x, s=10, color='r', label="Hungry")
		except:
			pass
		try:
			x, y = zip(*ddb['hunt']["Cord"].tolist())
			ax.scatter(y, x, s=10, color='black', label="Hunt")
		except:
			pass
		try:
			x, y = zip(*ddb['thirst']["Cord"].tolist())
			ax.scatter(y, x, s=10, color='b', label="Thirst")
		except:
			pass
		try:
			x, y = zip(*ddb['rest']["Cord"].tolist())
			ax.scatter(y, x, s=10, color='orange', label="Rest")
		except:
			pass
		ax.set_title("Total Deaths")
		ax.legend()
		plt.show()
		
		

	def bunny_deaths(self, dead_df, ax1):

		bdf = dead_df[dead_df['Specie']=='bunny']
		ndata = bdf.groupby('Reason')['Reason'].size()
		rank = ndata.argsort().argsort()
		pal = sea.color_palette("Reds_r", len(ndata))
		fg = sea.barplot(ndata.index, ndata, palette=array(pal[::-1])[rank], ax=ax1)
		fg.set_title("Bunny Deaths from:")
		

	def fox_deaths(self, dead_df, ax2):
		try:
			bdf = dead_df[dead_df['Specie']=='fox']
			ndata = bdf.groupby('Reason')['Reason'].size()
			rank = ndata.argsort().argsort()
			pal = sea.color_palette("Reds_r", len(ndata))
			ng = sea.barplot(ndata.index, ndata, palette=array(pal[::-1])[rank], ax=ax2)
			ng.set_title("Fox Deaths from:")
		except:
			print("[Fox_deaths] Something goes wrong")


	# fig=plt.figure(figsize=(8, 4))	
	# # fig.add_subplot(1, 2, 2)
	# # plt.imshow(output)
	# fig.add_subplot(1, 2, 1)
	# plt.imshow(path)
	# plt.show()	
# 	# print(output)

if t:
	vs = visualizator()