from flask import session
import facebook
import json

def get_user_data():
    if not session.get('fb_token'):
        raise Exception('FB Access token is not set on session.')

    token = session.get('fb_token')
    url = 'https://graph.facebook.com/me?access_token={}&fields=id,name,picture.width(9999)'.format(token)

    data = facebook.requests.get(url).content

    return json.loads(data)

def get_graph():
    if not session.get('fb_token'):
        raise Exception('FB Access token is not set on session.')

    token = session.get('fb_token')
    graph = facebook.GraphAPI(access_token=token)

    return graph
