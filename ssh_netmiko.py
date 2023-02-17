#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
# 作者：呼姆呼姆
# 邮箱：wuzhiping26@gmail.com

from netmiko import Netmiko


def netmiko_show_cred(host, username, password, cmd, device_type, enable):
    device_info = {
        'host': host,
        'username': username,
        'password': password,
        'device_type': device_type,
        'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        if enable:
            net_connect.enable()
        return net_connect.send_command(cmd)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


def netmiko_config_cred(host, username, password, cmds_list, enable='Cisc0123', ssh=True, verbose=False):
    device_info = {
        'host': host,
        'username': username,
        'password': password,
        'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
        'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        if verbose:
            output = net_connect.send_config_set(cmds_list)
            return output
        else:
            net_connect.send_config_set(cmds_list)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


if __name__ == '__main__':
    from re import match
    raw_result = netmiko_show_cred(host='10.187.254.4', username='wuzp', password='Systec123',
                                   cmd='show run', device_type='cisco_ios',
                                   enable='cisco'
                                   )
    # print(raw_result)
    # print(type(raw_result))
    raw_result1 = match(r'(.|\n)*((hostname|sysname)(.|\n)*)', raw_result)
    print(raw_result1.group(2))

    # config_commands = ['router ospf 1',
    #                    'router-id 1.1.1.1',
    #                    'network 1.1.1.1 0.0.0.0 a 0']
    #
    # print(netmiko_config_cred('10.1.1.253', 'admin', 'Cisc0123', config_commands, verbose=True))
