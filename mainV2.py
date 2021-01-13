# biblioteki
# from sense_hat import SenseHat
from picamera import PiCamera
from time import sleep
import ephem
from logzero import logger, logfile
from PIL import Image
from datetime import datetime
from datetime import timedelta
import os

# zmienne globalne
minimum_brightness = 0.35  # minimalna jasnosc
mission_time = 0.1  # docelowo 178
dir_path = os.path.dirname(os.path.realpath(__file__))
photo_counter = 1

# tworzy logfile
logfile(dir_path + "/spacerad.csv")

# poczatek czasu misji
start_time = datetime.now()
now_time = datetime.now()  # uzyte w petli koncowej

# Ustawienie Sense Hat
# sh = SenseHat()

# Ustawienia kamery
camera = PiCamera()
camera.resolution = (2592, 1944)  # Pytamy się Waldemara czy będzie ok rozdzielczość  (ta druga 1600, 912)

# Najnowsze dane TLE dla lokalizacji
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20316.41516162  .00001589  00000+0  36499-4 0  9995"
line2 = "2 25544  51.6454 339.9628 0001882  94.8340 265.2864 15.49409479254842"
iss = ephem.readtle(name, line1, line2)


# Funkcja zapisująca szerokość / długość geograficzną do danych EXIF ​​dla zdjęć
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


# pozyskiwanie jasnosci
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

logger.info("Mission started")  # poczatek misji

# main

while (now_time < start_time + timedelta(minutes=mission_time)):
    camera.start_preview(alpha=192)  # to jest do usuniecia
    try:

        lat, lon, direct1, direct2 = get_latlon()  # otrzymuje długość i szerokość geograficzną

        # zapisuje całą ścieżkę zdjęcia
        # zdjecie i jasnosc
        
        numer_zdjecia = str(photo_counter).zfill(4)
        
        image_name = ("spacerad_{}.jpg".format(numer_zdjecia))
        camera.capture(image_name)
        
        image = Image.open(image_name)
        jasnosc = calculate_brightness(image)

        # zapisywanie informacji do pliku log
        info_log = "\tspacerad_{}, ".format(numer_zdjecia) + "jasnosc: " + str(jasnosc)
        
        logger.info(info_log)
        logger.info("\n", lat,"\n", lon,"\n", direct1,"\n", direct2)

        if jasnosc < minimum_brightness:
            os.remove(image_name)
            logger.info("\tUsunieto zdjecie spacerad_{}".format(numer_zdjecia))
            photo_counter -= 1

    except Exception as e:
        logger.error("{}: {})".format(e.__class__.__name__, e))
        logger.info("\tNie ma pliku, lub problem z jasnoscia")

    sleep(1)
    photo_counter += 1
    now_time = datetime.now()  # aktualizuje czas

# sense.clear()
camera.stop_preview()  # to jest tez do usuniecia
