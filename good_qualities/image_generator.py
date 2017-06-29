from PIL import ImageFont, Image, ImageDraw, ImageFilter, ImageOps
import os.path, re
import random
import wget
from images import round_img, remove_image, image_colour, get_random_img, opposite_color


def get_random_qualities():
    with open('good_qualities/static/good-qualities.txt') as foo:
        f = foo.read()

    quality = f.strip().split('\n')

    return random.sample(quality, 7)

def user_background(user_image):
    with open('good_qualities/static/images/img_color.txt') as foo:
        f = foo.read()

    img_colour = image_colour(user_image)
    background = f.strip().split('\n')
    l = []

    for i in background:
       if img_colour == i.strip().split('~')[1]:
           l.append(i)
       else:
           get_random_img('good_qualities', 'img_color')
    return random.choice(l)

def draw_line(rotation, img_size=(160,34)):
    is_font =  ImageFont.truetype('good_qualities/static/fonts/Fighting Spirit 2.ttf', 20)
    color = '#fff'
    line = Image.new('L', img_size)
    d = ImageDraw.Draw(line)
    d.text( (0, 0), "---------------",  font=is_font, fill=color)
    w=line.rotate(rotation,  expand=1)
    return w

def generate_quality_image(user_id, user_name, user_image):
    """
    Returns a complete image that could paste on Facebook
    """
    path = 'good_qualities/static/user_image/{}.jpg'.format(user_id)

    if not os.path.exists(path):
        wget.download(user_image, out=path)

    image = Image.open(path).resize((280, 280))
    background = user_background(path)
    color = opposite_color(background.split('~')[1])
    quality = get_random_qualities()
    img = Image.open(background.split('~')[0])
    img.paste(image, (350,130))
    user_font = ImageFont.truetype('good_qualities/static/fonts/Bare Bones.ttf', 17)
    font =  ImageFont.truetype('good_qualities/static/fonts/Bare Bones.ttf', 12)

    img.paste(draw_line(180.1), (185,290), draw_line(180.1))
    img.paste(draw_line((180.1)), (610,290), draw_line(180.1))
    img.paste(draw_line((90.1), (80, 30)), (475,410), draw_line((90.1), (80,30)))
    img.paste(draw_line(45.1), (620,90), draw_line(45.1))
    img.paste(draw_line(145.1), (205,120), draw_line(145.1))
    img.paste(draw_line(30.1), (228,378), draw_line(30.1))
    img.paste(draw_line(145.1), (600,378), draw_line(145.1))

    draw = ImageDraw.Draw(img)
    draw.text((100, 277), quality[0], fill=color,font=font)
    draw.text((760, 275), quality[1], fill=color,font=font)
    draw.text((455, 493), quality[2], fill=color,font=font)
    draw.text((710, 85), quality[3], fill=color,font=font)
    draw.text((150, 118), quality[4], fill=color,font=font)
    draw.text((170,474), quality[5], fill=color, font=font)
    draw.text((715,486), quality[6], fill=color, font=font)
    draw.text((250, 20), "{}'s best qualities".format(user_name), fill=color, font=user_font)

    img.save('good_qualities/static/temp/{}.jpg'.format(user_id))
    image = os.path.abspath('good_qualities/static/temp/{}.jpg'.format(user_id))
    return image

