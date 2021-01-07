# Stock-Market-and-Sentiment-Analysis-
##### This project was done with @chihiroanihr under the guidance of professor R. Vincent in Winter 2019.

### Programming Techniques and Applications
#### 1.     Manual for the Users
##### 1-1.    Requirements:
User should be able to run ipynb extension file using jupyter notebook with the following
modules installed in order to run the program: numpy, bs4, datetime, enchant, instaphyte, keras, nltk, pandas, re, urllib 

##### 1-2.    Operation Manual:

Given the date and name of the company, the program is designed to predict the stock market during the
given time period and to analyze sentiment from the Instagram post containing
the hashtags of the company name during the corresponding period.

User can run real_user.ipynb and choose (i) the name
of the company, (ii) the type of the stock value, (iii) the number of days for
training datasets, and (iv) the number of days to be analyzed from 03 May 2019.
With those, the program will visualize the predicted stock data, original stock
data, and sentiment scores during the given time period in a graph.



#### 2.     Design Guide
##### 2-1.    Stock Market Prediction

The stock market is analyzed
and predicted using LSTM (Long Short-Term Memory) model. Frist, Stock market
data of 5 years (May 06, 2014 to May 03, 2019) of Ford, Tesla, and Nissan –
containing the dates, opening, closing, highest and lowest values – are
collected from Yahoo finance in csv
files.  user.ipynb asks the users to input the name of the company among
three, the type of the stock values such as opening/closing/average stock
values, the number of days to be used for the training datasets of LSTM model,
and the number of days to be analyzed from May 03 2019. 

With the chosen data by
user and using pandas module, LSTM.py reads the csv file, containing
the name of the company and extracts the appropriate stock values by choosing
the corresponding name of the column. As the designed LSTM model analyzes the
days of datasets chosen by the user (LSTM_date)
and predicts the next one day, the length of the window is defined as LSTM_date + 1. Then every window, with
the data of LSTM_date days and the
data of the next one day, is appended in a list windows. Then the data is normalized so that its value could be
between 0 to 1 using the following equation:  , where x is every single value, m is the
minimum value and M is the maximum value. Then the size of the test data is defined
considering the date chosen by the
user. With the size of the test data, training datasets and testing datasets
are defined and reshaped to have three dimensions to match the first layer of
LSTM modeling. While doing so, training datasets are shuffled for machine
learning.



LSTM model is then
created using keras module with the
references from Keras Documentation;
a sequential model is created by passing a list of layer instances to the
constructor. In this model, two stacks of LSTM layers are created on top of
each other, making the model capable of learning higher-level temporal
representations; the first LSTM returns their full output sequences, but the second
one returns the last step in its output sequence by converting the input
sequence into a single vector. 



The first layer returns a
sequence of vectors of dimension LSTM_date
and return_sequences is set to True
in order to obtain a full sequence. The first layer receives information about
its input shape, input_shape =
(LSTM_date, 1), as it analyzes the number of LSTM_dates days and predicts the next one day. This allows the
model to know what the input shape it should expect while the following layers
can do automatic shape inference. 



The second layer returns
a single vector of dimension LSTM_date
+15 and return_sequences is set to False.
The dimension of the vector is different from the dimension of the first layer,
as it is observed to have higher accuracy than when they have the same
dimensions. The dimension of the output is set to 1 as it predicts the stock
value of one day after LSTM_date.
Then every layer is compiled using RMSProp
optimizer as it is recommended for the recurrent neural networks. Loss value is
obtained using a mean square error.



The exact start and end
dates of the analysis are tracked by extracting the date data from the csv
stock file by indexing [the number of rows – date – 1] for the start date and [the number of rows – 1] for the
end date (or it could be set to 03 May 2019). Here, the dates of the stock data
are not consecutive, so every date included in stock data is collected in a
list test_date to be used for sentiment
analysis of the corresponding dates.



##### 2-2.    Sentiment Analysis



###### 2.2.1.    Scraping



Using main.py, 1000 recent Instagram posts with the hashtags containing
the name of the company are stored as csv file in sentiment_data folder, using instaphyte, urllibs and beautifulSoup4 modules. 



###### 2.2.1.1. Scraping and Filtering Instagram Posts



When scraping
data from the Instagram hashtag, the html data from its page source is
obtained. The instaphyte module
enables to get access to every post associated with the specified hashtag. It returns
the information of every single post in json
format then is converted into csv file. 



In order to
avoid Unicode decode error, fix_text.py
extracts English words, filtering out emojis or unremarkable characters. Also,
multiple Instagram posts with identical contents, which are assumed to be
generated for advertisement, are filtered by examining each post in two cases: whether the content of each
post is duplicated; or whether the post is missing the content. In the case of
duplicated content, Instagram_scraping_urllib.py
appends each content of the post to the list item_list and compares them with the content of the next post. To
optimize the loop for examining each post with the elements in the item_list, the list comprehension and
binary search method are implemented. 



