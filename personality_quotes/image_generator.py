from PIL import ImageFont, Image, ImageDraw
from ast import literal_eval as make_tuple
from bs4 import BeautifulSoup
from requests import get
import os.path, re
import textwrap
import random
import wget
from images import round_img, remove_image


path = os.path.dirname(__file__)
quote_path = os.path.join(path, 'personality_quotes/static/quotes.txt')
secure_random = random.SystemRandom()

def get_random_img():
    """
    Returns a random background image
    """
    with open('personality_quotes/static/images/img_color.txt', 'r') as foo:
        f = foo.read()

    image = f.strip().split('\n')
    l = []

    for i in image:
        l.append(i.strip().split('~'))

    return secure_random.choice(l)

def opposite_color(color):
    if color == 'white' or color == 'snow'  or color == 'silver':
        return '#000000'
    if color == 'olive':
        return '#9d6da7'
    else:
        return '#FFFFFF' #'#ffb5da'


def quote_scraper(link='https://www.goodreads.com'):
    """
    Returns a list of quotes
    # base url is https://www.goodreads.com
    """
    soup = BeautifulSoup(get(link).content, 'html.parser')
    raw_data = soup.select('.quoteText')
    quotes = []

    for i in raw_data:
        quote = i.text.strip().split('\n')
        print('downloading quotes........')
        if len(quote[0]) <= 180:
            quotes.append(quote[0]+'~')

    with open(quote_path, 'a+') as foo:
        for i in quotes:
            w = foo.write(i)


def random_quote(quote_path='personality_quotes/static/quotes.txt'):
    """
    Returns a random quote from text file
    """
    with open(quote_path) as foo:
        quote = foo.read()

    random_quote = quote.strip().split('~')
    text = secure_random.choice(random_quote)

    if len(text) <= 75:
        t = textwrap.wrap(text, 75)
        return '\n\t'.join(t)
    elif len(text) <= 130:
        t = textwrap.wrap(text, 60)
        return '\n\t'.join(t)
    else:
        t = textwrap.wrap(text, 55)
        return '\n\t'.join(t)

def generate_quote_image(user_id, user_name, user_image):
    """
    Returns a complete image that could paste on Facebook
    """
    profile_id = user_id[2:]
    path = 'personality_quotes/static/user_image/{}.jpg'.format(profile_id)

    if not os.path.exists(path):
        wget.download(user_image, out=path)

    image = round_img(path)

    background = get_random_img()
    image_dimension = make_tuple(background[2])
    defines_dimension = make_tuple(background[3])
    name_dimension = make_tuple(background[4])
    quote_dimension = make_tuple(background[5])
    color = opposite_color(background[1])

    img = Image.open(background[0])
    img.paste(image, (image_dimension), image)
    f = 'personality_quotes/static/fonts/OstrichSans-Black.ttf'
    font = ImageFont.truetype(f, 35)
    font_for_user = ImageFont.truetype(f, 27)

    draw = ImageDraw.Draw(img)
    draw.text((defines_dimension), 'Quote that Describes', fill=color, font=ImageFont.truetype(f, 22) )
    draw.text((name_dimension), user_name, fill=color, font=font_for_user)
    draw.text((quote_dimension), random_quote(), fill=color, font=font)

    img.save('personality_quotes/static/tem/{}.jpg'.format(user_id))
    image = os.path.abspath('personality_quotes/static/tem/{}.jpg'.format(user_id))
    return image

