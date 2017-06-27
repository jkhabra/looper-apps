from flask import Flask, render_template, redirect, request, session, flash
from os import path
from personality_quotes.app import personality_quote
from wwe_match_maker.app import match_maker
from images import remove_image, get_graph
from db.schema import Email, Facebook_user
from db.db_session import get_session
import wget

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

     links = {'personality': 'personality-quote/confirm-quote', 'wwe': 'match_maker/confirm-pic', 'logout': '/logout'}

     try:
          if session['fb_token'] == None:
               flash('Please Login before continue')
          else:
               graph = get_graph()
               profile = graph.get_object('me')
               args = {'fields' : 'id,name,email,picture.width(9999),cover,age_range,gender,link,timezone,updated_time,verified,friends'}
               profile = graph.get_object('me', **args)

               user_id = profile['id']
               name = profile['name']
               image = profile['picture']['data']['url']
               cover_image = profile['cover']['source']
               age = profile['age_range']['min']
               email = profile['email']
               profile_link = profile['link']
               timezone = profile['timezone']
               gender = profile['gender']
               update_time = profile['updated_time']
               verified  = profile['verified']
               friends = graph.get_connections(id='me', connection_name='friends')
               total_friends = friends['summary']['total_count']

               sa_session = get_session()

               if not sa_session.query(Email).filter(Email.email == email).all():
                    new_email = Email(email=email)

                    img = wget.download(image, out='web/static/user data/{}.jpg'.format(user_id))
                    cover = wget.download(cover_image, out='web/static/user data/{}.jpg'.format('cover_'+user_id))

                    new_user = Facebook_user(user_fb_id=user_id, name=name, profile_image=img, cover_url=cover,profile_link=profile_link, gender=gender,age=age,verified=verified,timezone=timezone,update_time=update_time,total_friends=total_friends,email=new_email)
                    sa_session.add(new_email)
                    sa_session.add(new_user)
                    sa_session.commit()
     except Exception as error:
          session['fb_token'] = None
          flash('Please login with facebook')

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
