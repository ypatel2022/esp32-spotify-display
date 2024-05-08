from PIL import Image
import requests
import numpy as np

# download image
image_url = 'https://i.scdn.co/image/ab67616d00001e02072e9faef2ef7b6db63834a3'
img_data = requests.get(image_url).content
with open('./images/src-image.png', 'wb') as handler:
    handler.write(img_data)

# open
image = Image.open('./images/src-image.png')

# resize
resized_image = image.resize((128, 128))
resized_image.save('./images/resized-image.png')

# convert to 16 bit
image16B = resized_image.convert(mode='P', palette=Image.ADAPTIVE,colors=16)
image16B.save('./images/image16B.bmp')


# convert to bmp
# bmp_image = image16B.tobitmap(name='bitmap')

# bmp_image.save('./images/final-image.bmp')