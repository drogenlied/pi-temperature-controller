#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import RPi.GPIO as GPIO
import diag

class PWM():

    def __init__(self, right=True):
        if right:
            self.inapin = 16
            self.inbpin = 19
            self.pwmpin = 21
            self.enapin = 20
            self.enbpin = 26
            self.diapin = 12
            self.dibpin = 6
            self.fanpin = 13
        else:
            self.inapin = 5
            self.inbpin = 22
            self.pwmpin = 24
            self.enapin = 25
            self.enbpin = 23
            self.diapin = 17
            self.dibpin = 18
            self.fanpin = 27

        self.freq = 10

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enapin, GPIO.OUT)
        GPIO.setup(self.enbpin, GPIO.OUT)
        GPIO.setup(self.inapin, GPIO.OUT)
        GPIO.setup(self.inbpin, GPIO.OUT)
        GPIO.setup(self.pwmpin, GPIO.OUT)
        GPIO.setup(self.fanpin, GPIO.OUT)
        GPIO.setup(self.diapin, GPIO.IN)
        GPIO.setup(self.dibpin, GPIO.IN)
        self.p = GPIO.PWM(self.pwmpin, self.freq)

    def start(self):
        GPIO.output(self.fanpin, True)
        GPIO.output(self.enapin, True)
        GPIO.output(self.enbpin, True)
        GPIO.output(self.inapin, True)
        GPIO.output(self.inbpin, False)

        # Setup PWM and DMA channel 0
        self.p.start(0)

    def stop(self):
        # Stop PWM
        self.p.stop()
        GPIO.output(self.enapin, False)
        GPIO.output(self.enbpin, False)
        GPIO.output(self.inapin, False)
        GPIO.output(self.inbpin, False)
        GPIO.output(self.fanpin, False)

    def change(self, duty):        
        if duty >= 0:
            GPIO.output(self.inapin, True)
            GPIO.output(self.inbpin, False)
        else:
            GPIO.output(self.inapin, False)
            GPIO.output(self.inbpin, True)
        self.p.ChangeDutyCycle(abs(duty))

if __name__ == '__main__':
    diag.diag()

    side = len(sys.argv) >= 2 and sys.argv[1] == 'right'
        
    p1 = PWM(side)

    p1.setup()
    diag.diag()

    p1.start()
    print("full forward")
    p1.change(100)
    time.sleep(30)
    print("full backward")
    p1.change(-100)
    time.sleep(30)

    p1.stop()

    diag.diag()

