import json
from pymongo import MongoClient
from time import time
import sys
import datetime
import pymongo

LANGUAGES = ['es', 'en']
LANG_ES = 'es'
LANG_EN = 'en'
LAST_HOURS = 1
LAST_DAYS = 4

def read_database(url):
    with open(url) as fh:
        return json.load(fh)

def write_database(url):
    with open(url, 'w') as fh:
        return json.dump(url, fh)


def store_tweets(tweets):
   
    for tweet in tweets:
        #tweet is a dict
        id_tweet = tweet["id_str"]
        created_at = tweet["created_at"]
        retweet_count = tweet['retweet_count'] * 1.5
        favorite_count = tweet['favorite_count']
        score = retweet_count + favorite_count
        id_user = tweet['user']["id_str"]
        user = tweet['user']
        language = tweet['lang']
        #list_hashtags is a list of dicts
        list_hashtags = tweet['entities']['hashtags']
        
        #only save spanish or english tweets
        if language in LANGUAGES:
            insert_tweet(tweet, language)
            insert_score_tweet(id_tweet, score, created_at, language)
            store_users(id_user, user, language)
            store_tweets_of_user(id_user, id_tweet, created_at, score, language)
            store_hashtags_of_tweet(list_hashtags, id_tweet, score, created_at, id_user, language)

def store_users(id_user, user, language):
    if search_user(id_user, language) == None:
        #insert user
        insert_user(id_user, user, language)
    
def store_tweets_of_user(id_user, id_tweet, created_at, score, language):
    if search_tweets_of_user(id_user, language) == None:
        #insert tweets of user
        insert_tweets_of_user(id_user, id_tweet, created_at, score, language)
    else:
        #update tweets of user
        update_tweets_of_user(id_user, id_tweet, created_at, score, language)

def store_hashtags_of_tweet(list_hashtags, id_tweet, score, created_at, id_user, language):
    for dict_hashtag in list_hashtags:
        #extract relevant information about hashtags
        id_hashtag = dict_hashtag['text']
        #check hashtag does not been saved previously or update information that hashtag
        if search_hashtag(id_hashtag.lower(), language) == None: 
            #insert hashtag
            insert_hashtag(id_hashtag, id_tweet, score, created_at, id_user, language)
        else:
            #update hashtag
            update_hashtag(id_hashtag, id_tweet, score, created_at, id_user, language)
        
def store_important_tweets(id_tweet, score, worst_score, most_important_tweets):
    if len(most_important_tweets) < 100:
        most_important_tweets.append((id_tweet, score))
    elif score >= worst_score:
        most_important_tweets[-1] = (id_tweet, score)
    
    return most_important_tweets[-1][1]


def insert_tweet(tweet, language):
    mydb["tweets_" + language].insert_one(tweet)

def insert_score_tweet(id_tweet, score, created_at, language):
    mycol = {"_id": id_tweet, "score": score, "created_at": created_at}
    mydb["score_tweets_" + language].insert_one(mycol)


def insert_user(id_user, user, language):
    mycol = {"_id": id_user, "user": user}
    mydb["users_" + language].insert_one(mycol)

def search_user(id_user, language):
    return mydb['users_' + language].find_one({"_id": id_user})


def insert_tweets_of_user(id_user, id_tweet, created_at, score, language):
    mycol = {"_id": id_user, "total_score": score, "length": 1, "tweets": [{"id_tweet": id_tweet, "created_at": created_at}]}
    mydb["tweets_of_user_" + language].insert_one(mycol)

def update_tweets_of_user(id_user, id_tweet, created_at, score, language):
    filter = {"_id": id_user}
    update = {"$inc": {"total_score": score, "length": 1}, "$push": {"tweets": {"id_tweet": id_tweet, "created_at": created_at}}}
    mydb["tweets_of_user_" + language].find_one_and_update(filter, update)

def search_tweets_of_user(id_user, language):
    return mydb["tweets_of_user_" + language].find_one({"_id": id_user})


def insert_hashtag(id_hashtag, id_tweet, score, created_at, id_user, language):
    mycol = {"_id": id_hashtag, "id_lower": id_hashtag.lower(), "length": 1, "tweets": [{"id_tweet": id_tweet, "score": score, "created_at": created_at}],
        "users": [{"id_user": id_user, "score": score, "created_at": created_at}]}
    mydb["hashtags_" + language].insert_one(mycol)

def update_hashtag(id_hashtag, id_tweet, score, created_at, id_user, language):
    filter = {"id_lower": id_hashtag.lower()}
    update = {"$inc": {"length": 1}, "$push": {"tweets": {"id_tweet": id_tweet, "score": score, "created_at": created_at}, 
    "users": {"id_user": id_user, "score": score, "created_at": created_at}}}
   
    mydb["hashtags_" + language].find_one_and_update(filter, update)

def search_hashtag(id_hashtag, language):
    return mydb["hashtags_" + language].find_one({"id_lower": id_hashtag.lower()})

def search_user_of_hashtag(id_hashtag, id_user, language):
    return mydb["hashtags_" + language].find_one({"id_lower": id_hashtag.lower(), "users.id_user": id_user})


if __name__ == "__main__":

    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["db_tweets"]

    start = time()
    
    #database.py is a first element of argv list -> len(sys.argv) >= 1 always
    if len(sys.argv) == 2:
        if sys.argv[1] == '-l':
            #json file is done
            tweets_json = read_database('/home/josepitarch/Documentos/TFG/TwitterAnalytics/database/corona.json')
            #tweets_json = tweets_json[:1000]
         
            #clear all collections
            for language in LANGUAGES:
                mydb['tweets_' + language].delete_many({})
                mydb["score_tweets_" + language].delete_many({})
                mydb['hashtags_' + language].delete_many({})
                mydb["users_" + language].delete_many({})
                mydb["tweets_of_user_" + language].delete_many({})
            
            #load the new data into the database
            store_tweets(tweets_json)

            finish = time()
            total = finish - start
            cociente, resto = int(total // 60), int(total % 60)
            tmp = str(cociente) + '.' + str(resto)

            print('[INFO] Tweets are been saved successfully')
            print('[INFO] Hashtags are been saved successfully')
            print('[INFO] Users are been saved successfully')
            print('Tiempo transcurrido para cargar todos los datos: %s minutos' %tmp)
        
        elif sys.argv[1] == '-r':
            #read information of database
            for item in mydb["tweets_of_user_es"]:
                print(item)
            finish = time()
            total = finish - start
            cociente, resto = int(total // 60), int(total % 60)
            tmp = str(cociente) + '.' + str(resto)
            print('Tiempo transcurrido para cargar todos los datos: %s minutos' %tmp)
        else:
            print('<usage>: database.py [-l] [-r]')
    else:
        print('<usage>: database.py [-l] [-r]')