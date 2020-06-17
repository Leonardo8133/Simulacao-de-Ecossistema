from sklearn.datasets import load_digits
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


digits = load_digits()
print(digits.data.shape)
print(digits.target.shape)

x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.4, random_state=0)

logis= LogisticRegression().fit(x_train,y_train)

plt.figure(figsize=(40,8))
for x in range(6):
    plt.subplot(6, 1, x+1)
    plt.imshow(np.reshape(x_test[x], (8,8)), cmap=plt.cm.gray)
    pred=logis.predict(x_test[x].reshape(1,-1))
    plt.title(pred, fontsize = 20)
