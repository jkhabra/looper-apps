from flask import Flask, render_template, redirect, request, session, jsonify, flash
from .fb import get_graph, get_user_data
import os.path
from .image_generator import generate_quote_image, remove_quote_image
import time

app = Flask(__name__)

app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))

app_id = "1854877241500808"
redirect_uri = 'https://looperapps.herokuapp.com/accept-fb-token'

@app.route('/')
def home():
    login_url = 'https://www.facebook.com/v2.9/dialog/oauth?' \
                + 'client_id=1854877241500808' \
                + '&redirect_uri=' + redirect_uri \
                + '&state=randomstring123' \
                + '&response_type=token' \
                + '&scope=public_profile,publish_actions,user_friends,email'

    session['quote_image'] = None
    remove_quote_image()
    remove_quote_image('web/static/user_image')
    return render_template('index.html', login_url=login_url)


@app.route('/accept-fb-token')
def accept_fb_token():
    if request.args.get('access_token'):
        session['fb_token'] = request.args.get('access_token')

        return redirect('/confirm-quote')

    return render_template('receive_fb_token.html')

@app.route('/confirm-quote')
def confirm_quote():
    graph = get_graph()
    profile = graph.get_object('me')
    args = {'fields' : 'id,name,email,picture.width(9999)', }
    profile = graph.get_object('me', **args)

    user_id = profile['id']
    user_name = profile['name']
    user_image = profile['picture']['data']['url']

    if not session.get('quote_image'):
        session['quote_image']= generate_quote_image(user_id, user_name, user_image)
        print(session.get('quote_image'))

    if request.args.get('post_image') == 'no':
        print('REFRESHING QUOTE IMAGE')
        session['quote_image'] = None
        remove_quote_image()

        return redirect('/confirm-quote')

    if request.args.get('post_image') == 'yes':
        img = graph.put_photo(image=open(session.get('quote_image'), 'rb').read(), message='Find out which quote matches to your personality')
        session['post_id'] = img['id']
        flash('Your post has been posted to your profile')
        return redirect('/success')

    return render_template('confirm_quote.html', user_id=user_id, random_str=str(time.time()))


@app.route('/success')
def success():
    graph = get_graph()
    profile = graph.get_object('me')
    user_id = profile['id']

    if request.args.get('post_image') == 'again':
        return redirect('/confirm-quote?post_image=no')

    return render_template('success.html', user_id=user_id, post_id=session.get('post_id'), random_str=str(time.time()))
