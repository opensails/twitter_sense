from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor


import twitter_credentials

# # # # # TWITTER CLIENT # # # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth



# # # # TWITTER STREAMER # # # # #
class TwitterStreamer():
# Class for streaming and processing live tweets

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        #This handles authentication and the connection to the Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        #add a filter
        stream.filter(track=hash_tag_list)   


# # # # TWITTER STREAMER LISTENER # # # # #
class TwitterListener(StreamListener):
#This is a basic listener class that just prints received tweets to stdout.
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
        return True
    
    def on_error(self, status):
        if status == 420:
            #Returning False data method incase data limit occurs
            return False
        print(status)

if __name__ == '__main__':

    hash_tag_list = ["coronavirus", "covid-19", "DoctorsSpeakUp"]
    fetched_tweets_filename = "tweets.txt"

    twitter_client = TwitterClient('charlottejogs')
    print(twitter_client.get_user_timeline_tweets(5))
 #   twitter_streamer = TwitterStreamer()
#  twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)



