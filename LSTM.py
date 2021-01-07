'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''

from keras.models import Sequential
from keras.layers import LSTM, Dense
import pandas as pd  # read/open csv file (stock market data are in csv file )
import numpy as np 


def stock_analyzer(company, CO, date, LSTM_date):
    
    '''
    1.Read stock market data
    '''
    st_data = pd.read_csv('stock_data//' + company + '.csv')
    row, col = st_data.shape
    # Opening prices & Closing prices & Average prices
    open_price, close_price = st_data['Open'].values,st_data ['Close'].values
    mid_price = (open_price + close_price)/2
    
    # maximum and minumum values; wil be used later for data normalization 
    O_maxi, C_maxi, M_maxi = max(open_price), max(close_price), max(mid_price)
    O_mini, C_mini, M_mini = min (open_price), min(close_price), min(mid_price)
    
    global title #to be used for the data visualization
    ''' opening / closing / average of the two stock values'''
    if CO == 'C': #if the user choose the opening stock data
        price = close_price
        maxi, mini = C_maxi, C_mini 
        title = 'Closing'
        
    elif CO == "O": #if the user choose the closing stock data
        price = open_price
        maxi, mini = O_maxi, O_mini
        title = 'Opening'
        
    elif CO == "M": #if the user choose the average stock data
        price = mid_price
        maxi, mini = M_maxi, M_mini 
        title = 'Average of Opening and Closing' 
    else:
        print ("Please enter a valid choice")


    '''
    2. Create Windows
    '''
    length = LSTM_date + 1  # dataset of x + 1 days (analyzed + predicted)
    windows = [] # inital list for windows
    for index in range (len(price) - length):
            windows.append(price[index:index + length]) 
            # append every window, which includes the data of x days and the data of the next 1 day

            
    '''
    3. Nomalize the data so that the value could be between 0 to 1 using the following equation:
    (x-min_val)/(max_val-min_val)
    '''
    normalized_data = []
    for wd in windows:    
        normalized_window = [(float(p)-mini)/float(maxi-mini)for p in wd]
        normalized_data.append (normalized_window)
    windows = np.array(normalized_data)


    '''
    4. Data sorting
    '''
    '''4-1. Define the size of the dataset to be tested'''
    wid_r = windows.shape [0] # number of rows of windows 
    wid_analyzed = (float(1- date/wid_r)) #ratio of data to be tested = 1 - ratio of data to be analyzed
    size = int(round(wid_r*(wid_analyzed))) #size of data to be tested

    '''4-2. Training dataset'''
    train = windows [:size,:] #training data
    np.random.shuffle (train) #shuffle the training data
    train_x_days = train[:,:-1]  #data of x days
    train_x_days = np.reshape (train_x_days,(train_x_days.shape[0],train_x_days.shape[1],1))
    #reshape to have three dimensions of modeling for the fisrt layer
    train_1_day = train[:,-1] # data of the next 1 day

    '''4-2. Testing dataset'''
    test_x_days = windows[size:,:-1]  #testing data
    test_x_days = np.reshape (test_x_days, (test_x_days.shape[0],test_x_days.shape[1],1))
    #reshape to have three dimensions of modeling (lstm_1)
    test_1_day = windows[size:,-1] #data of next 1 day

    '''4-3. Track the tested dates
            this will be used for sentiment anlaysis'''
    test_date_end = st_data['Date'].iloc[row-1]
    test_date_start = st_data['Date'].iloc[row-1-date]
    test_date = []
    for i in (st_data['Date'].iloc[row-1-date: row-1]):
        test_date.append(i)

        
    '''
    5. Building a LSTM model
    (references from keras Documentation)
    - stack 2 LSTM layers on top of each other,
      making the model capable of learning higher-level temporal representations.
    - The first LSTM returns their full output sequences, 
      but the last one returns the last step in its output sequence 
      by converting the input sequence into a single vector.
    '''
    
    model = Sequential()
    # create a Sequential model by passing a list of layer instances to the constructor
    
    '''first layer'''
    model.add(LSTM(LSTM_date, return_sequences = True, input_shape = (LSTM_date,1))) 
    # setting return_sequences to True is necessary in order to obtain the full sequence as the ouput
    # returns a sequence of vectors of dimension LSTM_date
    # pass an input_shape argument to the first layer so that the model knows what the input shape it should expect. 
    # following layers can do automatic shape inference
    # in input_shape, the batch dimension is not included

    '''second layer'''
    model.add(LSTM(LSTM_date+15,return_sequences = False)) 
    # returns a single vector of dimension LSTM_date + 15 for precision
    # in this case, it is observed that second layer with a single vector of dimension that is different from the diemsion of the first layer increases the accuracy 

    '''output'''
    model.add(Dense(1,activation = "linear")) 
    # output = the next 1 day after x days

    model.compile (loss = "mse",optimizer = "rmsprop") 
    # obtain loss using mean square error
    # use RMSProp optimizer as it is recommended for the recurrent neural networks

    '''training the model'''
    model.fit (train_x_days, train_1_day, 
              validation_data = (test_x_days,test_1_day),
               batch_size = 10, # number of grouped data
               epochs = 20) # number of repetition
    
    predict = model.predict(test_x_days)
    
    return test_1_day, test_x_days, predict, test_date_start, test_date_end, test_date



