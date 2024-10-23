import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        user='root',
        password='0707',
        host='localhost',
        database='table',
        port=3306,
        autocommit=True
    )

    if connection.is_connected():
        print("连接成功")

        cursor = connection.cursor()

        query = "SELECT * FROM airports;"
        cursor.execute(query)

        rows = cursor.fetchall()

        for row in rows:
            print(row)

except Error as e:
    print("数据库操作失败:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("数据库连接已关闭")
