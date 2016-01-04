import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split

from convRBM import CRBM
import getData as dataRead

import numpy as np
import random
import time
from datetime import datetime
import cPickle

# read the data
seqReader = dataRead.FASTAReader()
allSeqs = seqReader.readSequencesFromFile('../data/wgEncodeAwgDnaseUwAg10803UniPk.fa')

#data = [allSeqs[random.randrange(0,len(allSeqs))] for i in range(20000)]
data = allSeqs
train_set, test_set = train_test_split(data, test_size=0.1)
print "Training set size: " + str(len(train_set))
print "Test set size: " + str(len(test_set))

start = time.time()
trainingData = np.array([dataRead.getMatrixFromSeq(t) for t in train_set])
testingData = np.array([dataRead.getMatrixFromSeq(t) for t in test_set])
print "Conversion of test set in (in ms): " + str((time.time()-start)*1000)

learner = CRBM(3, 20, 0.001, 2)
print "Data mat shape: " + str(trainingData.shape)
start = time.time()
scores = learner.trainMinibatch(trainingData, testingData, 100, 50, 1)
print "Training of " + str(trainingData.shape[0]) + " performed in: " + str(time.time()-start) + " seconds."

# save trained model to file
file_name = datetime.now().strftime("trainedModel_%Y_%m_%d_%H_%M.pkl")

with open('models/' + file_name, 'w') as f:
	cPickle.dump(learner, f)
	
for i in range(len(scores)):
    plt.ylabel('Function applied during learning')
    plt.xlabel('Number Of Epoch')
    plt.title('Small dataset on real data')
    plt.plot(scores[i])
    plt.savefig('test_' + str(i) + ".png")
