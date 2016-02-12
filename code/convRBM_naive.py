# Imports
import sys
import os
import random
import time
import numpy as np


class NaiveCRBM:

    def __init__ (self, hyperParams):
        self.hyper_params = hyperParams
        
    def setMotifs (self, motifs_):
        self.motifs = motifs_

    def setBiases (self, b_):
        self.bias = b_

    def setC (self, c_):
			  self.c=c_

    def computeHgivenV (self, data):
        N_h = data.shape[3]-self.hyper_params['motif_length']+1

        M=self.hyper_params['motif_length']

        if self.hyper_params['doublestranded']:
            K=2*self.hyper_params['number_of_motifs']
        else:
            K=self.hyper_params['number_of_motifs']

        h_input = np.zeros((data.shape[0], K, 1, N_h))
        for sample in range(data.shape[0]):
            for k in range(K):
                for n in range(N_h):
                    x = np.sum(data[sample,0,:,range(n,n+M)].T*self.motifs[k,0,:,:]) + self.bias[0,k]
                    h_input[sample, k, 0, n] = x
        
        prob_of_H = np.exp(h_input)
        H = np.zeros(h_input.shape)

        horizontal_pooling_factor=self.hyper_params['pooling_factor']
        if self.hyper_params['doublestranded']:
            vertical_pooling_factor=2
        else:
            vertical_pooling_factor=1

        horizontal_bins = N_h / self.hyper_params['pooling_factor']
        vertical_bins = self.hyper_params['number_of_motifs']

        for iseq in range(data.shape[0]):
            for ivbin in range(vertical_bins):
                for ihbin in range(horizontal_bins):
                    denominator = 1.0
                    for iv in range(vertical_pooling_factor):
                        for ih in range(horizontal_pooling_factor):
                	      	 denominator+=prob_of_H[iseq,ivbin*vertical_pooling_factor+iv,0,ihbin*horizontal_pooling_factor+ih]
                    for iv in range(vertical_pooling_factor):
                        for ih in range(horizontal_pooling_factor):
                	      	 prob_of_H[iseq,ivbin*vertical_pooling_factor+iv,0,ihbin*horizontal_pooling_factor+ih]=\
                	      	 prob_of_H[iseq,ivbin*vertical_pooling_factor+iv,0,ihbin*horizontal_pooling_factor+ih]/denominator
                        
        return [prob_of_H,H]


    def computeVgivenH (self, hidden):
        
        # calculate full convolution (not valid, therefore padding is applied with zeros)
        M = self.hyper_params['motif_length']
        N_v = hidden.shape[3] + M - 1
        if self.hyper_params['doublestranded']:
            K=2*self.hyper_params['number_of_motifs']
        else:
            K=self.hyper_params['number_of_motifs']

        v_input = np.zeros((hidden.shape[0],1,4,N_v))
        for i in range(4):
            v_input[:,:,i,:]=self.c[0,i]

        for iseq in range(hidden.shape[0]):
            for k in range(K):
                for n in range(hidden.shape[3]):
                    v_input[iseq,0,:,range(n,n+M)] += \
                    		self.motifs[k,0,:,:].T * hidden[iseq,k,0,n]
                        
        
        prob_of_V = self.softmax(v_input)
        
        V = np.zeros(v_input.shape)
        
        return [prob_of_V, V]
        

    def collectVHStatistics(self, prob_of_H, data):
    	  #reshape input 
        # calculate full convolution (not valid, therefore padding is applied with zeros)
        M = self.hyper_params['motif_length']
        if self.hyper_params['doublestranded']:
            K=2*self.hyper_params['number_of_motifs']
        else:
            K=self.hyper_params['number_of_motifs']

        vh = np.zeros((K,1,4,M))

        for iseq in range(prob_of_H.shape[0]):
            for k in range(K):
                for n in range(prob_of_H.shape[3]):
                    vh[k,0,:,:] += data[iseq,0,:,range(n,n+M)].T * prob_of_H[iseq,k,0,n]
                        
        
        vh=vh/ (prob_of_H.shape[0]*prob_of_H.shape[3])

        return vh

    def collectVStatistics(self, data):
    	  #reshape input 
        c=np.zeros((1,4))
        for iseq in range(data.shape[0]):
            for ipos in range(data.shape[3]):
							c[0,:]+=data[iseq,0,:,ipos]+data[iseq,0,::-1,ipos]

        c=2.*c/np.sum(c)
        return c

    def collectHStatistics(self, hidden):
    	  #reshape input 
        K=self.hyper_params['number_of_motifs']
        if self.hyper_params['doublestranded']:
            K=2*K
        b=np.zeros((1,K))

        for iseq in range(hidden.shape[0]):
            for ipos in range(hidden.shape[3]):
                for k in range(K):
                    b[0,k]+=hidden[iseq,k,0,ipos]

        b=b/(hidden.shape[0]*hidden.shape[3])
        return b

    def collectUpdateStatistics(self, prob_of_H, data):
    	  #reshape input 

        average_VH=self.collectVHStatistics(prob_of_H, data)
        average_H=self.collectHStatistics(prob_of_H)
        average_V=self.collectVStatistics(data)

        # make the kernels respect the strand structure
        if self.hyper_params['doublestranded']:
            average_VH,average_H = self.matchWeightchangeForComplementaryMotifs(average_VH,average_H)

        return average_VH, average_H, average_V

    
    def matchWeightchangeForComplementaryMotifs(self, evh,eh):

        evhre = evh.reshape((evh.shape[0]//2, 2, 1,evh.shape[2], evh.shape[3]))
        evhre_ = T.inc_subtensor(evhre[:,0,:,:,:], evhre[:,1,:,::-1,::-1])
        evhre = T.set_subtensor(evhre[:,1,:,:,:], evhre[:,0,:,::-1,::-1])
        evh=evhre.reshape(evh.shape)
        evh=evh/2.


        ehre = eh.reshape((1,eh.shape[1]//2, 2))
        ehre=T.inc_subtensor(ehre[:,:,0], ehre[:,:,1])
        ehre=T.set_subtensor(ehre[:,:,1], ehre[:,:,0])
        eh=ehre.reshape(eh.shape)
        eh=eh/2.

        return evh,eh
        
    def softmax (self, x):
        return np.exp(x) / np.exp(x).sum(axis=2, keepdims=True)
