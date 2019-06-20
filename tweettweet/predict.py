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

    log_reg = LogisticRegression(solver='lbfgs', max_iter=1000).fit(embeddings, labels)

    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    
    predictions = log_reg.predict_proba(np.array(tweet_embedding).reshape(1, -1))[0]
    result = {tweeter1_handle: round(predictions[1]*100, 2),
              tweeter2_handle: round(predictions[0]*100, 2)}
    
    return result
