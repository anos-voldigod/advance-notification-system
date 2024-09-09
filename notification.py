import requests
import tweepy
import numpy as np
import pandas as pd
from plyer import notification
import time
google_map_api_key = 'AIzaSyCYyGLamHrPclvmQVvejg-qlXkaSCwPE8M'
twitter_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAgdvgEAAAAAj7OoLs8C%2FAXGCVlpOY%2FcmZ5unkY%3DbsTiVI1z0TyhPKCyBFh22EXjPTum5P6i9psohz6MdRRPWkIGBA'

client = tweepy.Client(bearer_token=twitter_bearer_token)

def get_live_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        location = data['loc'] 
        return location
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

def get_crowd_data(location):
    try:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=1000&type=restaurant&key={google_map_api_key}"
        response = requests.get(url)
        data = response.json()
        crowd_data = []
        for result in data['results']:
            name = result['name']
            rating = result['rating']
            vicinity = result['vicinity']
            crowd_data.append((name, rating, vicinity))
        return pd.DataFrame(crowd_data, columns=['Name', 'Rating', 'Vicinity'])
    except Exception as e:
        print(f"Error fetching crowd data: {e}")
        return None

def tweet_sentiment(location, radius='2km'):
    try:
        query = f"point_radius:[{location} {radius}]"
        tweets = client.search_recent_tweets(query=query, max_results=100)

        sentiments = []
        for tweet in tweets.data:
            if 'good' in tweet.text.lower():
                sentiments.append(1)  # Positive sentiment
            elif 'bad' in tweet.text.lower():
                sentiments.append(-1)  # Negative sentiment
            else:
                sentiments.append(0)  # Neutral sentiment
        average_sentiment = np.mean(sentiments) if sentiments else 0
        return average_sentiment
    except Exception as e:
        print(f"Error fetching tweet sentiment: {e}")
        return 0

def assess_safety(crowd_level, tweet_sentiment):
    if crowd_level is not None and len(crowd_level) > 5:
        notification.notify(title='Crowd Alert', message='social anxiety', app_icon=None, timeout=10)
    elif crowd_level is not None and len(crowd_level) > 3 and len(crowd_level) <= 5:
        notification.notify(title='Crowd Alert', message='theek hi hai', app_icon=None, timeout=10)
    elif tweet_sentiment > 0:
        notification.notify(title='Crowd Alert', message='vaah ji vaah', app_icon=None, timeout=10)
    elif tweet_sentiment < 0:
        notification.notify(title='Crowd Alert', message='bhaag jaa bsdk', app_icon=None, timeout=10)
    else:
        notification.notify(title='Crowd Alert', message='Nrml', app_icon=None, timeout=10)

def check_and_notify():
    while True:
        live_location = get_live_location()
        crowd_data = get_crowd_data(live_location)
        tweet_sentiment_score = tweet_sentiment(live_location)
        assess_safety(crowd_data, tweet_sentiment_score)

        notification.notify(
            title='Location Safety Alert',
            message=f"Current Location: {live_location}\nCrowd Data: {len(crowd_data) if crowd_data is not None else 'N/A'}\nSafety: [Calculated]",
            timeout=10
        )
        time.sleep(600)

if __name__ == "__main__":
    check_and_notify()
