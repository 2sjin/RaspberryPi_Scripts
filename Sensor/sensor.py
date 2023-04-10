#!usr/bin/python

import MySQLdb

db = MySQLdb.connect(host="localhost", port=3306, user="rpi4", passwd="!#rpi4", db="rpi4")

cursor = db.cursor()

cursor.execute("select * from sensor_log")

for data in cursor.fetchall():
    print(data)

db.close()
