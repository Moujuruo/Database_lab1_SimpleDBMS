import pymysql
from faker import Faker
import random

db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password" : "root",
    "db" : "moviecomment"
}


fake = Faker()

try:
    # 建立数据库连接
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 清空数据库每张表的数据
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
    cursor.execute('TRUNCATE TABLE Reviews')
    cursor.execute('TRUNCATE TABLE Characters')
    cursor.execute('TRUNCATE TABLE Movies')
    cursor.execute('TRUNCATE TABLE Directors')
    cursor.execute('TRUNCATE TABLE ProductionCompanies')
    cursor.execute('TRUNCATE TABLE Users')
    cursor.execute('TRUNCATE TABLE Actors')
    cursor.execute('TRUNCATE TABLE Awards')
    cursor.execute('TRUNCATE TABLE movieawards')
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
    conn.commit()

except Exception as e:
    print(e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()