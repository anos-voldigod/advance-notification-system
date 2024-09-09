# advance-notification-system

## Overview
This project is a Python-based safety notification system that uses Google Maps API, Twitter API, and real-time location data to assess the safety of a given area. The system fetches crowd data from nearby locations and analyzes the sentiment of tweets from that area. Based on the crowd level and tweet sentiment, it notifies the user about the safety of the location.

## Features
1. Live Location Tracking: The system automatically detects the user's current location using the IP address.
2. Crowd Data Retrieval: Fetches data from Google Maps API about nearby places, including their names, ratings, and vicinities.
3. Sentiment Analysis: Analyzes recent tweets from the area to determine the overall sentiment, using basic keyword matching for positive, negative, and neutral sentiments.
4. Safety Assessment: Assesses the safety of the location based on the crowd level and tweet sentiment, and sends desktop notifications to the user with a summary of the situation.
5. Automated Notification System: Continuously checks the location and provides updates every 10 minutes.
