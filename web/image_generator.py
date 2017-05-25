from PIL import ImageFont, Image, ImageDraw, ImageColor
from bs4 import BeautifulSoup
from requests import get
import random
import textwrap
import re
import os.path

path = os.path.dirname(__file__)
quote_path = os.path.join(path, 'static/quotes.txt')
secure_random = random.SystemRandom()

def quote_scraper(link):
    """
    Returns a list of quotes
    # base url is https://www.goodreads.com
    """
    soup = BeautifulSoup(get(link).content, 'html.parser')
    raw_data = soup.select('.quoteText')
    quotes = []

    for i in raw_data:
        quote = i.text.strip().split('\n')
        quotes.append(quote[0]+'~')

    with open(quote_path, 'a+') as foo:
        for i in quotes:
            w = foo.write(i)

def image_size(image):
    """
    Return resized image
    """
    size = 550, 350
    img = image

    try:
        im = Image.open(image)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(img)
    except IOError:
        print("cannot create thumbnail")

def resize_all_img():
    """
    Resize all images that in folder
    """
    img_path = os.path.join(path, 'static/images/')
    image = os.listdir(img_path)

    for i in image:
        if i.endswith('.jpg') or i.endswith('.png'):
            image_size(img_path+i)
    print('<<<<<<<<<<<<<<<<<Everything is done here>>>>>>>>>>>>>>>>>>>')

def random_img():
    """
    Returns a random background image
    """
    img_path = os.path.join(path, 'static/images/')
    image = secure_random.choice(os.listdir(img_path))

    if image.endswith('.jpg') or image.endswith('.png'):
        return img_path + image
    else:
        return random_img()

def random_quote():
    """
    Returns a random quote from text file
    """
    with open(quote_path) as foo:
        quote = foo.read()

    random_quote = quote.strip().split('~')
    return '\n'.join(line.strip() for line in re.findall(r'.{1,26}(?:\s+|$)', secure_random.choice(random_quote)))
    # return textwrap.fill(secure_random.choice(random_quote), 35)

def generate_image(user):
    """
    Returns a complete image that could paste on Facebook
    """
    user_image = Image.open('web/q1.jpg')
    resize = user_image.resize((150, 120))
    background = random_img()

    img = Image.open(background)
    img.paste(resize, (20, 20))
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 23)
    draw = ImageDraw.Draw(img)
    draw.text((25, 153), user, fill='black', font=font)
    draw.text((250,10), random_quote(), fill='black', font=font)
    img.save('sample.jpg')
