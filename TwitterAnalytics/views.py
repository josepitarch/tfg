import pdb
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, loader
from django.shortcuts import render, redirect
import json
from TwitterAnalytics import DatabaseController as bd
from time import time

#------ Global variables -------
msg_error = "Something has gone wrong..."

def index(request):
   language = request.LANGUAGE_CODE[:2]
   if language == 'es':
      return render(request, 'es/index.html')
   else:
      return render(request, 'en/index.html')

def es(request):
   return render(request, 'es/index.html')

def en(request):
   return render(request, 'en/index.html')

def hashtag(request):
   language = request.LANGUAGE_CODE[:2]
   if request.method == 'GET':
      hashtag =  request.GET.get('hashtag', None)
      lang = request.GET.get('lang', None)
      if lang != None:
         language = lang
   
   if hashtag != None and len(hashtag) > 0:
      if check_language(language) == 'es':
         return render(request, 'es/hashtag.html', {"hashtag": hashtag})
      else:
         return render(request, 'en/hashtag.html', {"hashtag": hashtag})
   
   else:
      return JsonResponse(msg_error, safe = False)
        
def find_hashtag(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      hashtag = request.GET.get('hashtag', None)
      lang = request.GET.get('lang', None)
      if lang != None:
         language = lang
   
   if hashtag != None and len(hashtag) > 0:
      database = bd.DatabaseController(language)
      response = database.find_hashtag(hashtag.lower())
      response = json.dumps(response)
      
      return JsonResponse(response, safe = False)
   
   else:
      return JsonResponse(msg_error, safe = False)
    
def load_important_tweets(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)
   
   database = bd.DatabaseController(language)
   important_tweets = database.load_important_tweets()
   response = json.dumps(important_tweets)
   
   return JsonResponse(response, safe = False)

def load_important_hashtags(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)

   database = bd.DatabaseController(language)
   important_hashtags = database.load_important_hashtags()
   response = json.dumps(important_hashtags)
   return JsonResponse(response, safe = False)

def load_important_users(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)

   database = bd.DatabaseController(language)
   important_users = database.load_important_users()
   response = json.dumps(important_users)
   return JsonResponse(response, safe = False)

def load_activity_users(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)

   database = bd.DatabaseController(language)
   activity_users = database.load_activity_users()
   response = json.dumps(activity_users)
   return JsonResponse(response, safe = False)

def load_activity_tweets(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)

   database = bd.DatabaseController(language)
   activity_tweets = database.load_activity_tweets()
   response = json.dumps(activity_tweets)
   return JsonResponse(response, safe = False)

def load_important_tweets_hashtag(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      print(request.GET)
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)
   
   hashtag = str(request.GET.get('hashtag', None)).lower()
   database = bd.DatabaseController(language)
   tweets_of_hashtag = database.load_important_tweets_hashtag(hashtag)
   response = json.dumps(tweets_of_hashtag)
   return JsonResponse(response, safe = False)

def load_important_users_hashtag(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)

   hashtag = str(request.GET.get('hashtag', None)).lower()
   database = bd.DatabaseController(language)
   important_users_hashtag = database.load_important_users_hashtag(hashtag)
   response = json.dumps(important_users_hashtag)
   return JsonResponse(response, safe = False)

def load_activity_tweets_hashtag(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)
         
   hashtag = str(request.GET.get('hashtag', None)).lower()
   database = bd.DatabaseController(language)
   activity_tweets_hashtag = database.load_activity_tweets_hashtag(hashtag)
   response = json.dumps(activity_tweets_hashtag)
   return JsonResponse(response, safe = False)

def load_activity_users_hashtag(request):
   language = check_language(request.LANGUAGE_CODE[:2])
   if request.method == 'GET':
      lang = request.GET.get('lang', None)
      if lang != None:
         language = check_language(lang)

   hashtag = str(request.GET.get('hashtag', None)).lower()
   database = bd.DatabaseController(language)
   activity_users_hashtag = database.load_activity_users_hashtag(hashtag)
   response = json.dumps(activity_users_hashtag)
   return JsonResponse(response, safe = False)

def check_language(language):
   return language if language in ['es', 'en'] else 'en'