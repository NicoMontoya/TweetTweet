"""Prediction of users based on tweet embeddings"""
import numpy as np  
from sklearn.linear_model import LogisticRegression
from .models import Tweeter
from .twitter import BASILICA

def predict_tweeter(tweeter1_handle, tweeter2_handle, tweet_text):
    tweeter1 = Tweeter.query.filter(Tweeter.handle == tweeter1_handle).one()
    tweeter2 = Tweeter.query.filter(Tweeter.handle == tweeter2_handle).one()
    tweeter1_embeddings = np.array([tweet.embedding for tweet in tweeter1.tweets])
    tweeter2_embeddings = np.array([tweet.embedding for tweet in tweeter2.tweets])
    embeddings = np.vstack([tweeter1_embeddings, tweeter2_embeddings])
    labels = np.concatenate([np.ones(len(tweeter1.tweets)),
                             np.zeros(len(tweeter2.tweets))])

    log_reg = LogisticRegression().fit(embeddings, labels)

    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
