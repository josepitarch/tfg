import pdb
import json
from pymongo import MongoClient
import pymongo
from time import time
import datetime
from operator import itemgetter
import requests
import numpy as np
import sys

MAX_IMPORTANT_TWEETS = 20
MAX_IMPORTANT_HASHTAGS = 10
MAX_IMPORTANT_USERS = 10
MAX_ACTIVE_USERS = 10
MAX_SUGGESTIONS_PER_HASHTAG = 5
MAX_IMPORTANT_TWEETS_PER_HASHTAG = 20
MAX_IMPORTANT_USERS_PER_HASHTAG = 10
MAX_DISTANCE_LEVENSHTEIN = 2
MAX_TWEETS_TODAY = 75
MAX_TWEETS_LAST_DAYS = 75
LAST_DAYS = 5

class DatabaseController:

    def __init__(self, language):
       self.__myclient = MongoClient("mongodb://localhost:27017/")
       self.__mydb = self.__myclient["db_tweets"]
       self.__mytweets = self.__mydb["tweets_" + language]
       self.__myscore_tweets = self.__mydb["score_tweets_" + language]
       self.__myhashtags = self.__mydb["hashtags_" + language]
       self.__mytweets_of_user = self.__mydb["tweets_of_user_" + language]
       self.__myusers = self.__mydb["users_" + language]
       self.language = language 
       
    def find_hashtag(self, hashtag):
        response = self.__myhashtags.find_one({"id_lower": hashtag})
        if response != None:
            return str(response['length'])
        else:
            suggestions = list()
            for item in self.__myhashtags.find():
                distance = levenshtein(hashtag, item['id_lower'])
                if distance <= MAX_DISTANCE_LEVENSHTEIN:
                    print(distance)
                    suggestions.append((item['_id'], distance))
              
            return [x for x, y in sorted(suggestions, key = lambda tuple:tuple[1])[:MAX_SUGGESTIONS_PER_HASHTAG]]
    
    def load_important_tweets(self):
        important_tweets = list()
        for mytweet in self.__myscore_tweets.find().sort([("score", pymongo.DESCENDING)]).limit(MAX_IMPORTANT_TWEETS):
            id_tweet = mytweet["_id"]
            tweet = search_tweet(self.__mytweets, id_tweet)
            important_tweets.append(tweet)
        
        return important_tweets
    
    def load_important_hashtags(self):
        name, longitude = list(), list()
        for myhashtag in self.__myhashtags.find().sort([("length", pymongo.DESCENDING)]).limit(MAX_IMPORTANT_HASHTAGS):
            id_hashtag = myhashtag["_id"]
            length = myhashtag["length"]
            name.append(id_hashtag)
            longitude.append(length)
        
        return [name, longitude]
    
    def load_important_users(self):
        important_users = list()
        for myimporant_user in self.__mytweets_of_user.find().sort([("total_score", pymongo.DESCENDING)]).limit(MAX_IMPORTANT_USERS):
            id_user = myimporant_user["_id"]
            user = search_user(self.__myusers, id_user)
            important_users.append(user)

        return important_users

    def load_activity_users(self):
        activity_users = list()
        
        for item in self.__mytweets_of_user.find().sort([("length", pymongo.DESCENDING)]).limit(MAX_ACTIVE_USERS):
            user = search_user(self.__myusers, item['_id'])
            user_tweets = item['tweets']
            activity_user = create_activity(self, user_tweets)
            activity_users.append([activity_user, user])

        return activity_users
   
    def load_activity_tweets(self):
        tweets = self.__mytweets.find()
        return create_activity(self, tweets)

    def load_important_tweets_hashtag(self, id):
        important_tweets = list()
        hashtag = self.__myhashtags.find_one({"id_lower": id})
        if hashtag != None:
            #tweets_of_hashtag is a list of dicts
            tweets_of_hashtag = hashtag['tweets']
            #only recover TWEETS_PER_HASHTAG most relevant tweets
            tweets_of_hashtag = sort_tweets_of_hashtag(tweets_of_hashtag)
          
            for item in tweets_of_hashtag:
                id_tweet = item[0]
                tweet = search_tweet(self.__mytweets, id_tweet)
                important_tweets.append(tweet)
            
            return important_tweets
        else:
            return None

    def load_important_users_hashtag(self, id):
        important_id_users, important_users, visited_user = list(), list(), list()
        hashtag = self.__myhashtags.find_one({"id_lower": id})
        #list of dicts
        if hashtag != None:
            users = hashtag['users']
            for user in users:
                id = user['id_user']
                score = 0
                if id in visited_user:
                    continue
                else:
                    visited_user.append(id)
                
                for user_in in users:
                    if id == user_in['id_user']:
                        score += user_in['score']

                if len(important_id_users) == MAX_IMPORTANT_USERS_PER_HASHTAG:
                    important_id_users[-1] = (id, score)
                else:
                    important_id_users.append((id, score))
                            
                important_id_users = sorted(important_id_users, key = lambda tuple:tuple[1], reverse = True)

            for user in important_id_users:
                important_users.append(search_user(self.__myusers, user[0]))

            return important_users
        
        else:
            return None

    def load_activity_users_hashtag(self, id):
        activity_id_users, activity_users = list(), list()
        hashtag = self.__myhashtags.find_one({"id_lower": id})
        #list of dicts
        if hashtag != None:
            users = hashtag['users']

            for user in users:
                length = 0
                dates = list()
                for user_in in users:
                    if user['id_user'] == user_in['id_user']:
                        length = length + 1
                        dates.append({"created_at": user_in['created_at']})
                
                if user['id_user'] not in [x[0] for x in activity_id_users]:
                    activity_id_users.append((user['id_user'], length, dates))

            activity_id_users = sorted(activity_id_users, key = lambda tuple:tuple[1], reverse = True)[:MAX_IMPORTANT_USERS_PER_HASHTAG]
            
            for id_user in activity_id_users:
                user = search_user(self.__myusers, id_user[0])
                dates = create_activity(self, id_user[2])
                activity_users.append([dates, user])

            return activity_users
        
        else:
            return None

    def load_activity_tweets_hashtag(self, id):
        hashtag = self.__myhashtags.find_one({"id_lower": id})
        return create_activity(self, hashtag['tweets']) if hashtag != None else None


