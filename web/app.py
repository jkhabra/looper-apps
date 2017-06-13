from flask import Flask, render_template, redirect, request, session
from personality_quotes.app import personality_quote
from wwe_match_maker.app import match_maker


app = Flask(__name__)
app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))

app.register_blueprint(personality_quote, url_prefix='/personality-quote')
app.register_blueprint(match_maker, url_prefix='/match_maker')


app_id = "1854877241500808"
redirect_uri = 'http://localhost:5000/accept-fb-token'


@app.route('/')
def index():
     login_url = 'https://www.facebook.com/v2.9/dialog/oauth?' \
                + 'client_id=1854877241500808' \
                + '&redirect_uri=' + redirect_uri \
                + '&state=randomstring123' \
                + '&response_type=token' \
                + '&scope=public_profile,publish_actions,user_friends,email'
     home= {'personality': 'personality-quote/confirm-quote', 'wwe': 'match_maker/confirm-pic', 'logout': '/logout'}

     return render_template('index.html', home=home, login_url=login_url)


@app.route('/accept-fb-token')
def accept_fb_token():
    if request.args.get('access_token'):
        session['fb_token'] = request.args.get('access_token')

        return redirect('/')

    return render_template('fb-token.html')


@app.route('/logout')
def logout():
     session['fb_token'] = None
     return redirect('/')
