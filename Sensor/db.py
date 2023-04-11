#!usr/bin/python3

from measure import *
import MySQLdb


# 모든 데이터를 SELECT 하는 함수
def select_all(cur):
    # 커서로 SQL 데이터 조작(SELECT)
    cur.execute("SELECT * FROM sensor_log")

    # 커서로 SELECT한 데이터 전체 출력
    for data in cur.fetchall():
        print(data)
        

# MySQL 연동 함수
def mysql_connect():
    # 데이터베이스 연결
    db = MySQLdb.connect(host="localhost", port=3306, user="rpi4", passwd="!#rpi4", db="rpi4")

    # 커서 생성
    cursor = db.cursor()

    # 커서로 SQL 데이터 조작(INSERT)
    insert_sql = "INSERT INTO sensor_log VALUES(now(), {0}, {1}, {2}, {3}, {4}, {5}, {6})"\
                   .format(cpu_temp(), sensor_temp(), sensor_hum(), cpu_clock(), gpu_clock(), voltage(), processes())
    cursor.execute(insert_sql)

    # 데이터베이스 SELECT 함수 호출(테스트용)
    # select_all(cursor)
    
    # 데이터베이스 커밋
    db.commit()

    # 데이터베이스 롤백
    # db.rollback()

    # 데이터베이스 연결 해제(커서도 제거됨)
    db.close()    
