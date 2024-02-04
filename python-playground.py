import pandas
from sklearn import linear_model
import matplotlib.pyplot as plt
import scipy
import numpy
import csv
#numpy, matplotlib, pandas, scipy, sklearn

vot = open('predictnumber.xlsx', 'w')

print("hello")

df = pandas.read_csv("data.csv")

X = df[['Weight', 'Volume']] # independent variables: weight and volume
y = df['CO2'] # weight and volume used to predict CO2 - looks at how CO2 changes in relation to weight and volume

""" regr = linear_model.LinearRegression()
regr.fit(X.values, y.values)

#predict the CO2 emission of a car where the weight is 2300kg, and the volume is 1300cm3:
predictedCO2 = regr.predict([[3000, 2300]]) """
""" 
print(predictedCO2) """
plt.plot(X, y)
plt.grid()
plt.show()
