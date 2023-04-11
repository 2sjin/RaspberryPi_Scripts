#!usr/bin/python3

import Adafruit_DHT as dht
import time

SENSOR = dht.DHT11
PIN = 23

# 센서의 습도 및 온도 측정 값을 리턴하는 함수
def sensor_hum_temp():
    # 5초 동안 반복해서 측정(1초에 1번씩)
    for cnt in range(5):
        # 습도 및 온도 측정
        hum, temp = dht.read(SENSOR, PIN)

        # 습도, 온도 중 측정되지 않은 값이 있으면 1초 후 재측정
        if (hum is None) or (temp is None):
            time.sleep(1)
            continue

        # 습도 및 온도 측정 모두 성공하면 측정 중단
        else:
            break

    # None 값이 존재하면 "null"로 변경
    hum = "null" if hum is None else hum
    temp = "null" if temp is None else temp

    # 측정값 리턴
    return hum, temp
