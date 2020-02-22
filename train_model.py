# Import required libraries
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import sklearn

#bTEST = True
bTEST = False

if bTEST == True:
	INPUT_DIM = 3 # 45 = 5 Hand Cards + 40 Table Cards
	NUM_OF_CLASSES = 3 # The number of output cathegories. In this example 0,1,2. Zero represents empty spaces.
else:
	INPUT_DIM = 45 # 45 = 5 Hand Cards + 40 Table Cards
	NUM_OF_CLASSES = 11 # The number of output cathegories. In 40 there are only 10 possible categories + zero which is an empty space on the table or hand card

#OUTPUT_DIM = 1 # 1 Next Card
#NUM_EXAMPLES = 10 # Number of examples for testing purposes
#CARDS_MAX = 2 # In cuarenta the max is 10, so we set it to 11

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

# Keras specific
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical 

# load dataset
if bTEST == True:
	dataframe = pd.read_csv("cuarenta.data.old", header=None)
else:
	dataframe = pd.read_csv("cuarenta.data", header=None)

dataset = dataframe.values
X = dataset[:,0:INPUT_DIM]
y = dataset[:,INPUT_DIM]

print("X")
print(X)
print("y")
print(y)

# Encode outputs for classification problems
y = to_categorical(y,NUM_OF_CLASSES)
print("Categorical y")
print(y)
count_classes = y.shape[1] # Bits needed to represent output classes
print("Count Clases: " + str(count_classes))


print("-------------------------------")

# Define Model
model = Sequential()
model.add(Dense(500, activation='relu', input_dim=INPUT_DIM))
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(count_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# build the model
model.fit(X, y, epochs=20)

# Save model
model.save("cuarenta_model.ml")

# predict
#print("Yp:     NO    |    YES")

if bTEST == True:
	Sample_x = np.array([[1,2,1]]) # Expect: 1
else:
	Sample_x = np.array([[7,4,2,4,3,9,5,3,6,9,2,9,5,10,1,10,7,10,9,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,1,6,1,0]]) # Expecting: 1

print("Sample_x:" + str(Sample_x))
print("Dimension:" + str(Sample_x.shape))
# For the output of 3 the array shows the probability of each category --> [0.2%, 0.2%, 0.6%] --> This means that category 2 has higher probability
Yp = model.predict_proba(Sample_x)
print("Yp:" + str(Yp))
