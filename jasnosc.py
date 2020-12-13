import sys
from PIL import Image
import os

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

i = 0
while i <= 7:#w zaleznosci od ilosci zdjec
    i += 1
    image = Image.open("P ({}).jpg".format(i))
    jasnosc = calculate_brightness(image)
    print(jasnosc)
    if jasnosc < 0.1:
        os.remove("P ({}).jpg".format(i))
