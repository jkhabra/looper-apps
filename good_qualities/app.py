from flask import Blueprint, render_template, redirect, request, session, jsonify, flash
import os.path
from .image_generator import generate_quality_image
import time
from images import get_graph, remove_image

good_qualities  = Blueprint('good_qualities', __name__, template_folder='templates', static_folder='static')

@good_qualities.route('/confirm-pic')
def confirm_quote():
    remove_image('good_qualities/static/temp')
    session['quality_image'] = None

    try:
        graph = get_graph()
        profile = graph.get_object('me')
        args = {'fields' : 'id,name,email,picture.width(9999)'}
        profile = graph.get_object('me', **args)

        user_id = profile['id']
        user_name = profile['name']
        user_image = profile['picture']['data']['url']

        if not session.get('quality_image'):
            session['quality_image']= generate_quality_image(user_id, user_name, user_image)
            print(session.get('quality_image'))

        if request.args.get('post_image') == 'no':
            print('REFRESHING QUALITY IMAGE')
            session['quality_image'] = None
            remove_image()

            return redirect('good_qualities/confirm-pic')

        if request.args.get('post_image') == 'yes':
            img = graph.put_photo(image=open(session.get('quality_image'), 'rb').read(), message='Find out which kind of qualities people see in you')
            session['post_id'] = img['id']
            flash('Your post has been posted to your profile')
            return redirect('good_qualities/success')

    except Exception as error:
        session['fb_token'] = None
        return redirect('/')

    return render_template('good_qualities/confirm_quote.html', user_id=user_id, random_str=str(time.time()))


@good_qualities.route('/success')
def success():
    graph = get_graph()
    profile = graph.get_object('me')
    user_id = profile['id']

    if request.args.get('post_image') == 'again':
        return redirect('good_qualities/confirm-pic?post_image=no')

    return render_template('good_qualities/success.html', user_id=user_id, post_id=session.get('post_id'), random_str=str(time.time()))
