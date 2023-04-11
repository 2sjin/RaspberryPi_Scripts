#!usr/bin/python3

import MySQLdb
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

# MySQL 연동 테스트용 함수
def mysql_test():
    # 데이터베이스 연결
    db = MySQLdb.connect(host="localhost", port=3306, user="rpi4", passwd="!#rpi4", db="rpi4")

    # 커서 생성
    cursor = db.cursor()

    # 커서로 SQL 데이터 조작(INSERT)
    insert_sql = "INSERT INTO sensor_log VALUES(now(), {0}, {1}, {2}, {3}, {4}, {5}, {6})"\
                   .format(cpu_temp(), sensor_temp(), sensor_hum(), cpu_clock(), gpu_clock(), voltage(), processes())
    cursor.execute(insert_sql)

    """
    # 커서로 SQL 데이터 조작(SELECT)
    cursor.execute("SELECT * FROM sensor_log")

    # 커서로 SELECT한 데이터 전체 출력
    for data in cursor.fetchall():
        print(data)
    """
    
    # 데이터베이스 커밋
    db.commit()

    # 데이터베이스 롤백
    # db.rollback()

    # 데이터베이스 연결 해제(커서도 제거됨)
    db.close()    


mysql_test()
