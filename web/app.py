from flask import Flask, render_template, redirect, request, session, jsonify
from .fb import get_graph, get_user_data
import os.path
from .image_generator import generate_quote_image, remove_quote_image
import time

app = Flask(__name__)

app.config.update(dict(SECRET_KEY='A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'))

app_id = "1854877241500808"
redirect_uri = "http://localhost:5000/accept-fb-token"

@app.route('/')
def home():
    login_url = 'https://www.facebook.com/v2.9/dialog/oauth?' \
                + 'client_id=1854877241500808' \
                + '&redirect_uri=http://localhost:5000/accept-fb-token' \
                + '&state=randomstring123' \
                + '&response_type=token' \
                + '&scope=public_profile,publish_actions,user_friends,email'

    session['quote_image'] = None
    remove_quote_image()
    return render_template('index.html', login_url=login_url)


@app.route('/accept-fb-token')
def accept_fb_token():
    if request.args.get('access_token'):
        session['fb_token'] = request.args.get('access_token')

        return redirect('/confirm-quote')

    return render_template('receive_fb_token.html')

@app.route('/confirm-quote')
def confirm_quote():
    data = get_user_data()
    user_id = data['id']
    user_name = data['name']
    user_image = data.get('picture').get('data').get('url')

    if not session.get('quote_image'):
        session['quote_image']= generate_quote_image(user_id, user_name, user_image)
        print(session.get('quote_image'))

    if request.args.get('post_image') == 'no':
        print('REFRESHING QUOTE IMAGE')
        session['quote_image'] = None
        remove_quote_image()

        return redirect('/confirm-quote')

    if request.args.get('post_image') == 'yes':
        graph = get_graph()
        img = graph.put_photo(image=open(session.get('quote_image'), 'rb').read(), message='Find out which quote matches to your personality')

        return redirect('/')

    return render_template('confirm_quote.html', user_id=user_id, random_str=str(time.time()))

