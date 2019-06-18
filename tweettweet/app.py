from decouple import config
from flask import Flask, render_template, request 
from .models import DB, Tweeter

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

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('layout.html', title='DB Reset!', tweeters=[])

    return app