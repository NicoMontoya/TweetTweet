from decouple import config
from flask import Flask, render_template, request 
from .models import DB, Tweeter, Tweet
from .twitter import add_or_update_tweeter
from .predict import predict_tweeter

def create_app():
    """Create and configure an instance of the flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route("/")
    def root():
        tweeters = Tweeter.query.all()
        return render_template('layout.html', title='Home', tweeters=tweeters)

    @app.route("/tweeter", methods=['POST'])
    @app.route("/tweeter/<handle>", methods=['GET'])
    def tweeter(handle=None, message=''):
        handle = handle or request.values['tweeter_handle']
        try:
            if request.method == 'POST':
                add_or_update_tweeter(handle)
                message = "Tweeter {} succesfully added!".format(handle)
            tweets = Tweeter.query.filter(Tweeter.handle == handle).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(handle, e)
            tweets = []
        return render_template('user.html', title=handle, tweets=tweets, message=message)

    @app.route("/compare", methods=["POST"])
    def compare():
        tweeter1, tweeter2 = request.values['tweeter1'], request.values['tweeter2']
        prediction = predict_tweeter(tweeter1, tweeter2, request.values['tweet_text'])
        return render_template('compare.html', title=tweeter1 if prediction else tweeter2)
        #return tweeter1 if prediction else tweeter2


    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('layout.html', title='DB Reset!', tweeters=[])

    return app