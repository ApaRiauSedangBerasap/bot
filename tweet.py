# use python-twitter package : https://github.com/bear/python-twitter
import twitter, sys, os

# I personally use https://github.com/tweepy/tweepy/blob/master/examples/oauth.py to get my access token
consumer_key         = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret      = os.getenv('TWITTER_CONSUMER_SECRET')
access_token_key     = os.getenv('TWITTER_ACCESS_TOKEN_KEY')
access_token_secret  = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

media = open(sys.argv[2], 'rb') if len(sys.argv) > 2 else None
status = api.PostUpdate(sys.argv[1], media=media)
