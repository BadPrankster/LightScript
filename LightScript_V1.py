# Projektarbeit Elektronik: Lichtsteuerung
# Johnsion Atputharajah / Lucas Wirz-Vitiuk
# September 2021

# Bibliotheken importieren
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
GPIO.setmode(GPIO.BCM)
from gpiozero import MotionSensor

# LED-Variabeln definieren
PIXEL_COUNT = 320
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
bright = 255

# Zeitdauer festlegen
wait = 30
dim_wait = 1.5

# Auswahl der Pins
pir1 = MotionSensor(4)
pir2 = MotionSensor(14)

# Dimmer-Parameter
dim_levels = 5
dim_factor = dim_levels


# Code

while True:
   
# Helligkeit über Uhrzeit steuern
    if datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) <= datetime.now(): 
        bright = 85
    if datetime.today().replace(hour=7, minute=30, second=0, microsecond=0) <= datetime.now(): 
        bright = 170
    if datetime.today().replace(hour=18, minute=0, second=0, microsecond=0) <= datetime.now(): 
        bright = 225
    if datetime.today().replace(hour=21, minute=30, second=0, microsecond=0) <= datetime.now(): 
        bright = 200
    print("Brightness is set to " + str(bright))  

# Reaktion Sensor 1 -> LEDs von vorne einschalten
    if pir1.motion_detected:
        print("Motion detected - Sensor 1 - start")
        for i in range(pixels.count()):
            pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(bright, bright, bright))
            pixels.show()
        print("Motion detected - Sensor 1 - end")
        dim_factor = dim_levels
        sleep(wait)

# Reaktion Sensor 2 -> LEDs von hinten einschalten
    if pir2.motion_detected:
        print("Motion detected - Sensor 2 - start")
        for j in range(pixels.count()):
            pixels.set_pixel(pixels.count() -j -1, Adafruit_WS2801.RGB_to_color(bright, bright, bright))
            pixels.show()
        print("Motion detected - Sensor 2 - end")
        dim_factor = dim_levels
        sleep(wait)

# Informative Textausgabe
    if not pir1.motion_detected:
        print("Motion stopped - Sensor 1")
    if not pir2.motion_detected:
        print("Motion stopped - Sensor 2")

# Ohne Reaktion -> LEDs dimmen und ausschalten
    if not (pir1.motion_detected or pir2.motion_detected):
        if dim_factor > 0:
            dim_factor -= 1
            bright = int(bright * (dim_factor/dim_levels))
            for k in range(pixels.count()):
                pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(bright, bright, bright))
            pixels.show()
            sleep(dim_wait)
        else:
            print("Turn LEDs off")
            pixels.clear()
            pixels.show()

# Neustart um Mitternacht
    if datetime.today().replace(hour=23, minute=59, second=0, microsecond=0) <= datetime.now():
        os.system("sudo reboot")

# Ende des Codes, wird wiederholt
