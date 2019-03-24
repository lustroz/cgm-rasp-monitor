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

boldFont = ImageFont.truetype("Lato-Bold.ttf", 55)
regularFont = ImageFont.truetype("Lato-Regular", 15)
thinFont = ImageFont.truetype("Lato-Thin", 10)

width = 128
height = 64
image = Image.new('1', (width, height))

serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)

device = sh1106(serial, rotate=2) #sh1106  

def drawState(text):
    x = 0
    top = 0

    with canvas(device) as draw:
        draw.text((x, top), text, font=regularFont, fill=200)

def draw(source, recTime, value, direction, delta):
    x = 0
    top = -2

    if source == 'nightscout':
        src = 'N'
    else:
        src = 'D'

    elapsed = int(time.time()) - recTime / 1000
    if delta > 0:
        dStr = '+' + str(delta)
    elif delta < 0:
        dStr = '-' + str(-delta)
    else:
        dStr = '='

    if value < 100:
        vX = x + 60
    else:
        vX = x + 30

    with canvas(device) as draw:
        draw.text((x, top), src, font=regularFont, fill=255)
        draw.text((x, top+10), str(int(elapsed / 60))+' m', font=regularFont, fill=255)
        draw.text((x, top+30), dStr, font=regularFont, fill=255)
        #draw.text((x+25, top+32), 'mg/dL', font=thinFont, fill=255)
        draw.text((vX, top), str(value),  font=boldFont, fill=255)
