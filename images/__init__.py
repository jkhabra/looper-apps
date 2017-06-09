from PIL import ImageFont, Image, ImageDraw, ImageColor, ImageOps
from flask import session
import facebook
import webcolors
import os, re
import random

path = os.path.dirname(__file__)
quote_path = os.path.join(path, 'personality_quotes/static/quotes.txt')
secure_random = random.SystemRandom()

def image_size(image):
    """
    Return resized image
    """
    size = 1000, 1080
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

def img_file():
    """
    Create a file that contain background image with their color
    """
    img_path = os.path.join(path, 'static/images/')
    resize_all_img()
    image = os.listdir(img_path)
    img_list = []

    for i in image:
        print(i)
        if i.endswith('.jpg') or i.endswith('.png'):
            t = (img_path+i, image_colour(img_path+i))
            img_list.append(t)

    with open('web/static/images/img_color.txt', 'a+') as foo:
        f = foo.write('\n'.join('{}~{}'.format(*x) for x in img_list))
    print('<<<<<<<<<<<<<<<<<<<<Work is done here>>>>>>>>>>>>>>>')

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

def image_colour(img):
    """
    Returns RGB colours of the image
    """
    img = Image.open(img)
    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0

    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            r_total += r
            g_total += g
            b_total += b
            count += 1

    rgb_colour  = (r_total/count, g_total/count, b_total/count)

    #closest_name = rgb_to_hex(rgb_colour)
    closest_name = get_colour_name(rgb_colour)
    return closest_name


def get_colour_name(rgb_colour):
    """
    Returns the name of RGB colour
    """
    min_colours = {}
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - rgb_colour[0]) ** 2
        gd = (g_c - rgb_colour[1]) ** 2
        bd = (b_c - rgb_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def rgb_to_hex(rgb):
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])

    my_hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
    if my_hex[0] == '#':
        my_hex = my_hex[1:]
        rgb = (my_hex[0:2], my_hex[2:4], my_hex[4:6])
        #rgb = (r,g,b)
        comp = ['%02X' % (290 - int(a, 16)) for a in rgb] #255,16
        return '#' + ''.join(comp)
    return hex

def opposite_color(color):
    if color == 'white' or color == 'snow'  or color == 'silver':
        return '#000000'
    if color == 'olive':
        return '#9d6da7'
    else:
        return '#FFFFFF' #'#ffb5da'

def round_img(image, t=(100,100)):
    im = Image.open(image)
    im = im.resize(t);
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    return im
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('web/static/tem/{}.png'.format(user_id))

def remove_image(folder='personality_quotes/static/tem'):
    pattern = '.jpg'
    folder = os.path.abspath(folder)
    try:
        for f in os.listdir(folder):
            if re.search(pattern, f):
                os.remove(os.path.join(folder, f))
    except Exception as error:
        print('File does not exist {}'.format(error))

def get_graph():
    if not session.get('fb_token'):
        raise Exception('FB Access token is not set on session.')

    token = session.get('fb_token')
    graph = facebook.GraphAPI(access_token=token)

    return graph
