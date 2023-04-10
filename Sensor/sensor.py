#!usr/bin/python

#import MySQLdb
import subprocess

def print_temp():
    # 명령어 실행
    command = "vcgencmd measure_temp"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

    # 명령어 리턴값 가져오기
    print(result)

def db():
    # 데이터베이스 연결
    db = MySQLdb.connect(host="localhost", port=3306, user="rpi4", passwd="!#rpi4", db="rpi4")

    # 커서 생성
    cursor = db.cursor()

    # 커서로 SQL 데이터 조작
    cursor.execute("select * from sensor_log")

    # 커서로 SELECT한 데이터 전체 출력
    for data in cursor.fetchall():
        print(data)

    # 커밋/롤백(단순 SELECT에서는 불필요)
    # db.commit()
    # db.rollback()

    # 데이터베이스 연결 해제(커서도 제거됨)
    db.close()    

print_temp()