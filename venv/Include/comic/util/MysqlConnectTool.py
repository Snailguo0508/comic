import pymysql

class MysqlConnectTool:
    def __init__(self):
        pass

    def getConnect(self):
        try:
            connect = pymysql.connect("localHost", "root", "123", "python")
            print("获取数据库连接成功")
            return connect;
        except Exception as e:
            print("获取数据库连接异常")
            return None

    def save(self,sql):
        try:
            conn = getConnect()

            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print("保存数据异常")
            connrollback()
        conn.close()




