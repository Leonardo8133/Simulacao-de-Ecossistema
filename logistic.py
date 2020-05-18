#Logistic Regression
from pandas import read_csv
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
import pickle as pc

def load_model():	
	db = read_csv("data/decision_data.csv")
	X = db[["Hungry", "Thrist", "Love", "Rest"]]/100
	y = db[["Decision"]]
	X = np.array(X)
	y = np.array(y).reshape(-1,)

	print(X)
	print(y)


	model = LogisticRegression()
	model.fit(X,y)
	print(model.predict_proba([[0.1,0.1,0.3,0.2]]))

	megafile = open("logs.pkl", "wb")
	pc.dump(model, megafile)

load_model()