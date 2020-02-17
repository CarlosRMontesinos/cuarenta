# Import required libraries
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import sklearn

INPUT_DIM = 3 # 45 = 5 Hand Cards + 40 Table Cards
OUTPUT_DIM = 1 # 1 Next Card
NUM_EXAMPLES = 10 # Number of examples for testing purposes
CARDS_MAX = 2 # In cuarenta the max is 10, so we set it to 11

# Import necessary modules
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

# Keras specific
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical 

#df = pd.read_csv('cuarenta.data') 
#print(df.shape)
#df.describe()

# load dataset
dataframe = pd.read_csv("cuarenta.data", header=None)
dataset = dataframe.values
X = dataset[:,0:INPUT_DIM]
y = dataset[:,INPUT_DIM]

# one hot encode outputs
y = to_categorical(y)
count_classes = y.shape[1] # Bits needed to represent output classes
print(count_classes)

print(X)
print(y)

print("-------------------------------")

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
#print(X_train.shape); print(X_test.shape)

# one hot encode outputs
#y_train = to_categorical(y_train)
#y_test = to_categorical(y_test)

#count_classes = y_test.shape[1]
#print(count_classes)

# Model1
#model = Sequential()	
#model.add(Dense(8, input_dim=INPUT_DIM, activation='relu'))
#model.add(Dense(count_classes, activation='softmax'))
# Compile model
#model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Model 2
model = Sequential()
model.add(Dense(500, activation='relu', input_dim=INPUT_DIM))
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(count_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

#print(X_train)
#print(y_train)

# build the model
model.fit(X, y, epochs=20)

# predict
print("Yp:     NO    |    YES")
Sample_x = np.array([[1,2,1]]) # (~1, 0) | We expect a NO
Yp = model.predict_proba(Sample_x)
print( "Yp:" + str(Yp))

Sample_x = np.array([[1,2,1]]) # (~1, 0) | We expect a NO
Yp = model.predict_proba(Sample_x)
print( "Yp:" + str(Yp))

Sample_x = np.array([[2,1,2]]) # (~1, 0) | We expect a NO
Yp = model.predict_proba(Sample_x)
print( "Yp:" + str(Yp))

Sample_x = np.array([[0,1,1]]) # (0, ~1) | We expect a YES
Yp = model.predict_proba(Sample_x)
print( "Yp:" + str(Yp))

Sample_x = np.array([[0,1,0]]) # (~1, 0) | We expect a NO
Yp = model.predict_proba(Sample_x)
print( "Yp:" + str(Yp))

Sample_x = np.array([[1,1,1]]) # (0, ~1) | We expect a YES
Yp = model.predict_proba(Sample_x)
print( "Yp:" + str(Yp))

Sample_x = np.array([[1,0,1]]) # (~1, 0) | We expect a NO
Yp = model.predict_proba(Sample_x)
print( "Yp:" + str(Yp))

# Save model
model.save("cuarenta_model.ml")


