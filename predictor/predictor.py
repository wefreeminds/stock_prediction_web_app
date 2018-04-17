#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 18:42:01 2018

@author: giorgoschantzialexiou
"""
import os
import sys
from flask import jsonify
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
    to_create_test = stock_prices

    scaler = MinMaxScaler(feature_range=(0, 1))
    stock_prices = scaler.fit_transform(stock_prices)


    # create the test data set:
    train_size = int(len(to_create_test) * 0.80)  # TODO: break this to different function
    test_size = len(to_create_test) - train_size  # it is not part of the minscaler
    test = to_create_test[train_size:len(to_create_test),:]




    return (scaler,test)



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

def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])

    return np.array(dataX), np.array(dataY)



def recomend_buy_sell_hold():

    recomendation = "HOLD"   #TODO: implement the indicator

    return recomendation



if __name__=='__main__':


    stock_name = 'AAPL'
    days = 1

    if len(sys.argv) < 2:
        print 'ERROR: Not all argumetns have been specified'
    else:
        stock_name = sys.argv[1]
        days = sys.argv[2]
        input_prediction = np.array([[float(sys.argv[3])]])   # current price

    stock_name = stock_name.upper()

    model_dir = os.path.join('trained_models',stock_name)
    model_dir = os.path.join(model_dir,stock_name.lower())

    data_csv = '../data/historical_stock_price_data/hist_' + stock_name  + '.csv'

    remake_scaler, test = Create_Min_Max_Scaler(data_csv,stock_name)

    model  = Deserialize_Model(model_dir)
    look_back = 1


    testX, testY = create_dataset(test, look_back)
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


    predict_length=5
    input_prediction = np.array([[175]])

    predictions = predict_stock_price(model, input_prediction, predict_length)

    print "predictions"
    print(remake_scaler.inverse_transform(np.array(predictions).reshape(-1, 1)))
    actual_predictions = remake_scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    ## savigin predictions
    predictions_file = '/Users/giorgoschantzialexiou/Repositories/stock_prediction_web_app/predictor/predictions.json'

    data = {"success": False}
    data['predictions'] = []
    data['stock_name:'] = stock_name

    i = 0
    for predict in actual_predictions:
        r = {'day': i, 'predicted_price': str(predict)}
        data['predictions'].append(r)
        i += 1

    recomended_action  = recomend_buy_sell_hold()

    data['recommendation'] = recomended_action

    f = open(predictions_file,'w')
    json.dump(data, f)

    f.close()


