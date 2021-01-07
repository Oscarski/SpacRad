from logzero import logger, logfile
from PIL import Image
import os

minimum_brightness = 0.35 #minimalna jasnosc
photo_amount = 11 #ilosc zdjec

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

logger.info("\tMission started") #poczatek misji

index = 1

while index <= photo_amount:#w zaleznosci od ilosci zdjec
    try:
        nazwa = str(index).zfill(4)
        image = Image.open("spacerad_{}.jpg".format(nazwa))
        jasnosc = calculate_brightness(image)
        info_log = "\tspacerad_{}, ".format(nazwa) + "jasnosc: " + str(jasnosc)
        logger.info(info_log)
        if jasnosc < minimum_brightness:
            os.remove("spacerad_{}.jpg".format(nazwa))
            logger.info("\tUsunieto zdjecie spacerad_{}".format(nazwa))

    except Exception as e:
            logger.error("\t{}: {})".format(e.__class__.__name__, e))
            logger.info("\tNie ma pliku, lub problem z jasnoscia")
    index += 1


