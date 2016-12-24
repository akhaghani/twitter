import sys, time
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
tweet_count=1000  #number of tweets you want to pull

def get_twitter_client():  #insert keys from Twitter
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_secret = ""
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

class CustomListener(StreamListener):
    def __init__(self, fname):
        self.outfile = "%s.jsonl" % fname

    def on_data(self, data):
        global tweet_count
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                tweet_count=tweet_count-1
        except BaseException as e:
            sys.stderr.write("Error on_data: {}\n".format(e))
            time.sleep(5)
        if tweet_count<1:
            sys.exit("Done")
            return False
        else:
            return True

    def on_error(self, status):
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n".format(status))
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True

query = ["", ""] #insert hashtags, twitter handles and/or keywords within "" seperated by commas

auth = get_twitter_client()
twitter_stream = Stream(auth, CustomListener("")) #place output file name between ""
twitter_stream.filter(track=query, async=True)