###### 2.2.1.2. Balancing the Number of Posts



While scraping,
data is balanced by limiting the number of posts. Using Instaphyte API, it is possible to access every Instagram post and the total number
of posts is specified through instaphyte
module. Then the number of posts per day is balanced by setting the number of
daily posts to be obtained and by ignoring the rest once the number of elements
of certain date in date_list reaches
its maximum (This will be discussed later), yet the code execution time is not
reduced as it scrapes through all the posts. 



With the use of unix_calculate.py, web scraping allows to
access up to recent 2 years of the Instagram posts. Here, the get_2years function in the unix_calculate file returns two year’s
dates in a list called time_range.
Comprehending the mechanism of Unix datetime, the unix_calculate file also converts Unix datetime to normal datetime,
since the date of each post are originally indicated as Unix datetime. Scraping
continues if date of the post is in recent 2 years, in other words, if the date
obtained are found in time_range. 



Then, as mentioned above, the
date of the post obtained is appended to the list date_list. When the post scraped with same dates reaches its
maximum number in the list (which is set to 5), the program looks for the
identical date in the time_range list
and removes the element in time_range
list, so that it will not save the posts with same date anymore.



Then, the
final balanced data is stored as a csv file in sentiment_data
folder, categorizing hashtag, date posted, number of posts for the certain
hashtag, url of the individual post, number of likes and the ID of the poster.



###### 2.2.2. Analyzing Sentiment Data



With the collected
Instagram posts data in a csv file, Senti.py
read the csv file and appends a new column 'Sentiment
Score'. Then it deletes the row with empty hashtag data and stores the
position of the deleted rows in a list notag
since it occurs an error when indexing the deleted position. Compound sentiment
score of every row, except for the positions of the deleted rows, is evaluated using
ntlk module and each sentiment score
is appended in the 'Sentiment Score' column.  



As the raw data has
non-consecutive dates and has several data in one day, the sentiment scores are
modified in two ways. For the dates with more than one data, the sentiment
score of that date is defined by calculating the average of the entire scores
of the date. When there are the non-consecutive dates in the data file during
the chosen period of time, the sentiment score of the missing date is defined
by calculating the average of the first existing date in the data file before
the missing date and the first existing date in the data file after the missing
date (Here, the missing dates are first found using the function daterage and the missing dates are
appended in a list nodate). Then the
date and the corresponding sentiment score are stored as a dictionary. Sentiment
scores are normalized and stored in a list in the order of date.



##### 2-3. Visualization of Data



Given the period of time,
predicted stock values, original stock values and sentiment scores of the corresponding
dates are projected in one graph. Here, sentiment scores are modified so that they
could be in the same range as stock values by being multiplied by fit.



 



Observation and Discussion 



            It is observed that the sentiment score generally
matches the stock data. However, due to the limited number of sentiment data,
the trends of sentiment score are not reliable. Also, On average, it takes
1.30 minutes ~ 2 minutes to scrape 1000 posts since the program is dealing
with massive amounts of data to scrape. For the future
project, scraping execution time could be shortened and sentiment analysis
could be done for other languages including emojis in order to collect more
data in consecutive days. Also, stock data scraping could be done and websites
could be created for better data visualization. 



 



References



            Stock data 



-       
https://ca.finance.yahoo.com/quote/F/history?p=F&.tsrc=fin-srch
(Ford)



-       
https://ca.finance.yahoo.com/quote/NSANY/history?period1=322718400&period2=1556337600&interval=1d&filter=history&frequency=1d (Nissan)



-       
https://ca.finance.yahoo.com/quote/TSLA/history?p=TSLA&.tsrc=fin-srch
(Tesla) 



Keras 



-       
https://keras.io/getting-started/sequential-model-guide/ (Keras Documentaion)



Scraping
Instagram Posts



-       
https://github.com/ScriptSmith/instaphyte (API)



-       
https://www.pythonforbeginners.com/python-on-the-web/web-scraping-with-beautifulsoup 



-       
https://qiita.com/piruty/items/d360f436d1b57cc9c980 (BeautifulSoup)



-       
https://github.com/tomkdickinson/Instagram-Search-API-Python/blob/master/instagram_search.py (Code on GitHub for scraping)



-       
https://stackabuse.com/how-to-format-dates-in-python/ (Date
formatting)



Text Filtering



-       
https://codereview.stackexchange.com/questions/191279/filter-out-non-alphabetic-characters-from-a-list-of-words (non-alphabetic
character)



-       
https://stackoverflow.com/questions/3788870/how-to-check-if-a-word-is-an-english-word-with-python (non-alphabetic
character)



Unix Calculation 



-       
https://stackoverflow.com/questions/7136385/calculate-day-number-from-an-unix-timestamp-in-a-math-way (unix-timestamp)



Sentiment Analysis



-       
https://towardsdatascience.com/https-towardsdatascience-com-algorithmic-trading-using-sentiment-analysis-on-news-articles-83db77966704
(nltk)