def sort_tweets_of_hashtag(tweets_of_hashtag):
    #list of tuples [(id_tweet, score)]
    list_tweets = list()
    for dct in tweets_of_hashtag:
        keys = list()
        for key in dct.keys():
            keys.append(key)
        list_tweets.append((dct[keys[0]], dct[keys[1]]))
    
    return sorted(list_tweets, key = lambda tuple:tuple[1], reverse = True)[:MAX_IMPORTANT_TWEETS_PER_HASHTAG]

def search_tweet(mytweets, id_tweet):
    mycol = {"id_str": id_tweet}
    tweet = mytweets.find_one(mycol)
    return reduce_tweet(tweet)

def search_user(myusers, id_user):
    mycol = {"_id": id_user}
    user = myusers.find_one(mycol)
    return reduce_user(user)

def reduce_tweet(tweet):
    minimize_tweet = dict()
    minimize_tweet['profile_image_url_https'] = tweet['user']['profile_image_url_https']
    minimize_tweet['check_url_image'] = check_url_image(tweet['user']['profile_image_url_https'])
    minimize_tweet['name'] = tweet['user']['name']
    minimize_tweet['screen_name'] = tweet['user']['screen_name']
    minimize_tweet['retweet_count'] = tweet['retweet_count']
    minimize_tweet['favorite_count'] = tweet['favorite_count']
    minimize_tweet['full_text'] = tweet['full_text']#[:tweet['full_text'].find('https://')]
    minimize_tweet['created_at'] = transform_date(tweet['created_at'].split())
    aux = tweet['source']
    minimize_tweet['source'] = aux[aux.find("Twitter"):aux.find("</a>")]

    contains_media = tweet.get('extended_entities', None)
    if contains_media != None:
        minimize_tweet['media'] = True
        
        if contains_media['media'][0]['type'] == 'photo':
            minimize_tweet['media_type'] = 'photo'
            minimize_tweet['media_url'] = contains_media['media'][0]['media_url_https']
        else:
            minimize_tweet['media_type'] = 'video'
            aux = contains_media['media'][0]['video_info']['variants'][0]['url']
            if aux.find('m3u8') == -1:
                minimize_tweet['media_url'] = aux
            else:
                minimize_tweet['media_url'] = contains_media['media'][0]['video_info']['variants'][1]['url']
    else:
       minimize_tweet['media'] = False
    
    return minimize_tweet

