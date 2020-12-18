from logzero import logger, logfile
from PIL import Image
import os

minimum_brightness = 0.35 #minimalna jasnosc
photo_amount = 6 #ilosc zdjec

# czyta i zapisuje sciezke tam gdzie jest main.py
dir_path = os.path.dirname(os.path.realpath(__file__))

# tworzy logfile
logfile(dir_path + "/spacerad.csv")


def calculate_brightness(image):
    greyscale = image.convert('L')
    histogram = greyscale.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (index - scale)
    if brightness == 255:
        return 1
    else:
        return brightness / scale

logger.info("Mission started") #poczatek misji

index = 0

while index <= photo_amount:#w zaleznosci od ilosci zdjec
    try:
        index += 1
        image = Image.open("P{}.jpg".format(index))
        jasnosc = calculate_brightness(image)
        print("Zdjecie {}:".format(index), jasnosc)
        if jasnosc < minimum_brightness:
            os.remove("P{}.jpg".format(index))
    except Exception as e:
            logger.error("{}: {})".format(e.__class__.__name__, e))
            logger.info("\tNie ma pliku, lub problem z jasnoscia")


