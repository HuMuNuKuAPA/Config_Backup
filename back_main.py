#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
# 作者：呼姆呼姆
# 邮箱：wuzhiping26@gmail.com

from ssh_netmiko import netmiko_show_cred
from get_configuration_hash import get_hash
import pymysql
from datetime import datetime
from mysql_data_modify import data_modify
from add_device_dict import all_device
import time
from multiprocessing import Pool
from re import match

'''
第一步：拿到设备的配置文件
第二步：对配置文件进行hash，得到hash后的值
第三步：连接数据库，用第二步中得到hash值，对数据库进行搜索
第四步：根据数据搜索的结果进行判断：
        1 如果有搜索结果，对指定设备的Check_time字段更新;
        2 如果没有结果，使用设备名称对数据库进行搜索，查看数据库中是否已有该设备的记录：
            1） 如果没有，则对该设备在数据库中新建记录
            2） 如果数据库中已有该设备的记录，则说明设备的配置信息已有变化，需要在数据库中更新其配置文件、MD5、Modify_Time、Check_Time
'''


def main_fuc(device_info):
    mysql_db_info = {
        'host': '10.168.51.237',
        'user': 'wuzp',
        'password': 'Systec#278',
        'port': 3306,
        'charset': 'utf8',
        'db': 'config_backup',
    }
    # 1.得到配置文件,并通过配置文件
    config_result = netmiko_show_cred(**device_info)
    raw_result = match(r'(.|\n)*((hostname|sysname)(.|\n)*)', config_result).group(2)

    # 2.得到hash值
    hash_result = get_hash(raw_result)

    # 3.连接数据库，通过hash值，对数据库进行搜索
    conn = pymysql.connect(**mysql_db_info)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql_select = "SELECT * FROM device_backup where MD5=%s"
    cursor.execute(sql_select, [hash_result, ])
    data = cursor.fetchall()

    # 4.对结果进行判断
    current_time = datetime.now().strftime('%Y:%m:%d %H:%M:%S')
    if data:
        # 如果有搜索结果，对指定设备的Check_time字段更新;
        sql = "update device_backup set Check_Time=%s where hostname=%s"
        data_modify(conn, cursor, sql, [current_time, device_info['host']])
    else:
        sql = "SELECT * FROM device_backup where hostname=%s"
        cursor.execute(sql, [device_info['host'], ])
        data = cursor.fetchall()
        if data:
            """
            如果数据库中已有该设备的记录，则说明设备的配置信息已有变化，需要在数据库中更新其配置文件、MD5、Modify_Time、Check_Time
            """
            sql = "update device_backup set MD5=%s,Config=%s,Modify_Time=%s,Check_Time=%s " \
                  "where hostname=%s"
            data_modify(conn, cursor, sql, [hash_result, raw_result, current_time, current_time, device_info['host']])
        else:
            sql = "INSERT INTO device_backup(hostname,MD5,Config,Modify_Time,Check_Time) VALUES(%s,%s,%s,%s,%s)"
            data_modify(conn, cursor, sql, [device_info['host'], hash_result, raw_result, current_time, current_time])
    return


def immediate_backup():
    start = time.time()
    p = Pool(4)
    for i in all_device:
        p.apply_async(main_fuc, args=(i,))
    print('等待所有子进程完成。')
    p.close()
    p.join()
    end = time.time()
    print("总共用时{}秒".format((end - start)))


if __name__ == '__main__':
    immediate_backup()


