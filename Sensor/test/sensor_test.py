#!usr/bin/python3

import Adafruit_DHT as dht
import time

SENSOR = dht.DHT11
PIN = 23

read_cnt = 0

while True:
    hum, temp = dht.read(SENSOR, PIN)

    if read_cnt > 10:
        print("Failed to read.")
        break

    elif hum is None or temp is None:
        read_cnt += 1
        print("Reading...")
        continue

    else:    
        print("Hum: {} / Temp: {}".format(hum, temp))

    time.sleep(1)
