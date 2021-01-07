'''
Sia Ham, 1730812
Rhina Kim,1731848
R. Vincent, instructor
420-LCW-MS 
Programming Techniques and Applications
Final Project
'''


from instaphyte import Instagram
import json
from bs4 import BeautifulSoup
import re
import urllib.request
import datetime as dt
from fix_text import unicode_decode,separate
from unix_calculate import get_2years
from binary_search import BinarySearch as bs


api = Instagram()


### scrape website and returns html_info converted into json format ###
def scrape(tag):
    html_info = urllib.request.urlopen('https://www.instagram.com/explore/tags/'+tag).read() # get html info of the page using urllib module
    soup = BeautifulSoup(html_info,"lxml")
    for script_tag in soup.find_all("script"):
        if script_tag.text.startswith("window._sharedData ="):
            shared_data = re.sub("^window\._sharedData = ", "", script_tag.text)
            shared_data = re.sub(";$", "", shared_data)
            shared_data = json.loads(shared_data)
    return shared_data


### get total number of posts obtained from certain hashtag ###
def get_n_posts(data):
    TotalPost = data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['count'] # total number of posts obtained from certain hashtag
    return TotalPost


######################################################################################

### get ID ###
def get_ID(data):
    ID = data["node"]["id"]
    return ID


### get date time ###
def get_date(data):
    time_stamp = data["node"]["taken_at_timestamp"]
    date = dt.datetime.fromtimestamp(time_stamp) #encode date
    #date = date.strftime('%Y-%m-%d  %H:%M') 
    date = date.strftime('%Y-%m-%d') #only need year, month, date
    
    return date


### get URL of the post ###
def get_url(data):
    url = data["node"]["display_url"]
    return url


### get likes of the post ###
def get_likes(data):
    likes = data["node"]["edge_liked_by"]["count"]
    return likes

#######################################################################################


### ### get Text, date, id, date, url, likes ###
def create_datalist(tag_df, N_POSTS, hashtag, n_posts):
    dup_text = 0 # count duplicated text
    no_text = 0 # count post without any text(contents)
    ignored = 0 # count posts ignored (based on the date that are not within past 2 years, or max 5 posts collected with same dates)

    ## used for duplicated texts
    item_list = []
    saw = set(item_list)
    
    ## used for duplicated dates
    date_list = []


    ## Time range List used for scraping posts with limited date ranges
    time_range = get_2years() # Since we need posts within only 2 years (from now) so any posts with date that matches with date_range list will be considered.


    for post in api.hashtag(hashtag, N_POSTS):
        # or for post in api.location(###).hashtag(tag, 10)):
        collect_max = 5

        ########### get date #################
        date = get_date(post)
        found = bs(time_range, date)

        if found == False:
            ignored += 1 #just to count number of texts ignored
            continue

        else:
            if date not in date_list:
                date_list.append(date)
            else:
                date_list.append(date)
                if date_list.count(date) == collect_max: # only get max 3 posts with certain post's date
                    print("################",date,"of post is full (collect max", collect_max, ")")
                    time_range.remove(date) # Here...needs to be improved...
                    continue
        #########################################


        d = json.loads(json.dumps((post))) # USC2 not supported so convert into jsoon
        #display = json.dumps(post, indent=2) # just for display
        #print(display)


        ############## get TEXT #################
        try:
            # get text from the post
            text = d["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
            if text not in saw: # avoid iteration of duplicated (exact same) text
                saw.add(text)
                item_list.append(text)
            else:
                dup_text += 1
                #print(date, "text duplicated.")
                continue
            
            # remove useless characters that affect sentiment analysis
            text = unicode_decode(text)
            text = separate(text)
            #print("\n", text, "\n")
            
        except IndexError:
            no_text += 1
            print(date, "text missing.")
            continue
        # or...
        #if len(d["node"]["edge_media_to_caption"]["edges"])<1:
            #no_text += 1
            #continue
        #########################################
        

        ID = get_ID(d)
        url = get_url(d)
        likes = get_likes(d)

        '''
        print("ID: ", ID)
        print("Text: ", text)
        print("time: ", date)
        print("url: ", url)
        print("likes: ", likes)

        print("--------------------")
        '''
        
        ## append in csv file
        tag_df.loc[len(tag_df)] = [hashtag, n_posts, date, text, url, likes, ID]
    
    posts_obtained = len(date_list) # used for counting total posts obtained
    date_list.clear() # because you might be iterating with different hashtags again
    return tag_df, posts_obtained, ignored, dup_text, no_text



'''
# Optional:
# Get all posts tagged as being in London
for post in api.location("213385402"):
    print(post)
'''

# How to find location number?
# https://havecamerawilltravel.com/photographer/instagram-location-search/



# https://stackabuse.com/how-to-format-dates-in-python/
