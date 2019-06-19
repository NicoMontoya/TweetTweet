"""Retrieve tweet embeddings and persist in the database"""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, Tweeter

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))

TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET')) 

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_tweeter(username):
    """ adds or updates user and their tweets"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_tweeter = (Tweeter.query.get(twitter_user.id) or
                      Tweeter(id=twitter_user.id, handle=username))
        DB.session.add(db_tweeter)
        tweets = twitter_user.timeline(
            count=250, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_tweeter.newest_tweet_id
        )

        if tweets:
            db_tweeter.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')

            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_tweeter.tweets.append(db_tweet)
            DB.session.add(db_tweet)
            

    except Exception as e:
        # something else
        print("Error processing {}: {}".format(username, e))
        raise e
    else:
        DB.session.commit()

