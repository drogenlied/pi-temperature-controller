#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from influxdb import InfluxDBClient
except:
    pass
import statistics
import datetime
import getopt
import i2cdev
import struct
import signal
import time
import math
import sys

class TSYS01:
    READ_ADC  = 0x00
    RESET     = 0x1E
    START_ADC = 0x48
    READ_ROM0 = 0xA0

    def __init__(self, bus = 1, device = 0x77):
        self.bus = bus
        self.device = device
        self.rom = []

    def open(self):
        self.i2c = i2cdev.I2C(self.device, self.bus)
        
    def close(self):
        self.i2c.close()

    def reset(self):
        buf = struct.pack('B', self.RESET)
        self.i2c.write(buf)
        time.sleep(0.003)

    def readRomAddr(self, addr):
        reg = self.READ_ROM0 | 0x0F & ( addr << 1)
        buf = struct.pack('B', reg)
        self.i2c.write(buf)
        rbuf = self.i2c.read(2)
        return struct.unpack('>H', rbuf)[0]

    def readRom(self):
        self.rom = []
        for i in range(8):
            self.rom.append(self.readRomAddr(i))
        
    def startADC(self):
        buf = struct.pack('B', self.START_ADC)
        try:
            self.i2c.write(buf)
        except OSError:
            pass
        time.sleep(0.010)

    def readADC(self):
        buf = struct.pack('B', self.READ_ADC)
        self.i2c.write(buf)
        rbuf = self.i2c.read(3)
        return struct.unpack('>I', b'\0' + rbuf)[0]

    def temperatureCelsius(self, adcValue):
        if len(self.rom) < 8:
            self.readRom()
        adc16 = adcValue / 2**8
        return (-2.0 * self.rom[1] * 10**-21 * adc16**4
              +  4.0 * self.rom[2] * 10**-16 * adc16**3
              + -2.0 * self.rom[3] * 10**-11 * adc16**2
              +  1.0 * self.rom[4] * 10**-6  * adc16
              + -1.5 * self.rom[5] * 10**-2 );

    def temperatureKelvin(self, adcValue):
        return 273.15 + self.temperatureCelsius(adcValue)


# Generates the necessary payload to post
# temperature data into the InfluxDB
def temperature_data(temperature, variance):
    return [
        {
             'measurement': 'Temperature',
             'fields': {
                 'degrees_celsius': temperature,
                 'standard_deviation': variance},
              'tags': {
                  'sensor': 'TSYS01',
                  'host': 'jbpi'}
        }]


if __name__ == '__main__':
    opts, args = getopt.getopt(
                    sys.argv[1:],
                    'a:b:cdf:hi:n:N:v',
                    [
                        'address',
                        'bus',
                        'client',
                        'daemon',
                        'file',
                        'help',
                        'interval',
                        'number',
                        'average-number',
                        'verbose'
                    ]
                 )

    daemon = False
    bus = 1
    address = 0x77
    verbose = False
    n = 10
    avg = 1
    interval = 1.0
    outfile = sys.stdout
    influxClient = None

    for o, a in opts:
        if o in ('-a', '--address'):
            address = int(a)
        elif o in ('-b', '--bus'):
            bus = int(a)
        elif o in ('-d', '--daemon'):
            daemon = True
            n = 1
        elif o in ('-f', '--file'):
            try:
                outfile = open(a, 'a')
            except:
                outfile = sys.stdout
        elif o in ('-h', '--help'):
            print('Usage: {0} [-b bus] [-a device address] [-d] [-h]'.format(sys.argv[0]))
            print('-a address: i2c device address number')
            print('-b bus: bus number')
            print('-d: run as daemon')
            print('-h: show help')
            print('')
            sys.exit()
        elif o in ('-i', '--interval'):
            interval = float(a)
        elif o in ('-n', '--number'):
            n = int(a)
        elif o in ('-N', '--average-number'):
           avg = int(a)
        elif o in ('-v', '--verbose'):
            verbose = True
        elif o in ('-c', '--client'):
            daemon = True
            influxClient = InfluxDBClient('localhost', 8086, 'user', 'password', 'database')
        else:
            print('Usage: {0} [-b bus] [-a device address] [-d] [-h]'.format(sys.argv[0], ))
            sys.exit(1)

    def sighandler(signal, frame):
        print('Terminating.', file=sys.stderr)
        sys.exit(0)
    signal.signal(signal.SIGTERM, sighandler)

    if verbose:
        print('Device 0x{0:x} on bus 0x{1:x}.'.format(bus, address))
    t = TSYS01(bus, address)
    t.open()
    t.reset()
    t.readRom()
    if verbose:
        for i in range(8):
            print('ROM[{0}]: {1}'.format(i,t.rom[i]))
        print('Going for {0} measurements.'.format(n))
    for i in range(n):
        while True:
            lst = []
            for j in range(avg):
                t.startADC()
                time.sleep(interval/2.0)
                raw = t.readADC()
                if verbose:
                    print('Raw: {0:X}'.format(raw))
                    print('Raw16: {0:X}'.format(raw >> 8))
                    print('RawF: {0}'.format(raw / 2**8))
                lst.append(t.temperatureCelsius(raw))
                time.sleep(interval/2.0)
            if avg > 1:
                print('{0} {1:.6f} {2:.6f}'.format(datetime.datetime.now(), statistics.mean(lst), statistics.stdev(lst) ), file=outfile)
                if influxClient is not None:
                    influxClient.write_points(temperature_data(statistics.mean(lst), statistics.stdev(lst)))
            else:
                print('{0} {1:.6f} {2:.6f}'.format(datetime.datetime.now(), statistics.mean(lst), 0.00 ), file=outfile)
                if influxClient is not None:
                    influxClient.write_points(temperature_data(statistics.mean(lst), 0.0))
            outfile.flush()
            if not daemon:
                break
    t.close()
    outfile.close()
