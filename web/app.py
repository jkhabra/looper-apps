from flask import Flask, render_template, redirect, request
import os.path
import facebook

from .image_generator import generate_image


app = Flask(__name__)

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
        app.config['fb_token'] = token

        return redirect('/confirm-quote')

    image = generate_image('yo')

    if request.post_image == 'yes':
        graph = facebook.GraphAPI(access_token=token)
        # post = graph.put_object(parent_object='me', connection_name='feed', message='Hello!')
        img_path = os.path.dirname(__file__)
        image = os.path.join(img_path, './static/images/45.jpg')
        img = graph.put_photo(image=open(image, 'rb').read(), message='Look at this cool flash drive!')

    return render_template('confirm_quote.html')
