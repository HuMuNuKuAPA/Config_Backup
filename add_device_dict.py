#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
# 作者：呼姆呼姆
# 邮箱：wuzhiping26@gmail.com

username = 'wuzp'
passoword = 'Systec123'

cisco_dicve_list = [
    {'192.168.252.122': ['KJW4331-1', 'cisco_ios']},
    {'192.168.252.126': ['KJW4431-2', 'cisco_ios']},
    {'10.0.240.5': ['G3-R4331', 'cisco_ios']},
    {'192.168.252.142': ['G3-R4331-02', 'cisco_ios']},
    {'192.168.9.254': ['WGQ-313-R4331', 'cisco_ios']},
    {'192.168.9.253': ['WGQ-803-R4431', 'cisco_ios']},
    {'192.168.10.252': ['HXSZ-304-M04-C3548-Core1', 'cisco_nxos']},
    {'10.192.10.248': ['HXSZ-304-M05-C3548-Core2', 'cisco_nxos']},
    {'10.187.70.7': ['JQ-D7_E10-INN-Core03', 'cisco_nxos']},
    {'10.187.70.8': ['JQ-D7_E12-INN-Core04', 'cisco_nxos']},
    {'10.187.254.4': ['G1-RN-R1001-1', 'cisco_ios', 'cisco']},
    {'10.187.254.5': ['G1-RN-R1001-2', 'cisco_ios', 'cisco']},
]

huawei_dicve_list = [
    {'10.187.95.30': 'JQE01-WN-AR6140-30'},
    {'10.187.95.29': 'JQE23-WN-AR6300-29'},

]
cisco_dicve_summary = []
for i in range(0, len(cisco_dicve_list)):
    try:
        enable_password = list(cisco_dicve_list[i].values())[0][2]
    except:
        enable_password = ''
    device_dict = {
        'host': list(cisco_dicve_list[i].keys())[0],
        'username': username,
        'password': passoword,
        'cmd': 'show run',
        'device_type': list(cisco_dicve_list[i].values())[0][1],
        'enable': '' if not enable_password else enable_password
    }
    cisco_dicve_summary.append(device_dict)

huawei_dicve_summary = []
for i in range(0, len(huawei_dicve_list)):
    device_dict = {
        'host': list(huawei_dicve_list[i].keys())[0],
        'username': username,
        'password': passoword,
        'cmd': 'display current-configuration',
        'device_type': 'huawei',
        'enable': ''
    }
    huawei_dicve_summary.append(device_dict)

all_device = cisco_dicve_summary + huawei_dicve_summary

if __name__ == '__main__':
    from pprint import pprint
    # pprint(cisco_dicve_summary)
    # print('----------------')
    # pprint(huawei_dicve_summary)
    pprint(all_device)
