from flask import Blueprint, render_template, redirect, request, session, jsonify, flash
import os.path
from .image_generator import generate_wwe_image
import time
from images import get_graph, remove_image

match_maker  = Blueprint('match_maker', __name__, template_folder='templates', static_folder='static')

@match_maker.route('/confirm-pic')
def confirm_quote():
    graph = get_graph()
    profile = graph.get_object('me')
    args = {'fields' : 'id,name,email,picture.width(9999),friends'}
    profile = graph.get_object('me', **args)

    user_id = profile['id']
    user_name = profile['name']
    user_image = profile['picture']['data']['url']

    if not session.get('wwe_image'):
        session['wwe_image']= generate_wwe_image(user_id, user_name, user_image)
        print(session.get('wwe_image'))

    if request.args.get('post_image') == 'no':
        print('REFRESHING QUOTE IMAGE')
        session['wwe_image'] = None
        remove_image()

        return redirect('match_maker/confirm-pic')

    if request.args.get('post_image') == 'yes':
        img = graph.put_photo(image=open(session.get('wwe_image'), 'rb').read(), message='Find out which wwe star matches to  personality')
        session['post_id'] = img['id']
        flash('Your post has been posted to your profile')
        return redirect('match_maker/success')

    return render_template('match_maker/confirm_quote.html', user_id=user_id, random_str=str(time.time()))


@match_maker.route('/success')
def success():
    graph = get_graph()
    profile = graph.get_object('me')
    user_id = profile['id']

    if request.args.get('post_image') == 'again':
        return redirect('match_maker/confirm-pic?post_image=no')

    return render_template('match_maker/success.html', user_id=user_id, post_id=session.get('post_id'), random_str=str(time.time()))
