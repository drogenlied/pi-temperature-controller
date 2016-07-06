#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
import temperaturelogd.tsys01_spi
import pwm

if __name__ == '__main__':

    t1 = tsys01_spi.TSYS01(0,0)
    t1.open()
    t1.reset()
    t1.readRom()

    t2 = tsys01_spi.TSYS01(0,1)
    t2.open()
    t2.reset()
    t2.readRom()

    print('setup')
    p1 = pwm.PWM(True)
    p2 = pwm.PWM(False)
    p1.setup()
    p2.setup()
    print('wait')
    for i in range(10):
        t1.startADC()
        t2.startADC()
        time.sleep(1)
        raw1 = t1.readADC()
        raw2 = t2.readADC()
        print("T1:", t1.temperatureCelsius(raw1))
        print("T2:", t2.temperatureCelsius(raw2))
    p1.start()
    p2.start()

    print('ramp')
    for i in range(-10, 10):
        print(i)
        t1.startADC()
        t2.startADC()
        time.sleep(1)
        raw1 = t1.readADC()
        raw2 = t2.readADC()
        print("T1:", t1.temperatureCelsius(raw1))
        print("T2:", t2.temperatureCelsius(raw2))
        p1.change(10*i)
        p2.change(10*i)
 
    p1.stop()
    p2.stop()
    print('post')
    for i in range(10):
        t1.startADC()
        t2.startADC()
        time.sleep(1)
        raw1 = t1.readADC()
        raw2 = t2.readADC()
        print("T1:", t1.temperatureCelsius(raw1))
        print("T2:", t2.temperatureCelsius(raw2))
 
    t1.close()
    t2.close()

