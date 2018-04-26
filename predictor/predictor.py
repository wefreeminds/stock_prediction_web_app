#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 18:42:01 2018

@author: giorgoschantzialexiou
"""
import os
import sys
import json
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
from pandas import read_csv
import real_time


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



def recomend_buy_sell_hold(days):   ## HISTORICAL

    recomendation = "HOLD"   #TODO: implement the indicator
    past_data = read_csv(data_csv)
    past_data = past_data['close']
    past_data.append(df, ignore_index=True)
    past_data = past_data.tail(30)


    ema_26_days = pd.ewma(past_data, span=26)
    ema_12_days = pd.ewma(past_data, span=12)

    MACD = ema_12_days -  ema_26_days



    ##plt.plot(MACD)

    MACD = MACD.tolist()

    if days < 5:
        days = 5

    MACD = MACD[-6:]

    start = MACD[0]

    # if start >0 and we find a price less than zero recomend SELL
    if start>=0:
        for price in MACD:
            if price < 0:
                recomendation = "SELL"

    else:
        for price in MACD:
            if price>=0:
                recomendation = "BUY"


    return recomendation






if __name__=='__main__':


    stock_name = 'AAPL'
    days = 3
    realtime_pred = False

    if len(sys.argv) < 2:
        print 'Usaga: Not all arguments have been specified'
    else:
        stock_name = sys.argv[1]
        days = int(sys.argv[2])
        input_prediction = np.array([[float(sys.argv[3])]])   # current price

    if len(sys.argv)==4:
        if sys.argv[4] == int(1):
            realtime_pred = True



    stock_name = stock_name.upper()


    predictor_dir = os.path.dirname(os.path.realpath(__file__))
    trained_models_dir = os.path.join(predictor_dir,'trained_models')
    model_dir = os.path.join(trained_models_dir,stock_name)


    model_dir = os.path.join(model_dir,stock_name.lower())

    data_csv = '../data/historical_stock_price_data/hist_' + stock_name  + '.csv'

    remake_scaler, test = Create_Min_Max_Scaler(data_csv,stock_name)

    model  = Deserialize_Model(model_dir)
    look_back = 1


    testX, testY = create_dataset(test, look_back)
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


    predict_length=5
    input_prediction = np.array([[175]])

    predictions = predict_stock_price(model, input_prediction, days)

    print "predictions"
    print(remake_scaler.inverse_transform(np.array(predictions).reshape(-1, 1)))
    actual_predictions = remake_scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    ## savigin predictions
    predictions_file = os.path.join(predictor_dir,'predictions.json')


    #predictions_file = '/Users/giorgoschantzialexiou/Repositories/stock_prediction_web_app/predictor/predictions.json'

    data = {"success": False}
    data['predictions'] = []
    data['stock_name:'] = stock_name

    predictions_to_recommend = []


    i = 1

    time_or_day = 'day'

    if realtime_pred:
        time_or_day = 'minute'

    for predict in actual_predictions:
        r = {time_or_day: i, 'predicted_price': str(predict[0])}
        data['predictions'].append(r)
        predictions_to_recommend.append(predict[0])


        i += 1

    predictions_to_recommend = np.asarray(predictions_to_recommend).reshape(len(predictions_to_recommend),1)
    df = pd.DataFrame(predictions_to_recommend) ## new predictions in dataframe


    if realtime_pred:
        real_time.HFT_RSI_RECOM(days=days,stock_name=stock_name)
    else:
        recomended_action  = recomend_buy_sell_hold(days)

    data['recommendation'] =  recomended_action

    f = open(predictions_file,'w')
    json.dump(data, f)

    f.close()


