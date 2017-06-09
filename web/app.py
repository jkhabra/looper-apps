from flask import Flask, render_template, redirect
from personality_quotes.app import personality_quote
from wwe_match_maker.app import match_maker


app = Flask(__name__)
app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))

app.register_blueprint(personality_quote, url_prefix='/personality-quote')
app.register_blueprint(match_maker, url_prefix='/match_maker')

@app.route('/')
def index():
    home= {'personality': 'personality-quote/home', 'wwe': 'match_maker/home'}

    return render_template('index.html',home=home)
