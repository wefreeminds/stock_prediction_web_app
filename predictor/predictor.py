#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 18:42:01 2018

@author: giorgoschantzialexiou
"""
import os
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from subprocess import check_output
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.models import model_from_json
from sklearn.cross_validation import  train_test_split
import time #helper libraries
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from numpy import newaxis


def Create_Min_Max_Scaler(data_csv,stock_name):
    
    prices_dataset =  pd.read_csv(data_csv, header=0)
    stock = prices_dataset[prices_dataset['stock_name']==stock_name]
    stock_prices = stock.close.values.astype('float32')
    stock_prices = stock_prices.reshape(stock_prices.shape[0], 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    stock_prices = scaler.fit_transform(stock_prices)
    
    return



def Deserialize_Model(model_dir):
    
    json_dir = model_dir + '.json'
    h5_dir = model_dir + '.h5'
    
    json_file = open(json_dir,'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(h5_dir)
    print("Loaded model from disk")
    
    return loaded_model


def predict_stock_price(model,firstValue, days = 1):
    
    prediction_seqs = []
    curr_frame = firstValue
    
    for i in range(days): 
        predicted = []        
        
        print(model.predict(curr_frame[newaxis,:,:]))
        predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
        
        curr_frame = curr_frame[0:]
        curr_frame = np.insert(curr_frame[0:], i+1, predicted[-1], axis=0)
        
        prediction_seqs.append(predicted[-1])
        
    return prediction_seqs




if __name__=='__main__':
    
    
    
    if len(sys.argv) < 2:
        print 'ERROR: Not all argumetns have been specified'
    else:
        stock_name = sys.argv[1]
        
    stock_name = stock_name.upper()
        
    model_dir = os.path.join('trained_models',stock_name)
    
    data_csv = '../data/historical_stock_price_data/hist_' + stock_name  + '.csv'
    
    remake_scaler = Create_Min_Max_Scaler(data_dir,stock_name)
    
    model  = Deserialize_Model(model_dir)
    
    
    predict_length=5
    predictions = predict_sequences_multiple(model, testX[0], predict_length)
    print(scaler.inverse_transform(np.array(predictions).reshape(-1, 1)))
    plot_results_multiple(predictions, testY, predict_length)
    
    