############################################################################
# Team SpaceRad
# Researchers: Oskar, Błażej, Dawid
# Team from Poland
# Thanks to SpaceWombats team
# https://github.com/jpalau-edu/AstroPi1920
############################################################################

# PL - biblioteki
# ENG - libraries
from picamera import PiCamera
from time import sleep
import ephem
from logzero import logger, logfile
from PIL import Image
from datetime import datetime
from datetime import timedelta
import os

# PL - Zmienne globalne
# ENG - Global variables
minimum_brightness = 0.34  # PL - minimalna jasnosc   ENG - minimum brightness
mission_time = 175  # docelowo 175
dir_path = os.path.dirname(os.path.realpath(__file__))
photo_counter = 1

# PL - tworzy logfile
# ENG - creates a logfile
logfile(dir_path + "/spacerad.csv")

# PL - poczatek czasu misji
# ENG - start of mission time
start_time = datetime.now()
now_time = datetime.now()  # PL - uzyte w petli koncowej    ENG - used in the final loop

# PL - ustawienia kamery
# ENG - camera settings
camera = PiCamera()
camera.resolution = (2592, 1944)  

# PL - Najnowsze dane TLE dla lokalizacji
# ENG - Latest TLE data for location
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20316.41516162  .00001589  00000+0  36499-4 0  9995"
line2 = "2 25544  51.6454 339.9628 0001882  94.8340 265.2864 15.49409479254842"
iss = ephem.readtle(name, line1, line2)


# PL - Funkcja zapisująca szerokość / długość geograficzną do danych EXIF ​​dla zdjęć
# ENG - Function that saves latitude / longitude to EXIF data for photos
def get_latlon():
    iss.compute()
    long_value = [float(i) for i in str(iss.sublong).split(":")]
    if long_value[0] < 0:
        long_value[0] = abs(long_value[0])
        camera.exif_tags['GPS.GPSLongitudeRef'] = "W"
        direction1 = "W"
    else:
        camera.exif_tags['GPS.GPSLongitudeRef'] = "E"
        direction1 = "E"
    camera.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (long_value[0], long_value[1], long_value[2] * 10)
    lat_value = [float(i) for i in str(iss.sublat).split(":")]
    if lat_value[0] < 0:
        lat_value[0] = abs(lat_value[0])
        camera.exif_tags['GPS.GPSLatitudeRef'] = "S"
        direction2 = "S"
    else:
        camera.exif_tags['GPS.GPSLatitudeRef'] = "N"
        direction2 = "N"
    camera.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (lat_value[0], lat_value[1], lat_value[2] * 10)
    return (str(lat_value), str(long_value), str(direction1), str(direction2))


# PL - pozyskiwanie jasnosci
# ENG - gaining clarity
def calculate_brightness(image):
    greyscale = image.convert('L')
    histogram = greyscale.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for photo_counter in range(0, scale):
        ratio = histogram[photo_counter] / pixels
        brightness += ratio * (photo_counter - scale)
    if brightness == 255:
        return 1
    else:
        return brightness / scale


logger.info("Mission started")  # PL - poczatek misji       ENG - the beginning of the mission

# PL,ENG - Main

while (now_time < start_time + timedelta(minutes=mission_time)):
    try:

        # PL - otrzymuje długość i szerokość geograficzną
        # ENG - gets longitude and latitude
        get_latlon()

        numer_zdjecia = str(photo_counter).zfill(4)

        # PL - robi zdjecie
        # ENG - takes a picture
        image_name = ("spacerad_{}.jpg".format(numer_zdjecia))
        camera.capture(image_name)

        # PL - otwiera zdjecie i liczy jasnosc
        # ENG - opens the picture and counts the brightness
        im = Image.open(image_name)
        width, height = im.size
        x = int(width * 0.1)
        y = int(width - width * 0.1)
        image = im.crop((x, 0, y, height))
        jasnosc = calculate_brightness(image)

        # PL - zapisywanie informacji do pliku log
        # ENG - writing information to a log file
        info_log = "\tspacerad_{}, ".format(numer_zdjecia) + "jasnosc: " + str(jasnosc)

        logger.info(info_log)
        logger.info(get_latlon())

        if jasnosc < minimum_brightness:
            os.remove(image_name)
            logger.info("\tUsunieto zdjecie spacerad_{}".format(numer_zdjecia))
            photo_counter -= 1

    except Exception as e:
        logger.error("{}: {})".format(e.__class__.__name__, e))
        logger.info("\tNie ma pliku, lub problem z jasnoscia")

    sleep(25)  # PL - do modyfikacji, robi zdjecia co sekunde       # ENG - for modification, takes photos every second
    photo_counter += 1
    now_time = datetime.now()  # PL - aktualizuje czas              # ENG - updates time

logger.info("Mission ended")
