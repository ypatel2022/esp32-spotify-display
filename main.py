from PIL import Image
import requests
import numpy as np

# download image
image_url = 'https://i.scdn.co/image/ab67616d00001e02715973050587fe3c93033aad'
img_data = requests.get(image_url).content
with open('./images/src-image.png', 'wb') as handler:
    handler.write(img_data)

# open
image = Image.open('./images/src-image.png')

# resize
resized_image = image.resize((128, 128))
resized_image.save('./images/resized-image.png')

# convert to bitmap array
def map_to_range(num, numMax, _min, _max):
    return int(float(num) / numMax * _max + _min)

def rgb_to_16_bit(rgb):

    r = rgb[0]
    g = rgb[1]
    b = rgb[2]

    r = map_to_range(r, 255, 0, 31)
    g = map_to_range(g, 255, 0, 63)
    b = map_to_range(b, 255, 0, 31)

    out = r << 11 | g << 5 | b
    return out


bitmap = []
img_arr = np.array(resized_image)


for i in range(len(img_arr)): 
    for j in range(len(img_arr)):
        bitmap.append(rgb_to_16_bit(img_arr[i][j]))

print(bitmap)