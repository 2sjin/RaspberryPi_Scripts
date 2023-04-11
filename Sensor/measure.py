#!usr/bin/python3

import subprocess

# CPU 온도를 리턴하는 함수
def cpu_temp():
    command = "vcgencmd measure_temp"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return float(result.stdout[5:-3])

# 센서의 온도 측정 값을 리턴하는 함수
def sensor_temp():
    return -1

# 센서의 습도 측정 값을 리턴하는 함수    
def sensor_hum():
    return -1

# ARM CPU의 클럭 속도를 리턴하는 함수
def cpu_clock():
    command = "vcgencmd measure_clock arm"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return int(result.stdout.split("=")[1])

# GPU Core의 클럭 속도를 리턴하는 함수
def gpu_clock():
    command = "vcgencmd measure_clock core"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return int(result.stdout.split("=")[1])

# 전원 공급 전압값을 리턴하는 함수
def voltage():
    command = "vcgencmd measure_volts"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return float(result.stdout[5:-2])

# 사용자가 실행 중인 프로세스 개수를 리턴하는 함수
def processes():
    command = "ps -u rpi4 | wc -l"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return int(result.stdout)
