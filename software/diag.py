#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

nrmodes = {-1: 'UNKNOWN', 11: 'BCM', 10: 'BOARD'}
pinmodes = { 0: 'OUT', 1: 'IN', 40: 'UART', 41: 'SPI', 42: 'I2C', 43: 'HARD PWM'}
tctl = {
  2: 'I2C SDA',
  3: 'I2C SCL',
  4: 'NONE',
  5: 'IN A LEFT',
  6: 'DIAG B RIGHT',
  7: 'SPI CS 1',
  8: 'SPI CS 0',
  9: 'SPI MISO',
  10: 'SPI MOSI',
  11: 'SPI CLK',
  12: 'DIAG A RIGHT',
  13: 'FAN RIGHT',
  14: 'SERIAL TX',
  15: 'SERIAL RX',
  16: 'IN A RIGHT',
  17: 'DIAG A LEFT',
  18: 'DIAB B LEFT',
  19: 'IN B RIGHT',
  20: 'ENABLE A RIGHT',
  21: 'PWM RIGHT',
  22: 'IN B LEFT',
  23: 'ENABLE B LEFT',
  24: 'PWM LEFT',
  25: 'ENABLE A LEFT',
  26: 'ENABLE B RIGHT',
  27: 'FAN  LEFT'
}

#    BOTH = 33
#    FALLING = 32
#    HIGH = 1
#    LOW = 0
#    PUD_DOWN = 21
#    PUD_OFF = 20
#    PUD_UP = 22
#    RISING = 31

def diag():
  print("Revision:", GPIO.RPI_INFO['REVISION'])
  print("Version:", GPIO.VERSION)

  print('Board mode', nrmodes[GPIO.getmode()])
  GPIO.setmode(GPIO.BCM)
  print('Board mode', nrmodes[GPIO.getmode()])

  for i in range(2,28):
    pm = pinmodes[GPIO.gpio_function(i)]
    if pm == 'IN':
      GPIO.setup(i, GPIO.IN)
      print('Pin {:2d} {:4s} {} {}'.format(i, pm, GPIO.input(i), tctl[i]))
    else:
      print('Pin {:2d} {:6s} {}'.format(i, pm, tctl[i]))

if __name__ == '__main__':
  diag()
