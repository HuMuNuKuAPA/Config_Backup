#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
# 作者：呼姆呼姆
# 邮箱：wuzhiping26@gmail.com

from back_main import immediate_backup
from apscheduler.schedulers.blocking import BlockingScheduler
"""
定时执行immediate_backup函数，进行设备配置备份,设置时间为每天晚上的23:26分

linux后台运行脚本nohup python3.6 periodic_backup.py &
参考链接https://www.jianshu.com/p/4041c4e6e1b0
"""
scheduler = BlockingScheduler(timezone='Asia/Shanghai')
scheduler.add_job(
    func=immediate_backup,
    trigger='cron',
    hour=23,
    minute=26,
)
scheduler.start()
