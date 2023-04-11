#!usr/bin/python

import MySQLdb
import subprocess

# 현재 CPU 온도를 리턴하는 함수
def cpu_temp():
    # 명령어 실행
    command = "vcgencmd measure_temp"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

    # 명령어 리턴값에서 온도 값만 추출하여 반환
    temp = float(result.stdout[5:-3])
    return temp

# MySQL 연동 테스트용 함수
def mysql_test():
    # 데이터베이스 연결
    db = MySQLdb.connect(host="localhost", port=3306, user="rpi4", passwd="!#rpi4", db="rpi4")

    # 커서 생성
    cursor = db.cursor()

    # 커서로 SQL 데이터 조작(INSERT)
    cursor.execute(f"INSERT INTO sensor_log VALUES(now(), {cpu_temp()})")

    # 커서로 SQL 데이터 조작(SELECT)
    cursor.execute("SELECT * FROM sensor_log")

    # 커서로 SELECT한 데이터 전체 출력
    for data in cursor.fetchall():
        print(data)
        
    # 데이터베이스 커밋
    db.commit()

    # 데이터베이스 롤백
    # db.rollback()

    # 데이터베이스 연결 해제(커서도 제거됨)
    db.close()    


mysql_test()
