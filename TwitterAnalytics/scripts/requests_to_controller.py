import requests
from time import time
import statistics as st

result, times = list(), list()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/find_hashtag/?lang=es&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover find_hashtag/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/find_hashtag/?lang=en&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover find_hashtag/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_tweets/?lang=es')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_tweets/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_tweets/?lang=en')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_tweets/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_hashtags/?lang=es')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_hashtags/?lang=es: ' + str(st.mean(times)) + ' seconds')

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_hashtags/?lang=en')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_hashtags/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_users/?lang=es')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_users/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_users/?lang=en')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_users/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_users/?lang=es')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_activity_users/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_users/?lang=en')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_activity_users/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_tweets/?lang=es')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_activity_tweets/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_tweets/?lang=en')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_activity_tweets/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_tweets_hashtag/?lang=es&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_tweets_hashtag/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_tweets_hashtag/?lang=en&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_tweets_hashtag/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_users_hashtag/?lang=es&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_users_hashtag/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_important_users_hashtag/?lang=en&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_important_users_hashtag/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_tweets_hashtag/?lang=es&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_acitivty_tweets_hashtag/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_tweets_hashtag/?lang=en&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_activity_tweets_hashtag/?lang=en: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_users_hashtag/?lang=es&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_acitivty_users_hashtag/?lang=es: ' + str(st.mean(times)) + ' seconds')

times.clear()

for i in range(10):
    start = time()
    request = requests.get('http://localhost:8000/load_activity_users_hashtag/?lang=en&hashtag=coronavirus')
    finish = time()
    times.append(finish - start)

result.append('Elapsed time to recover load_activity_users_hashtag/?lang=en: ' + str(st.mean(times)) + ' seconds')


for item in result:
    print(item)