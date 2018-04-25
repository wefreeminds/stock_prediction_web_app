#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 18:29:05 2018

@author: giorgoschantzialexiou
"""

from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
APIkey='PV7KXHYLKJK9Q3YG'
import time
import csv
from pylab import *
import pandas as pd
import numpy as np


def HFT_RSI_RECOM(days=5,stock_name='AAPL'):

    ti = TechIndicators(key='PV7KXHYLKJK9Q3YG', output_format='pandas')
    data, meta_data = ti.get_rsi(symbol=stock_name, interval='5min', time_period=5)#



    rsi = data['RSI'].tolist()

    if days > len(rsi):
        days = len(rsi) -1

    rsi = rsi[-days:]

    rsi_recom = np.mean(rsi)


    recommend = 'HOLD'
    if rsi_recom >=70:
        recommend = 'SELL'
    elif rsi_recom<=30:
        recommend = 'BUY'

    return recommend

