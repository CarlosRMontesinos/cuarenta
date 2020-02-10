from keras.models import Model
from keras.layers import Input, Dense
import numpy as np

INPUT_DIM = 3 # 45 = 5 Hand Cards + 40 Table Cards
OUTPUT_DIM = 1 # 1 Next Card
NUM_EXAMPLES = 10 # Number of examples for testing purposes
CARDS_MAX = 2 # In cuarenta the max is 10, so we set it to 11

#X = np.random.randint(CARDS_MAX, size=(NUM_EXAMPLES, INPUT_DIM))
#Y = np.transpose(X[:,1] * X[:,2])
#print X
#print (X[:,1] * X[:,2])
#print Y
print "----------------"

# Define Model
a = Input(shape=(INPUT_DIM,))
b = Dense(OUTPUT_DIM)(a)
model = Model(inputs=a, outputs=b)

# Configures the model for training.
model.compile(optimizer='rmsprop',
              loss='mean_squared_error',
              metrics=['accuracy'])

# Generate dummy data
#X = np.random.random((NUM_EXAMPLES, INPUT_DIM))
#X = np.random.randint(CARDS_MAX, size=(NUM_EXAMPLES, INPUT_DIM))
#Y = np.random.randint(CARDS_MAX, size=(NUM_EXAMPLES, 1))
#X = np.array([[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1],[0,0,0],[0,0,1]])
#Y = np.array([[0],[1],[1],[1],[0],[1],[1],[1],[0],[1]])
X = np.random.randint(CARDS_MAX, size=(NUM_EXAMPLES, INPUT_DIM))
Y = np.transpose(X[:,1] * X[:,2])

print X
print Y

# Train the model, iterating on the data in batches of INPUT_DIM samples
model.fit(X, Y, epochs=10, batch_size=INPUT_DIM)

# Predict
Sample_x = np.array([[0,0,1]])
Yp = model.predict(Sample_x)

print( "Input" + str(Sample_x))
print( "Prediction" + str(Yp))

