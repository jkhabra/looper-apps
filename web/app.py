from flask import Flask, render_template, redirect, request, session, jsonify
from .fb import get_graph, get_user_data
import os.path
from .image_generator import generate_image, user_img

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

    return render_template('index.html', login_url=login_url)


@app.route('/accept-fb-token')
def accept_fb_token():
    return render_template('receive_fb_token.html')

@app.route('/confirm-quote')
def confirm_quote():
    token = None

    if request.args.get('access_token'):
        token = request.args.get('access_token')
        session['fb_token'] = token

        return redirect('/confirm-quote')
    data = get_user_data()
    user_name = data['name']
    image_data = data.get('picture').get('data')
    user_image = user_img(image_data['url'])
    image = generate_image(user_name, user_image)

    if request.args.get('post_image') == 'yes':
        graph = get_graph()
        img = graph.put_photo(image=open(image, 'rb').read(), message='Find out which quote matches to your personality')
   # if request.args.get('post_image') == 'no':
        #return render_template('receive_fb_token.html')
    #    return redirect('/confirm-quote')
    return render_template('confirm_quote.html', quote_image=image)
