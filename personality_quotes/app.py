from flask import Blueprint, render_template, redirect, request, session, jsonify, flash
import os.path
from .image_generator import generate_quote_image
import time
from images import remove_image, get_graph

personality_quote  = Blueprint('personality_quote', __name__, template_folder='templates', static_folder='static')


@personality_quote.route('/confirm-quote')
def confirm_quote():
    remove_image()
    session['quote_image'] = None

    graph = get_graph()
    profile = graph.get_object('me')
    args = {'fields' : 'id,name,email,picture.width(9999)' }
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
        remove_image()

        return redirect('personality-quote/confirm-quote')

    if request.args.get('post_image') == 'yes':
        img = graph.put_photo(image=open(session.get('quote_image'), 'rb').read(), message='Find out which quote matches to your personality')
        session['post_id'] = img['id']

        flash('Your post has been posted to your profile')
        return redirect('personality-quote/success')

    return render_template('personality_quote/confirm_quote.html', user_id=user_id, random_str=str(time.time()))


@personality_quote.route('/success')
def success():
    graph = get_graph()
    profile = graph.get_object('me')
    user_id = profile['id']

    if request.args.get('post_image') == 'again':
        return redirect('personality-quote/confirm-quote?post_image=no')

    return render_template('personality_quote/success.html', user_id=user_id, post_id=session.get('post_id'), random_str=str(time.time()))
