from flask import Flask, render_template, redirect, request, session, flash
from os import path
from personality_quotes.app import personality_quote
from wwe_match_maker.app import match_maker
from images import remove_image, get_graph

app = Flask(__name__)

app.config.update(dict(
     DATABASE=path.join(path.dirname(app.root_path), 'db/facebook.db'),
     SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))

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

     links = {'personality': 'personality-quote/confirm-quote', 'wwe': 'match_maker/confirm-pic', 'logout': '/logout'}

     if session['fb_token'] is None:
          flash('Please Login before continue')
     else:
          graph = get_graph()
          profile = graph.get_object('me')
          args = {'fields' : 'id,name,email,picture.width(9999),cover,age_range,gender,link,timezone,updated_time,verified,friends'}
          profile = graph.get_object('me', **args)

          user_id = profile['id']
          user_name = profile['name']
          user_image = profile['picture']['data']['url']
          cover_image = profile['cover']
          age = profile['age_range']
          user_email = profile['email']
          user_profile_link = profile['link']
          timezone = profile['timezone']
          gender = ['gender']
          update_time = profile['updated_time']
          verified  = profile['verified']
          friends = graph.get_connections(id='me', connection_name='friends')
          total_friends = friends['summary']['total_count']

     return render_template('index.html', links=links, login_url=login_url)


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
