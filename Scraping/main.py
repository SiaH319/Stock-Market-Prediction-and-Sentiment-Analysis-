'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''

print("\n\n\nloading module...(please wait, may take up to 20 seconds.)\n")

import os
import instagram_scraping_urllib as isu
import datetime as dt
import time
import pandas as pd

print("Running in", os.getcwd(), "\n\n\n")


### Purposely iterates 3 tags when analyzing one motor company: in order to avoid missing dates in data.
### ex) 2019/2/3 for #ford post is missing because nobody uploaded on 2/3.
taglist = [
    ["ford", "fords", "fordmustang"],
    ["nissan","nissanusa","nissancanada"],
    ["tesla", "teslamotors", "teslacars"]
    ]

## Make a csv file
tag_df = pd.DataFrame(columns = ['Hashtag', 'Number of Posts', 'Date posted', 'text', 'url', 'likes', 'ID'])


################# INPUTS #####################
while True:
    print("\n1. Ford", "\n2. Nissan", "\n3. Tesla")
    i = input("Which company to analyze? (Enter number) or enter F to finish: ") #value name data
    if i == "F":
        break
    elif i == "1":
        tag = taglist[0]
        break
    elif i == "2":
        tag = taglist[1]
        break
    elif i == "3":
        tag = taglist[2]
        break
    else:
        print("Please type again.\n")

while True:
    j = input("\nHow many posts would you like to get for the selected hashtag?: ")
    try:
        j = int(j)
        break
    except ValueError:
        pass  # it was a string, not an int.
##############################################

print("\n")
print("-- Average code execution time: 90s(1min 30s) / 1000 posts,1hashtag --")
startTime = dt.datetime.now() # To measure code execution time
N_POSTS = j # Get j number of posts from each hashtags (user input)

## Iterate each hashtag in #Motor company
for hashtag in tag:
    print("\n\n===========================================")
    print("Tag: ", hashtag)
    shared_data = isu.scrape(hashtag) # get html info converted into json
    n_posts = isu.get_n_posts(shared_data) # return number of posts of certain tag
    print("Number of posts: ", n_posts)

    tag_df, posts_obtained, ignored, dup_text, no_text = isu.create_datalist(tag_df, N_POSTS, hashtag, n_posts)
    #tag_df, posts_obtained, ignored, dup_text, no_text, ID, text, date, url, likes = isu.create_datalist(tag_df, N_POSTS, hashtag, n_posts)
    print("===========================================")
    print("Number of posts Ignored: ", ignored, "/", N_POSTS)
    print("Number of Duplicated text: ", dup_text, "/", N_POSTS-ignored)
    print("Number of posts with missing text: ", no_text, "/", N_POSTS-ignored)
    print("Total number of posts obtained for "+hashtag+": ", posts_obtained)


## Save datas into csv file
file_name = tag[0].capitalize() + "_"   # Determine file name
from_path = os.getcwd()
to_path = from_path.replace("\Scraping", "") + "\Data_Analysis\sentiment_data\\"
tag_df.sort_values(by='Date posted', inplace=True)   # Sort Values based on Date posted
tag_df.to_csv(to_path + file_name + ".csv", encoding='utf_8_sig')   # encoding=... to avoid the text garbling


print("\n\n===========================================")
print("The time of code execution begin: ", time.ctime())
print("Time taken for the code excution: ", dt.datetime.now() - startTime)
print("\n\nCSV file has been created.")

