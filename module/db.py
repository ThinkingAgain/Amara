import pymysql
import time


class DB:
    """MySql--DB："""

    def __init__(self):
        self.db = "todo"
        self.pw = "asdfwj"

    def get_conn(self) -> bool:
        '''连接数据库'''
        try:
            self.conn = pymysql.connect(host='127.0.0.1', user='root',
                                        passwd=self.pw, port=3306,
                                        charset='utf8', db=self.db)
        except pymysql.Error as e:
            print(e)
            print('数据库连接失败')
            return False
        return True

    def close_conn(self):
        '''关闭数据库'''
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e)
            print('关闭数据库失败')

    def execute_sqllist(self, sql_list: list) -> int:
        '''使用sql语句列表操作（IUD）数据库:成功返回1，失败回滚并返回0'''
        self.get_conn()
        try:
            cursor = self.conn.cursor()
            for sql in sql_list:
                # print(sql)
                cursor.execute(sql)
            # 一定需要提交事务，要不不会显示，只会占位在数据库
            self.conn.commit()
            return 1
        except AttributeError as e:
            print('Error:', e)
            return 0
        except TypeError as e:
            print('Error:', e)
            # 发生错误还提交就是把执行正确的语句提交上去
            # self.conn.commit()
            # 下面这个方法是发生异常就全部不能提交,但语句执行成功的就会占位
            self.conn.rollback()
            return 0
        finally:
            cursor.close()
            self.close_conn()

    def get_all(self, sql):
        '''
        返回sql语句查询到的所有数据。
        返回值：字典列表 [{字段1: 值1, 字段2: 值2 ,....},{}, {}...]
        '''
        self.get_conn()
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            #print(cursor.description)
            desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
            return [dict(zip([col[0] for col in desc], values)) for values in cursor.fetchall()]

        except AttributeError as e:
            print("异常：", e)
            return None
        finally:
            self.close_conn()

    def __table_exist(self, table: str) -> bool:
        # 表是否存在?
        self.get_conn()
        try:
            cursor = self.conn.cursor()
            cursor.execute("show tables;")
            tables = [item[0] for item in cursor.fetchall()]
        except AttributeError as e:
            print('Error:', e)
        finally:
            cursor.close()
            self.close_conn()
        return table in tables

    def __create_table_onu_autofind(self, table: str) -> int:
        # 创建onu_autofind_yyyymm表
        sql = f"CREATE TABLE {table}(" \
              "`DATE` date Not NULL," \
              "`TIME` time Not Null," \
              "DID varchar(20) Not Null," \
              "REGION varchar(20) Not Null," \
              "DEV varchar(60) Not Null," \
              "FN varchar(20)," \
              "SN varchar(20)," \
              "PN varchar(20)," \
              "SERIALNUM varchar(20)," \
              "PWD varchar(20)," \
              "VENDORID varchar(20)," \
              "EQID varchar(20)," \
              "MAINSOFTVER varchar(20)" \
              ");"
        return self.execute_sqllist([sql])

    def insert_onu_autofind(self, data: list) -> int:
        '''插入onu autofind, 输入为字典列表 表名为onu_autofind_YYYYMM:成功返回1，失败回滚并返回0'''
        if not data: return 0
        # 确保onu_autofind_yyyymm存在
        table = "onu_autofind_" + "".join(data[0]["DATE"].split("-")[:2])
        if not self.__table_exist(table): self.__create_table_onu_autofind(table)
        # 由data生成sql语句并执行
        sqls = []
        for item in data:
            kvs = [(k, repr(v)) for k, v in item.items()]
            sqls.append(
                f"INSERT INTO {table} ({','.join([x[0] for x in kvs])}) VALUES ({','.join([x[1] for x in kvs])});")
        return self.execute_sqllist(sqls)

    def get_onu_autofind(self):
        """返回ONU自动发现字典列表(最近5分钟）
        【{所有字段:}，{。。。}，。。。】
        """
        table = "onu_autofind_" + time.strftime("%Y%m", time.localtime())
        today = time.strftime("%Y-%m-%d", time.localtime())
        #print(today)
        sql = f"select * from {table} where date='{today}' and " \
              f"time between date_add(now(), interval - 5 minute) and " \
              f"date_add(now(), interval + 5 minute) Order by Time DESC;"
        return self.get_all(sql)


if __name__ == "__main__":
    db = DB()
    # sqls = ['INSERT INTO onu_autofind(find_date,find_time,DID,REGION,Dev) ' \
    #      'VALUES("2019-11-16","10:16:18","126","市区","LC-市区-832-GPON-MA5680T-O1");']
    data = [{'DATE': '2019-11-17', 'TIME': '19:16:38', 'DID': '7342090', 'DEV': 'LC-冠县-辛集-GPON-MA5680T-O1',
             'FN': '0', 'SN': '5', 'PN': '7', 'SERIALNUM': '5A544547CBFA76F2', 'PWD': 'GCBFA76F2',
             'VENDORID': 'ZTEG', 'EQID': 'ZXHN F677V2', 'MAINSOFTVER': 'V2.0.0P1T3', 'region': '冠县'},
            {'DATE': '2019-11-16', 'TIME': '17:55:29', 'DID': '7351060', 'DEV': 'LC-莘县-古云-GPON-MA5680T-O1',
             'FN': '0', 'SN': '6', 'PN': '1', 'SERIALNUM': '464854544FA86222', 'PWD': '--', 'VENDORID': '0',
             'EQID': 'HG6543C', 'MAINSOFTVER': 'V1.0', 'region': '莘县'}]

    # print(db.execute_sqllist(sqls))
    print(db.insert_onu_autofind(data))