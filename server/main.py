from PIL import Image
import requests
import numpy as np

def map_to_range(num, numMax, _min, _max):
    return int(float(num) / numMax * _max + _min)

def rgb_to_16_bit_color(rgb):
    # image is R5 G6 B5
    # RBG = RRRRRGGGGGGBBBBB
    # R   = 1111100000000000 = 0xF800
    # G   = 0000011111100000 = 0x07E0
    # B   = 0000000000011111 = 0x001F

    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    r = map_to_range(r, 255, 0, 31)
    g = map_to_range(g, 255, 0, 63)
    b = map_to_range(b, 255, 0, 31)

    out = r << 11 | g << 5 | b
    return out

def get_bitmap_from_url(image_url):

    # download image
    img_data = requests.get(image_url).content
    with open('./image.png', 'wb') as handler:
       handler.write(img_data)

    # open
    image = Image.open('./image.png')

    # resize
    resized_image = image.resize((128, 128))
    # resized_image.save('./images/resized-image.png')

    # convert to bitmap array
    bitmap = []
    img_arr = np.array(resized_image)

    for i in range(len(img_arr)): 
        for j in range(len(img_arr)):
            bitmap.append(rgb_to_16_bit_color(img_arr[i][j]))

    return bitmap