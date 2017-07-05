import matplotlib.pyplot as plt
import numpy as np
import random
import time
from datetime import datetime
import joblib
import os
import sys
sys.path.append("../code")

from convRBM import CRBM
import plotting
from getData import loadSequences

outputdir = os.environ["CRBM_OUTPUT_DIR"]

########################################################
# SET THE HYPER PARAMETERS
hyperParams={
        'number_of_motifs': 10,
        'motif_length': 15,
        'input_dims':4,
        'momentum':0.95,
        'learning_rate': .1,
        'doublestranded': True,
        'pooling_factor': 1,
        'epochs': 100,
        'cd_k': 5,
        'sparsity': 0.5,
        'batch_size': 20,
    }

np.set_printoptions(precision=4)
train_test_ratio = 0.1
batchSize = hyperParams['batch_size']
np.set_printoptions(precision=4)
########################################################

# get the data

training_stem, test_stem = loadSequences('../data/stemcells.fa', \
        train_test_ratio)
training_fibro, test_fibro = loadSequences('../data/fibroblast.fa', \
        train_test_ratio, 4000)

test_merged = np.concatenate( (test_stem, test_fibro), axis=0 )
training_merged = np.concatenate( (training_stem, training_fibro), axis=0 )
nseq=int((test_merged.shape[3]-hyperParams['motif_length'] + \
        1)/hyperParams['pooling_factor'])*\
                hyperParams['pooling_factor']+ hyperParams['motif_length'] -1
test_merged = test_merged[:,:,:,:nseq]
training_merged =training_merged[:,:,:,:nseq]


# generate cRBM models
crbm_stem = CRBM(hyperParams=hyperParams)
crbm_fibro = CRBM(hyperParams=hyperParams)
crbm_merged = CRBM(hyperParams=hyperParams)

# train model
print "Train cRBM ..."
start = time.time()
crbm_stem.trainModel(training_stem,test_stem)
crbm_fibro.trainModel(training_fibro,test_fibro)
crbm_merged.trainModel(training_merged, test_merged)

crbm_stem.saveModel(outputdir + "/stem_model.pkl")
crbm_fibro.saveModel(outputdir + "/fibro_model.pkl")
crbm_merged.saveModel(outputdir + "/merged_model.pkl")

joblib.dump((training_stem, test_stem,training_fibro, test_fibro,training_merged,test_merged),
        outputdir + "dataset.pkl")
