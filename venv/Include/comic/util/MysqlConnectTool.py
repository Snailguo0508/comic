import pymysql


try:
    connect = pymysql.connect("localHost","root","123","python")
    cursor = connect.cursor()
    print("数据库连接成功")
    sql = "select * from user"
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        print(row)
except:
    print("数据库连接异常")



