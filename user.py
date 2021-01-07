'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''

company_list = ['Ford', 'Nissan', 'Tesla']
CO_list = ['C','O','M']

'''stock market data'''
while True:
    global  company
    company = input ("Choose one of the following companies for data analysis (Ford, Nissan, Tesla):")
    if company not in company_list:
        print ('\n' + 'Please enter a valid company name')
    else:
        break

'''stock value'''
while True:
    global CO
    CO = input("Enter O for the opening stock value, C for the closing stock value, and M for the average value of two:")
    if CO not in CO_list:
        print ('\n' + 'Please enter one of the followings: M, O, C')
    else:
        break


while True:
    global LSTM_date
    LSTM_date = int(input("Enter the number of days (around 30-60) to be used for the training datasets of LSTM model:"))
    #this will be used to store & analyze the data of x days and predict the data of the next 1 day'''
    if not 70 > LSTM_date > 25:
        print ('\n' + 'Please enter the number of days (around 30-60) for training datasets for LSTM:"')
    else:
        break


while True:
    global date
    date = int(input("Enter the number of days (less than 200 days) to be analyzed from 03 May 2019:"))
    if date > 200:
        print ('\n' + 'Please choose the number of days less than 200')
    else:
        break



