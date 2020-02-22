# Import required libraries
import numpy as np 

# Keras specific
import keras

# Load model
model = keras.models.load_model("cuarenta_model.ml")

# Use the model
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