def reduce_user(user):
    minimize_user = dict()
    minimize_user['name'] = user['user']['name']
    minimize_user['screen_name'] = user['user']['screen_name']
    minimize_user['verified'] = user['user']['verified']
    minimize_user['description'] = user['user']['description']
    minimize_user['check_url_image'] = check_url_image(user['user']['profile_image_url_https'])
    minimize_user['profile_image_url_https'] = user['user']['profile_image_url_https']
    minimize_user['followers_count'] = transform_followers_count(str(user['user']['followers_count']))

    return minimize_user

def transform_date(date):
    number_of_month = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", 
        "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    return date[2] + "/" + number_of_month[date[1]] + "/" + date[5]

def transform_followers_count(followers_count):
    return '+' + followers_count[0] + "0" * (len(followers_count) - 1)

def create_activity(self, data):
    #first dict for days, second dict for hours
        activity = [{}, {}]
        #[Day, Month, Number, Hour, Year]
        #date = datetime.datetime.now().strftime("%c").split()
        date = ["Thu", "Mar", "19", "14:15:27", "2020"]

        #number_of_day = int(date[2])
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        position = days.index(date[0])
        for i in range(0, LAST_DAYS + 1):
            #aux = number_of_day - LAST_DAYS + i
            aux = days[position - LAST_DAYS + i]
            activity[0][str(aux)] = 0
        
        for i in range(0, 24):
            activity[1][str(i)] = 0

        for item in data:
            #[Day, Month, Number, Hour, Zone, Year]
            date_tweet = item['created_at'].split()
            #same day, save hours
            if int(date[2]) - int(date_tweet[2]) <= LAST_DAYS:
                if int(date[2]) == int(date_tweet[2]):
                    aux = date_tweet[3].find(":")
                    hour = date_tweet[3][:aux]
                    exists_hour = activity[1].get(hour, None)
                    if exists_hour != None:
                        activity[1][hour] = activity[1][hour] + 1
                
                #save day
                day = date_tweet[0]
                exists_day = activity[0].get(day, None)
                if exists_day != None:
                    activity[0][day] =  activity[0][day] + 1
                            
        activity = transform_activity(self, activity, date)

        return activity

def transform_activity(self, activity_tweets, month):
    res=[[[],[]],[[],[]]]
    lan = 0 if self.language == 'es' else 1
    #days
    for tupla in activity_tweets[0].items():
        res[0][0].append(map_days_of_week(tupla[0], lan))
        res[0][1].append(tupla[1])
    #hours
    for tupla in activity_tweets[1].items():
        res[1][0].append(tupla[0])
        res[1][1].append(tupla[1])

    return res

def map_days_of_week(day, language):
    map_days = {"Mon": ["Lunes", "Monday"], "Tue": ["Martes", "Tuesday"], "Wed": ["Miércoles", "Wednesday"], 
    "Thu": ["Jueves", "Thursday"], "Fri": ["Viernes", "Friday"], "Sat": ["Sábado", "Saturday"], "Sun": ["Domingo", "Sunday"]}
    
    return map_days.get(day, None)[language]

def check_url_image(url):
    request = requests.get(url)
    if request.status_code == 200:
        return 1
    else:
        return 0

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])