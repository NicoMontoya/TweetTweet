"""SQL alchemy models for tweettweet"""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Tweeter(DB.Model):
    """Twitter users that we pull and analyze tweets for"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    handle = DB.Column(DB.String(15), nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return "<Tweeter {}>".format(self.handle)

class Tweet(DB.Model):
    """Tweets tweeted from the tweeters"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    embedding = DB.Column(DB.PickleType, nullable=False)
    tweeter_id = DB.Column(DB.BigInteger, DB.ForeignKey('tweeter.id'), nullable=False)
    tweeter = DB.relationship('Tweeter', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return "<Tweet {}>".format(self.text)