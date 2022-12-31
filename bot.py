import discord
import tweepy
import os
from dotenv import load_dotenv

DISCORD_API_KEY = os.getenv("DISCORD_API_KEY")

client = discord.Client()

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

user = os.getenv("TWITTER_USERNAME")

auth = tweepy.OAuth1UserHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

latest_tweet = None


@client.event
async def on_ready():
    tweets = twitter_api.user_timeline(screen_name=user)

    global latest_tweet
    latest_tweet = tweets[0]

    channel = client.get_channel() # Replace with the ID of the channel you want to send the message to
    await channel.send(latest_tweet.text)

@tasks.loop(seconds=10)
async def check_tweets():
    tweets = twitter_api.user_timeline(screen_name=user)

    latest_tweet_new = tweets[0]

    global latest_tweet
    if latest_tweet_new != latest_tweet:
        channel = client.get_channel() 
        await channel.send(latest_tweet_new.text)

        latest_tweet = latest_tweet_new

check_tweets.start()

client.run(DISCORD_API_KEY)