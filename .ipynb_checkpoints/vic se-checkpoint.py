'''
Sia Ham  Rhina Kim
Programming and Techniques
Final Project
'''

import pandas as pd  #read csv file (stock market data is in csv file )
import numpy as np 
import matplotlib.pyplot as plt #visualize the data
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activatio
import datetime

''' read stock market data'''
vs_data = pd.read_csv('vs_stock_data_5y.csv') 
vs_data.head() #first five data
high = vs_data['High'].values #bring the data of high prices 
low = vs_data['Low'].values #bring the data of low prices
mid  = (high+low)/2 #mid prices -> we are just predicting the low prices

'''create windows for the data of the 51 days
this store the data of 50 days and predict the data of the next date'''

seq_len = 50 #data set of 50 days
sequence_length = seq_len + 1 #data set of 50 + 1 days (stored + predicted)

result = []
for index in range (len(mid_prices) - seqence_length):
    result.append(mid[index:index + sequence_length]) #append every windows, which includes the data of 50days and the data of the next day

'''nomalize the data
let the first window be 0 by dividing by itself and -1
set the relative value for the others
by dividing its data by the first window and - 1'''

normalized_data = []
for window in result:
    normalized_window = [(float(p)/foat(window[0])-1)for p in window]
    normalized_data.append (normalize_window)

reult = np.array (normalized_data)

size = int(rount(result.shape[0]*0.9)) #90% of the dataset
training_data = retul [:size,:]
np.random.shuffle (training_data)
