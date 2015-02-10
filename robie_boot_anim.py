import time
from neopixel import *

# configure LED's:

LED_COUNT 	= 14 	  # 2 x 7 NeoPixel Jewels
LED_PIN		= 18	  # Hardware PCM pin (Pin 12, GPIO18) 
LED_FREQ_HZ	= 800000  # LED frequency (800Khz)
LED_DMA		= 5	  # DMA channel
LED_BRIGHTNESS	= 15	  # Can go up to 255, but it's good to keep power usage low
LED_INVERT	= False	  # I believe this is for ws2811's

# This was lifted from the rpi_ws281x strandtest demo. I only added the intensity code:
def wheel(pos, intensity=100):
  """Generate rainbow colors across 0-255 positions."""
  if pos < 85:
    r = ((pos * 3) * intensity ) / 100
    g = ((255 - pos * 3) * intensity ) / 100
    return Color(r, g, 0)
  elif pos < 170:
    pos -= 85
    r = ((255 - pos * 3) * intensity ) / 100
    b = ((pos * 3) * intensity ) / 100
    return Color(r, 0, b)
  else:
    pos -= 170
    g = ((pos * 3) * intensity ) / 100
    b = ((255 - pos * 3) * intensity ) / 100
    return Color(0, g, b)

def chaseDot(strip):
  max_range = 23
  chase_speed = 0.1
  for x in range(0,max_range):
    # This controls the leading pixel:
    if x < max_range-4:
      pix = (x % 6) + 1
      strip.setPixelColor( pix, wheel(x*(256/max_range), 100) ) 
      strip.setPixelColor( pix+7, wheel(x*(256/max_range), 100) )
    # This controls the "tail" pixels:
    for tail in range(1,5):
      if (x-tail)+4 >= max_range:
        continue
      pix = ((x-tail) % 6) + 1
      if pix <= x:
        intensity = 100 - (tail * 25)
        strip.setPixelColor( pix, wheel((x-tail)*(256/max_range), intensity) )
        strip.setPixelColor( pix+7, wheel((x-tail)*(256/max_range), intensity) )
    strip.show()
    time.sleep(chase_speed)

def fadeFromWhite(strip):
  fade_speed = 0.001
  for x in range(0,256):
    for y in range(0,LED_COUNT):
      strip.setPixelColor(y, Color(255-x,255-x,255-x))
    strip.show()
    time.sleep(fade_speed)
    
    
if __name__ == '__main__':
  try:
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    chaseDot(strip)
    fadeFromWhite(strip)
  finally:
    # ensure we don't leave LED's on if user ctl-c's:
    for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0,0,0))
                strip.show()
    strip = None
