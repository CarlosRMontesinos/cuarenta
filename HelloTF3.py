from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# https://www.tensorflow.org/get_started/premade_estimators

"""An Example of a DNNClassifier for the Iris dataset."""

import argparse
import tensorflow as tf
import pandas as pd
#import tensorflow as tf
#import iris_data

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')

TRAIN_URL = "http://download.tensorflow.org/data/iris_training.csv"
TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

CSV_COLUMN_NAMES = ['T0','T1','T2','T3','T4','T5','T6','T7','T8','T9','T10','T11','T12','T13','T14','T15','T16','T17','T18','T19','T20',
'T21','T22','T23','T24','T25','T26','T27','T28','T29','T30','T31','T32','T33','T34','T35','T36','T37','T38','T39','C0','C1','C2','C3','C4','NextCompCards']
		
SPECIES = ['0','1','2','3','4','5','6','7','8','9','10']

#CSV_COLUMN_NAMES = ['T0','T1','C0','NextCompCards']
#SPECIES = ['0','1','2']


def maybe_download():
    train_path = tf.keras.utils.get_file(TRAIN_URL.split('/')[-1], TRAIN_URL)
    test_path = tf.keras.utils.get_file(TEST_URL.split('/')[-1], TEST_URL)

    return train_path, test_path

def load_data(y_name='NextCompCards'):
    """Returns the iris dataset as (train_x, train_y), (test_x, test_y)."""
    train_path, test_path = maybe_download()

    train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
    train_x, train_y = train, train.pop(y_name)

    test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)
    test_x, test_y = test, test.pop(y_name)

    return (train_x, train_y), (test_x, test_y)


def load_MyData(y_name='NextCompCards'):
	"""Returns the iris dataset as (train_x, train_y), (test_x, test_y)."""
	#train_path, test_path = maybe_download()

	train_path = "../../Data/40_training.csv"
	test_path = "../../Data/40_test.csv"

	print(train_path)
	print(test_path)

	# Eliminate the header ROW
	train = pd.read_csv(train_path, names=CSV_COLUMN_NAMES, header=0)
	# Assign ALL columns to the X set and the last column to the Y set	
	train_x, train_y = train, train.pop(y_name)

	# Eliminate the header ROW
	test = pd.read_csv(test_path, names=CSV_COLUMN_NAMES, header=0)
	# Assign ALL columns to the X set and the last column to the Y set
	test_x, test_y = test, test.pop(y_name)

	return (train_x, train_y), (test_x, test_y)


