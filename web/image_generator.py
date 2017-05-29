from PIL import ImageFont, Image, ImageDraw, ImageColor
from bs4 import BeautifulSoup
from requests import get
import random
import textwrap
import re
import os.path
import wget
import webcolors

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
    size = 560, 450
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

    with open('web/static/images/img_color.txt', 'w') as foo:
        f = foo.write('\n'.join('{}~{}'.format(*x) for x in img_list))
    print('<<<<<<<<<<<<<<<<<<<<Work is done here>>>>>>>>>>>>>>>')

def get_random_img():
    """
    Returns a random background image
    """
    with open('web/static/images/img_color.txt', 'r') as foo:
        f = foo.read()

    image = f.split('\n')
    l = []

    for i in image:
        t = i.split('~')
        l.append((t[0], t[1]))

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

    closest_name = rgb_to_hex(rgb_colour)
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
        comp = ['%02X' % (255 - int(a, 16)) for a in rgb]
        return '#' + ''.join(comp)
    return hex

def random_quote():
    """
    Returns a random quote from text file
    """
    with open(quote_path) as foo:
        quote = foo.read()

    random_quote = quote.strip().split('~')
    #return '\n'.join(line.strip() for line in re.findall(r'.{1,26}(?:\s+|$)', secure_random.choice(random_quote)))
    return textwrap.fill(secure_random.choice(random_quote), 25)

def generate_image(user_name, user_image):
    """
    Returns a complete image that could paste on Facebook
    """
    user_image = Image.open('web/static/tem/user.jpg')
    resize = user_image.resize((150, 120))
    background = get_random_img()

    img = Image.open(background[0])
    img.paste(resize, (20, 20))
    font = ImageFont.truetype('web/static/fonts/helvetica-normal.ttf', 25)
    #font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 23)
    draw = ImageDraw.Draw(img)
    draw.text((20, 153), user_name, fill=background[1], font=font)
    draw.text((250,10), random_quote(), fill=background[1], font=font)
    img.save('web/static/tem/sample.jpg')
    image = os.path.abspath('web/static/tem/sample.jpg')
    return image

def user_img(url):
     wget.download(url, out= 'web/static/tem/user'+'.jpg')
