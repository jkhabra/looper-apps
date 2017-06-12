from PIL import ImageFont, Image, ImageDraw, ImageFilter
from ast import literal_eval as make_tuple
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

    image = round_img(path, (230, 230)).filter(ImageFilter.UnsharpMask(radius=2, percent=50, threshold=3))
    #image = Image.open(path).resize((350, 570)).filter(ImageFilter.Blur)
    l = get_random_img('logo', 'logo')
    logo = Image.open(l[0]).resize(make_tuple(l[1]))
    background = get_random_img('images', 'wwe')
    wrestler = get_random_img('wrestlers', 'wrestler')
    #w = Image.open('wwe_match_maker/static/wrestlers/6.png').resize((300,530))
    w = Image.open(wrestler[0]).resize((make_tuple(wrestler[2])))
    color = '#fff'

    img = Image.open(background[0])
    img.paste(image, (50,150), image)
    img.paste(w, (make_tuple(wrestler[3])), w)
    img.paste(logo, (make_tuple(l[2])), logo)
    user_font = ImageFont.truetype('wwe_match_maker/static/fonts/Smack Laideth Down 2016.ttf', 36)
    font =  ImageFont.truetype('wwe_match_maker/static/fonts/Brawl.ttf', 45)

    draw = ImageDraw.Draw(img)
    draw.text((125, 460), 'Once  in  a  lifetime',fill=color,font=font)
    draw.text((70, 410), user_name, fill=color, font=user_font)
    draw.text((605, 405),  wrestler[1], fill=color, font=user_font)

    img.save('wwe_match_maker/static/temp/{}.jpg'.format(user_id))
    image = os.path.abspath('wwe_match_maker/static/temp/{}.jpg'.format(user_id))
    return image

