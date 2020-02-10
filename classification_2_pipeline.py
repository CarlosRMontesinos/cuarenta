PPRANK = ['pp1', 'pp2', 'pp3', 'pp4', 'pp5', 'pp6', 'pp7', 'pp8', 'pp9', 'pp10', 'pp11', 'pp12', 'pp13', 'pp14', 'pp15']

FEATURES = (PPRANK)

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

data_df = pd.DataFrame.from_csv("data.csv")
X = np.array(data_df[FEATURES].values)
Y = (data_df["bres"].replace(14,13).values)


# define baseline model
def baseline_model():
    # create model
    model = Sequential()
    model.add(Dense(8, input_dim=(len(FEATURES)), init='normal', activation='relu'))
    model.add(Dense(14, init='normal', activation='softmax'))
    # Compile model
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
#build model
estimator = KerasClassifier(build_fn=baseline_model, nb_epoch=200, batch_size=5, verbose=0)

#split train and test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=seed)
estimator.fit(X_train, Y_train)

#get probabilities
predictions = estimator.predict_proba(X_test)

#convert expon to floats
probs = [[] for x in range(21)]
tick2 = 0
for i in range( len( predictions ) ):
    tick = 0
    for x in xrange(14):
        (predictions[i][(tick)]) = '%.4f' % (predictions[i][(tick)])
        probs[(tick2)].append((predictions[i][(tick)]))
        tick += 1
    tick2 += 1

# pprint probabilities
pp = pprint.PrettyPrinter(indent=0)
pp.pprint(probs)

#print class predictions
print estimator.predict(X_test)
print Y_test
