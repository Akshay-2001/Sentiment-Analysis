"""
Created on Tue Sep 20 19:15:13 2022

STOCK NEWS SENTIMENTAL ANALYSIS AND VISUALIZATION

@author: Akshay
"""

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

finviz_url = 'https://finviz.com'

ticker1 = 'AMZN'
ticker2 = 'AMD'
ticker3 = 'AAPL'
ticker4 = 'BB'
ticker5 = 'IBM'
ticker6 = 'HMC'

tickers = ['AMZN', 'AMD', 'AAPL', 'BB', 'IBM', 'HMC']

news_tables = {}

for ticker in tickers:
    url = finviz_url + '/quote.ashx?t=' + ticker
    
    req = Request(url=url, headers={'user-agent':'my-app'})
    response = urlopen(req)
    '''print(response)'''
    
    html = BeautifulSoup(response, 'html.parser')
    
    '''print(html)'''
    news_table = html.find(id='news-table')
    
    news_tables[ticker] = news_table
    
    # break
    
    
    
'''print(news_tables)'''

'''
TRIAL RUN TO CHECK IF IT IS WORKING WITH OUR DATA

amzn_data = news_tables['AMZN']
#finding all the table rows relevent to the above mentioned object
amzn_rows = amzn_data.findAll('tr')
#print(amzn_rows)

for index, row in enumerate(amzn_rows):
    title = row.a.text
    #we do this so as to get the text inside of the <a> tag
    timestamp = row.td.text
    #On observing the page source code, we get to know that the time stamp is in <td> tag. Hence we use the above code to get the timestamp as text
    print(timestamp + " " + title)
    
NOW WE NEED TO DO THIS TO EVERY TICKER IN THE LIST AND STORE THE SCRAPED DATA IN A NEW LIST OF ITEMS
'''

parsed_data = []

for ticker, news_table in news_tables.items():
    #iterating over every single key value pair in news tables dictionary
    
    for row in news_table.findAll('tr'):
        
        #scraping multiple elements title and time stamp
        
        title = row.a.get_text()
        date_data = row.td.text.split(' ')
        
        if len(date_data) == 1 :
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]
            
        parsed_data.append([ticker, date, time, title])
        
#print(parsed_data)

#Sentimental Analysis Part

df = pd.DataFrame(parsed_data,columns=['ticker', 'date', 'time', 'title'] )

vader = SentimentIntensityAnalyzer()

#print(vader.polarity_scores("I think Apple is a good company. I think they will fail sales this quarter."))

#print(df.head())
#print(df.tail())

#print(df['title'])

f = lambda title: vader.polarity_scores(title)['compound']

df['compound'] = df['title'].apply(f)

#print(df.head())

#Now Lets convert date from string to a date time format

df['date'] = pd.to_datetime(df.date).dt.date

plt.figure(figsize=(10,8))

mean_df = df.groupby(['ticker', 'date']).mean()
mean_df = mean_df.unstack()

mean_df = mean_df.xs('compound', axis="columns").transpose()
''' 
So if we just simply transpose mean_df 
then we get an extraneous column named compund which is not needed 
This compound column exists because of groupby and unstacking
and by simply taking the cross section we can get rid of the extra label that is added
'''
mean_df.plot(kind='bar')
plt.show()
#print(mean_df)

