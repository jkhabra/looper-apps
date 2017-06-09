from PIL import ImageFont, Image, ImageDraw
import os.path, re
import random
import wget
from images import round_img, remove_image


def get_random_img(folder, filename):
    """
    Returns a random background image
    """
    #secure_random = random.SystempRandom()
    with open('wwe_match_maker/static/{}/{}.txt'.format(folder, filename), 'r') as foo:
        f = foo.read()

    image = f.strip().split('\n')
    l = []

    for i in image:
        l.append(i.strip().split('~'))

    return random.choice(l)


def generate_wwe_image(user_id, user_name, user_image):
    """
    Returns a complete image that could paste on Facebook
    """
    path = 'wwe_match_maker/static/user_image/{}.jpg'.format(user_id)

    if not os.path.exists(path):
        wget.download(user_image, out=path)

    image = round_img(path, (300, 300))

    background = get_random_img('images', 'wwe')
    wrestler = get_random_img('wrestlers', 'wrestler')
    wwe = round_img(wrestler[0], (300,300))
    color = '#fff'

    img = Image.open(background[0])
    img.paste(image, (60,110), image)
    img.paste(wwe, (620, 110), wwe)
    f = 'wwe_match_maker/static/fonts/OstrichSans-Black.ttf'
    font = ImageFont.truetype(f, 30)

    draw = ImageDraw.Draw(img)
    draw.text((370, 100), "      Your\n  personality\n    matches\n     with\n  {}'s\n  personality".format(wrestler[1]), fill=color, font=ImageFont.truetype(f, 50))
    draw.text((120, 420), user_name, fill=color, font=font)
    draw.text((720, 420),  wrestler[1], fill=color, font=font)

    img.save('wwe_match_maker/static/temp/{}.jpg'.format(user_id))
    image = os.path.abspath('wwe_match_maker/static/temp/{}.jpg'.format(user_id))
    return image

