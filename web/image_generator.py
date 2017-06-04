from PIL import ImageFont, Image, ImageDraw, ImageColor, ImageOps
from ast import literal_eval as make_tuple
from bs4 import BeautifulSoup
from requests import get
import os.path, re
import random
import textwrap
import wget
import webcolors

path = os.path.dirname(__file__)
quote_path = os.path.join(path, 'static/quotes.txt')
secure_random = random.SystemRandom()

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
    with open('web/static/images/img_color.txt', 'r') as foo:
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

def random_quote():
    """
    Returns a random quote from text file
    """
    with open(quote_path) as foo:
        quote = foo.read()

    random_quote = quote.strip().split('~')
    text = secure_random.choice(random_quote)

    if len(text) <= 85:
        t = textwrap.wrap(text, 85)
        return '\n\t'.join(t)
    elif len(text) <= 130:
        t = textwrap.wrap(text, 60)
        return '\n\t'.join(t)
    else:
        t = textwrap.wrap(text, 55)
        return '\n\t'.join(t)

def round_img(image):
    im = Image.open(image)
    im = im.resize((100, 100));
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

def generate_quote_image(user_id, user_name, user_image):
    """
    Returns a complete image that could paste on Facebook
    """
    profile_id = user_id[2:]
    path = 'web/static/user_image/{}.jpg'.format(profile_id)

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
    font = ImageFont.truetype('web/static/fonts/OstrichSans-Black.ttf', 30)
    font_for_user = ImageFont.truetype('web/static/fonts/OstrichSans-Black.ttf', 25)

    draw = ImageDraw.Draw(img)
    draw.text((defines_dimension), 'Quote that Describes', fill=color, font=ImageFont.truetype('web/static/fonts/OstrichSans-Black.ttf', 22) )
    draw.text((name_dimension), user_name, fill=color, font=font_for_user)
    draw.text((quote_dimension), random_quote(), fill=color, font=font)

    img.save('web/static/tem/{}.jpg'.format(user_id))
    image = os.path.abspath('web/static/tem/{}.jpg'.format(user_id))
    return image

def remove_quote_image(folder='web/static/tem'):
    pattern = '.jpg'
    folder = os.path.abspath(folder)
    try:
        for f in os.listdir(folder):
            if re.search(pattern, f):
                os.remove(os.path.join(folder, f))
    except Exception as error:
        print('File does not exist {}'.format(error))
