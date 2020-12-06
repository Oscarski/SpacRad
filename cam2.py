import picamera
from time import sleep
from datetime import datetime
from datetime import timedelta
import cv2 as cv
import ephem
import os

MINIMUM_BRIGHTNESS = 55 # byte value, 255 - bright, 0 - dark
IDTH_PHOTO_BORDER = 500 # pixel offset from edges used when counting pixel brightness
HEIGHT_PHOTO_BORDER = 200 # pixel offset from edges used when counting brightness

#poczatek czasu misji
start_time = datetime.now()

#ustawienia kamery
cam = picamera.PiCamera()
cam.resolution = (2592, 1944)

#czas na zdjeciach (opcjonalne)
time_format = "%d/%m/%Y %H:%M:%S"
cam.annotate_background = picamera.Color('black')
cam.annotate_text_size = 40

#pozyskiwanie jasnosci zdjecia
def get_brightness(image):
    try:
        image_in_hsv = cv.cvtColor(cv.imread(image), cv.COLOR_BGR2HSV)
        brightness, pixel_counter = [0] * 2
        width = WIDTH_PHOTO_BORDER
        height = HEIGHT_PHOTO_BORDER
        while height < len(image_in_hsv) - 1 - HEIGHT_PHOTO_BORDER:
            while width < len(image_in_hsv[height]) - 1 - WIDTH_PHOTO_BORDER:
                brightness += image_in_hsv[height][width][2]
                pixel_counter += 1
                width += PIXEL_STEP
            height += PIXEL_STEP
            width = 0
        return brightness / pixel_counter
    except Exception as e:
        logger.error("{}: {})".format(e.__class__.__name__, e))
        logger.info("\tGetting brightness problem")
        return 255

now_time = datetime.now()
czas_misji = 0.5 #docelowo 178

photo_counter = 1

while (now_time < start_time + timedelta(minutes=czas_misji)):
    cam.start_preview(alpha = 192)
    image_name = "Photo{}.jpg".format(photo_counter)
    photo_counter+=1    
    cam.annotate_text = datetime.now().strftime(time_format)   
    sleep(3) 
    cam.capture(image_name)                                 
    now_time = datetime.now() #aktualizuje czas
                                    
    if get_brightness(image_name) < MINIMUM_BRIGHTNESS:
            os.remove(image_name)
            photo_counter -= 1
    


cam.stop_preview()
