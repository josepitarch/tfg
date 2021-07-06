"""TFG URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
import pdb
from django.contrib import admin
from django.urls import path, include
from TwitterAnalytics.views import index, hashtag, find_hashtag, load_important_tweets, load_important_hashtags, load_important_users
from TwitterAnalytics.views import load_activity_users, load_activity_tweets, es, en
from TwitterAnalytics.views import load_important_tweets_hashtag, load_important_users_hashtag, load_activity_users_hashtag, load_activity_tweets_hashtag

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('es/', es, name="es"),
    path('en/', en, name="en"),
    path('hashtag/', hashtag, name="hashtag"),
    path('find_hashtag/', find_hashtag, name="find_hashtag"),
    path('load_important_tweets/', load_important_tweets, name="load_important_tweets"),
    path('load_important_hashtags/', load_important_hashtags, name="load_important_hashtags"),
    path('load_important_users/', load_important_users, name="load_important_users"),
    path('load_activity_users/', load_activity_users, name="load_activity_users"),
    path('load_activity_tweets/', load_activity_tweets, name="load_activity_tweets"),
    path('load_important_tweets_hashtag/', load_important_tweets_hashtag, name="load_important_tweets_hashtag"),
    path('load_important_users_hashtag/', load_important_users_hashtag, name="load_important_users_hashtag"),
    path('load_activity_tweets_hashtag/', load_activity_tweets_hashtag, name="load_activity_tweets_hashtag"),
    path('load_activity_users_hashtag/', load_activity_users_hashtag, name="load_activity_users_hashtag"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
