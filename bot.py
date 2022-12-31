import discord
from discord.ext import tasks
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_API_KEY = os.getenv("DISCORD_API_KEY")

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

user = os.getenv("TWITTER_USERNAME")

auth = tweepy.OAuth1UserHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

latest_tweet = None

class MyClient(discord.Client):
    # The function that will be called when the bot is ready
    async def on_ready(self):
        print('Logged on as', self.user)
        tweets = twitter_api.user_timeline(screen_name=user)

        global latest_tweet
        latest_tweet = tweets[0]

        channel = client.get_channel(1058776614680416266) # Replace with the ID of the channel you want to send the message to
        await channel.send('https://twitter.com/twitter/statuses/' + str(latest_tweet.id))
    # A hook that will be called when the bot is ready
    async def setup_hook(self) -> None:
        self.check_tweets.start()
    

    @tasks.loop(seconds=10)
    async def check_tweets(self):
        tweets = twitter_api.user_timeline(screen_name=user)

        latest_tweet_new = tweets[0]

        global latest_tweet
        if latest_tweet_new != latest_tweet:
            channel = client.get_channel(1058776614680416266) 
            print('New tweet!')
            await channel.send(latest_tweet_new.text)

            latest_tweet = latest_tweet_new
        else:
            print('No new tweet')
    @check_tweets.before_loop
    async def before_check_tweets(self):
        await self.wait_until_ready()
        print('Finished waiting')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run(DISCORD_API_KEY)