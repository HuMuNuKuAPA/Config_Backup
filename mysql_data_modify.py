#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
# 作者：呼姆呼姆
# 邮箱：wuzhiping26@gmail.com

def data_modify(conn, cursor, sql, args):
    try:
        cursor.execute(sql, args)
        conn.commit()
    except:
        # 如果发生错误则回滚
        conn.rollback()
        print("更新失败")
    # 关闭光标对象
    cursor.close()


if __name__ == '__main__':
    import pymysql
    from datetime import datetime

    mysql_db_info = {
        'host': '10.168.51.237',
        'user': 'wuzp',
        'password': 'Systec#278',
        'port': 3306,
        'charset': 'utf8',
        'db': 'config_backup',
    }
    time = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    conn = pymysql.connect(**mysql_db_info)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "INSERT INTO device_backup(hostname,MD5,Config,Modify_Time,Check_Time) VALUES(%s,%s,%s,%s,%s)"
    data_modify(conn, cursor, sql, ['1.1.1.1', 'hash_result', 'raw_result', time, time])
