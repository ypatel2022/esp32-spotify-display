from PIL import Image
import numpy as np

img = Image.open('./images/resized-image.png')

img_arr = np.array(img)

bitmap = []

# // image is in R5 G6 B5
# // RBG = RRRRRGGGGGGBBBBB
# // R   = 1111100000000000 = 0xF800
# // G   = 0000011111100000 = 0x07E0
# // B   = 0000000000011111 = 0x001F

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
    # print(hex(out), ',', end='')
    

c=0
for i in range(len(img_arr)): 
    for j in range(len(img_arr)):
        rgb_to_16_bit(img_arr[i][j])
        c+=1
print(c)