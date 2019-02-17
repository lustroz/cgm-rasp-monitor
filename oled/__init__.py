from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import time
import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

boldFont = ImageFont.truetype("Lato-Bold.ttf", 50)
regularFont = ImageFont.truetype("Lato-Regular", 18)

width = 128
height = 64
image = Image.new('1', (width, height))

serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)

device = sh1106(serial, rotate=2) #sh1106  

def draw(origin, recTime, value, direction, delta):
    x = 0
    top = -2
    elapsed = int(time.time()) - recTime / 1000
    if delta > 0:
        dStr = '+' + str(delta)
    elif delta < 0:
        dStr = '-' + str(-delta)
    else:
        dStr = 0
    dStr += ' mg/dL'

    if value < 100:
        vX = x + 60
    else:
        vX = x + 40

    with canvas(device) as draw:
        draw.text((x, top), str(elapsed / 60) + ' min', font=regularFont, fill=255)
        draw.text((x, top+50), dStr, font=regularFont, fill=255)
        draw.text((vX, top), str(value),  font=boldFont, fill=255)
