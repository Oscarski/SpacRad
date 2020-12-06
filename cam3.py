from picamera import PiCamera
from time import sleep
from datetime import datetime 
from datetime import timedelta
import cv2
import os

minimum_brightness = 55 # minimalna jasnosc zdjecia, wielkosc w bajtach: 255 - jasne, 0 - ciemne
#width_border = 500 # pixel offset from edges used when counting pixel brightness
#height_border = 200 # pixel offset from edges used when counting brightness
krok = 20 # skraca liczenie jasnosci, przeskok w iteracji

# read and save the path to the main.py
dir_path = os.path.dirname(os.path.realpath(__file__))

# create logfile
logfile(dir_path + "/pardubicepi.log")

#poczatek czasu misji
start_time = datetime.now()
now_time = datetime.now() #uzyte w petli koncowej

#ustawienia kamery
cam = PiCamera()
cam.resolution = (2592, 1944)

-------------------------------
img = cv2.imread('test.jpg') #load rgb image
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert it to hsv

for x in range(0, len(hsv)):
    for y in range(0, len(hsv[0])):
        hsv[x, y][2] += value

img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imwrite("image_processed.jpg", img)

-----------------------------------------
import cv2
import numpy as np

image = cv2.read('image.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
value = 42 #whatever value you want to add
cv2.add(hsv[:,:,2], value, hsv[:,:,2])
image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
cv2.imwrite('out.png', image)
------------------------------------------

#pozyskiwanie jasnosci zdjecia
def get_brightness(image): #image jest nazwa pliku
    try:
        read_image = cv2.imread(image) #odczytuje zdjecie o nazwie image
        hsv = cv2.cvtColor(read_image, cv2.COLOR_BGR2HSV) #konwersja na hsv
        brightness, pixel_counter = [0] * 2

        for height in range(0, len(hsv)):
            for width in range(0, len(hsv[0]))
                brightness += hsv[height][width][2]
                pixel_counter += 1
                width += krok
            height += krok
            width = 0

        return brightness / pixel_counter

    except Exception as e:
        logger.error("{}: {})".format(e.__class__.__name__, e))
        logger.info("\tGetting brightness problem")
        return 255


# start the mission
logger.info("Mission started")

mission_time = 0.5 #docelowo 178

photo_counter = 1 #zmienna do iteracji 

while (now_time < start_time + timedelta(minutes=mission_time)):
    cam.start_preview(alpha = 192) #to jest do usuniecia

    # save the full path od upcoming photo
    image_name = dir_path + "/spacerad_" + str(photo_counter).zfill(4) + ".jpg"
    cam.capture(image_name)
    photo_counter+=1      
    sleep(3) 
                                     
    now_time = datetime.now() #aktualizuje czas
                                    
    if get_brightness(image_name) < minimum_brightness:
            os.remove(image_name)
            photo_counter -= 1
    


cam.stop_preview() #to jest tez do usuniecia

