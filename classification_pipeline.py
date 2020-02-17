# https://machinelearningmastery.com/multi-class-classification-tutorial-keras-deep-learning-library/

# This solution takes 3 inputs and maps them to a NO, YES label.
# The rule implemented is, if the last two numbers are 1's the output should be YES, else NO

# multi-class classification with Keras
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
import numpy as np

INPUT_DIM = 3 # 45 = 5 Hand Cards + 40 Table Cards
OUTPUT_DIM = 1 # 1 Next Card
NUM_EXAMPLES = 10 # Number of examples for testing purposes
CARDS_MAX = 2 # In cuarenta the max is 10, so we set it to 11

EPOCHS = 200 #200

# load dataset
dataframe = pandas.read_csv("cuarenta.data", header=None)
dataset = dataframe.values
X = dataset[:,0:INPUT_DIM].astype(float)
Y = dataset[:,INPUT_DIM]

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)

# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=INPUT_DIM, activation='relu'))
	model.add(Dense(INPUT_DIM-1, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

estimator = KerasClassifier(build_fn=baseline_model, epochs=EPOCHS, batch_size=5, verbose=0)
kfold = KFold(n_splits=10, shuffle=True)

# Evaluate model performance
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

# train
#estimator.fit(X, Y)

# estimate / predict Yp = [Prob NO , Prob YES]
#print("Yp:     NO    |    YES")
#Sample_x = np.array([[1,2,1]]) # (~1, 0) | We expect a NO
#Yp = estimator.predict_proba(Sample_x)
#print( "Yp:" + str(Yp))

#Sample_x = np.array([[2,1,2]]) # (~1, 0) | We expect a NO
#Yp = estimator.predict_proba(Sample_x)
#print( "Yp:" + str(Yp))

# Save model
model.save("cuarenta_model.ml")



#Sample_x = np.array([[0,1,1]]) # (0, ~1) | We expect a YES
#Yp = estimator.predict_proba(Sample_x)
#print( "Yp:" + str(Yp))

#Sample_x = np.array([[0,1,0]]) # (~1, 0) | We expect a NO
#Yp = estimator.predict_proba(Sample_x)
#print( "Yp:" + str(Yp))

#Sample_x = np.array([[1,1,1]]) # (0, ~1) | We expect a YES
#Yp = estimator.predict_proba(Sample_x)
#print( "Yp:" + str(Yp))

#Sample_x = np.array([[1,0,1]]) # (~1, 0) | We expect a NO
#Yp = estimator.predict_proba(Sample_x)
#print( "Yp:" + str(Yp))
