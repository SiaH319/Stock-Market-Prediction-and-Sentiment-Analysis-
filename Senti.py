'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''

import pandas as pd 
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import timedelta, date

def sentiment_analyzer(company, test_date_start, test_date_end, test_date):
    '''
    converting the string type date to datetime
    '''
    sd = test_date_start.split('-')
    ed = test_date_end.split('-')
    start_date = date(int(sd[0]),int(sd[1]),int(sd[2]))
    end_date= date(int(ed[0]),int(ed[1]),int(ed[2]))
    
    '''
    1.read data
    '''
    senti_data = pd.read_csv('sentiment_data//' + company + '.csv')
    senti_data['Sentiment Score'] = np.nan # new column for sentiment score
    instagram = SentimentIntensityAnalyzer()
    row, col = senti_data.shape
    
    '''
    2. delete the row with no hastag data
    '''
    notag = [] # initial list for the postition of the row with no hastag
    for i in range(row):
        if senti_data.isnull()['text'].iloc[i] == True: # if there is no hastag
            notag.append(i) 
    senti_data = senti_data.drop(i for i in notag)  # delete the row with no hastag

    
    '''
    3. add sentiment score value as a column
    '''
    for i in range(row): #for every values of Date posted, i = location(row index)
        if i not in notag:
            txt = (senti_data['text'].loc[i]) # hastag of the given date
            senti = instagram.polarity_scores(txt)['compound'] # compound sentiment score
            senti_data['Sentiment Score'].loc[i] = senti

    '''
    4. average sentiment score for the given date with one or more than one data
    '''
    def sentiment(date):
        senti_l = []
        for i in range(row): # for every values of Date posted, i = location(row index)
            if i not in notag: # no index exist
                if senti_data['Date posted'].loc[i] == str(date):
                    senti_l.append(senti_data['Sentiment Score'].loc[i])
        return sum(senti_l)/len(senti_l) # average sentiment value           
    
    '''
    range of the date
    '''
    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)
            
    '''
    check if there is any missing date (non-consecutive date) during the given timerange
    '''
    def nodate(start_date,end_date):
        nodate = []
        for i in daterange(start_date,end_date): 
            if any(senti_data['Date posted'].str.contains(str(i))) == False:
                # if there is any missing data during the given time
                nodate.append(str(i))
        return nodate
    
    def thedaybefore(date,add):
        end_date = date - timedelta(days=add)
        return str(end_date)
    def thedayafter(date,subtract):
        end_date = date + timedelta(days=subtract)
        return str(end_date)

    '''5. sentiment score in a dictionary {'date': modified sentiment socre}
        ** if the given date does not exist in data,
        find the first-existing date before the non-existing date
        and the first-existing date after the non-existing date
        and their average would the modified sentiment score for the non-existing date
    '''
    
    def sentiment_analysis(start_date,end_date):
        sentiment_dict={}
        no_date = nodate(start_date,end_date) # check if the dates of the data during the given timerange is consecutive
        # if there is no missing date (have consecutive dates) 
        if len(no_date) == 0: 
            for i in daterange(start_date, end_date): 
                sentiment_dict[str(i)] = sentiment(i)
                
        else: # if there is a missing date (non-consecutive dates)
            for i in daterange(start_date, end_date):
                if str(i) not in no_date: # if the given date exists in data, append the average data of sentiment score
                    sentiment_dict[str(i)] = sentiment(i)                        
                else: # if the given date does not exist in data
                    s,e = 0,0
                    while thedaybefore(i,s) in no_date: # find the first-existing date before the non-existing date
                        s+=1
                    start = str(thedaybefore(i,s))
                    while thedayafter(i,e) in no_date: #find the first-existing date after the non-existing date
                        e+=1
                    end = thedayafter(i,e)
                    sentiment_dict[str(i)] =((sentiment(start)+sentiment(end))/2) # average would the modified sentiment score for the non-existing date
        return(sentiment_dict)


    sentiment_score_list = [] # put the average sentiment score of during the given time range into a list so that it could be used for the data visualization
    result_sentiment = sentiment_analysis(start_date,end_date)
    for i in test_date:
        k = result_sentiment.get(str(i))
        sentiment_score_list.append(k)

    '''normalize the data using the following equation: (x-min_val)/(max_val-min_val)'''
    normalized_sentiment_score_list = []
    maxi = max(sentiment_score_list)
    mini = min(sentiment_score_list)
    
    for i in sentiment_score_list:
        normalized_sentiment_score_list.append((i-mini)/(maxi-mini))
        
    return normalized_sentiment_score_list 