def train_input_fn(features, labels, batch_size):
    """An input function for training"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset


def eval_input_fn(features, labels, batch_size):
    """An input function for evaluation or prediction"""
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)

    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices(inputs)

    # Batch the examples
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)

    # Return the dataset.
    return dataset


# The remainder of this file contains a simple example of a csv parser,
#     implemented using a the `Dataset` class.

# `tf.parse_csv` sets the types of the outputs to match the examples given in
#     the `record_defaults` argument.
CSV_TYPES = [[0.0], [0.0], [0.0], [0.0], [0]]

def _parse_line(line):
    # Decode the line into its fields
    fields = tf.decode_csv(line, record_defaults=CSV_TYPES)

    # Pack the result into a dictionary
    features = dict(zip(CSV_COLUMN_NAMES, fields))

    # Separate the label from the features
    label = features.pop('NextCompCards')

    return features, label


def csv_input_fn(csv_path, batch_size):
    # Create a dataset containing the text lines.
    dataset = tf.data.TextLineDataset(csv_path).skip(1)

    # Parse each line.
    dataset = dataset.map(_parse_line)

    # Shuffle, repeat, and batch the examples.
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)

    # Return the dataset.
    return dataset

##############
#### MAIN ####
##############
def main(args):

	# Fetch the data
	#(train_x, train_y), (test_x, test_y) = load_data()
	(train_x, train_y), (test_x, test_y) = load_MyData()	

	print(train_x)
	print(train_y)
	print(test_x)
	print(test_y)

	# Feature columns describe how to use the input based on the type of feature
	# We also explicitly name each column using the 'key' of the X vector
	my_feature_columns = []
	for key in train_x.keys():
		my_feature_columns.append(tf.feature_column.numeric_column(key=key))

	#print("\nFeature Column")
	#print(my_feature_columns)

	# Build 2 hidden layer DNN with 10, 10 units respectively.
	classifier = tf.estimator.DNNClassifier(
	   feature_columns=my_feature_columns,
	   # Two hidden layers of 10 nodes each.
	   hidden_units=[10, 10],
	   # The model must choose between 3 classes.
	   n_classes=11)

	# Train the Model.
	batch_size = 100
	train_steps = 1000
	#shuffle=False

	classifier.train(input_fn=lambda:train_input_fn(train_x,train_y,batch_size),steps=train_steps)   

	# Evaluate the model.
	eval_result = classifier.evaluate(input_fn=lambda:eval_input_fn(test_x, test_y,batch_size))

	print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

	# Generate predictions from the model
#	expected = ['Setosa', 'Versicolor', 'Virginica']
#	predict_x = {
#	   'SepalLength': [5.1, 5.9, 6.9],
#	   'SepalWidth': [3.3, 3.0, 3.1],
#	   'PetalLength': [1.7, 4.2, 5.4],
#	   'PetalWidth': [0.5, 1.5, 2.1],
#	}

	expected = ['6']
#	predict_x ={'T0':'3','T1':'9','T2':'5','T3':'10','T4':'5','T5':'7','T6':'6','T7':'0','T8':'0','T9':'0','T10':'0','T11':'0','T12':'0','T13':'0','T14':'0','T15':'0','T16':'0','T17':'0','T18':'0','T19':'0','T20':'0','T21':'0','T22':'0','T23':'0','T24':'0','T25':'0','T26':'0','T27':'0','T28':'0','T29':'0','T30':'0','T31':'0','C0':'4','C1':'6','C2':'0','C3':'0','C4':'0',}
#	predict_x ={'T0':3,'T1':9,'T2':5,'T3':10,'T4':5,'T5':7,'T6':6,'T7':0,'T8':0,'T9':0,'T10':0,'T11':0,'T12':0,'T13':0,'T14':0,'T15':0,'T16':0,'T17':0,'T18':0,'T19':0,'T20':0,'T21':0,'T22':0,'T23':0,'T24':0,'T25':0,'T26':0,'T27':0,'T28':0,'T29':0,'T30':0,'T31':0,'C0':4,'C1':6,'C2':0,'C3':0,'C4':0}
	predict_x ={'T0':[3],'T1':[9],'T2':[5],'T3':[10],'T4':[5],'T5':[7],'T6':[6],'T7':[0],'T8':[0],'T9':[0],'T10':[0],'T11':[0],'T12':[0],'T13':[0],'T14':[0],'T15':[0],'T16':[0],'T17':[0],'T18':[0],'T19':[0],'T20':[0],'T21':[0],'T22':[0],'T23':[0],'T24':[0],'T25':[0],'T26':[0],'T27':[0],'T28':[0],'T29':[0],'T30':[0],'T31':[0],'T32':[0],'T33':[0],'T34':[0],'T35':[0],'T36':[0],'T37':[0],'T38':[0],'T39':[0],'C0':[4],'C1':[6],'C2':[0],'C3':[0],'C4':[0]}


	predictions = classifier.predict(input_fn=lambda:eval_input_fn(predict_x,None,batch_size))
	print("*****************HERE*******************")
#	print(type(predictions))
#	print(type(expected))
#	zip(predictions, expected)	
	template = ('\nPrediction is "{}" ({:.1f}%), expected "{}"')

	for pred_dict, expec in zip(predictions, expected):
	   class_id = pred_dict['class_ids'][0]
	   probability = pred_dict['probabilities'][class_id]

	   print(template.format(SPECIES[class_id],
		                    100 * probability, expec))

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.ERROR)
    tf.app.run(main)
