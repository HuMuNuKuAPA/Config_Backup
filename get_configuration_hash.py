#!/usr/local/bin/python3
# -*- coding=utf-8 -*-
# 作者：呼姆呼姆
# 邮箱：wuzhiping26@gmail.com

import hashlib


def get_hash(configuration):
    run_config_strip = configuration.strip()
    run_config_space = run_config_strip.replace(' ', '')
    run_config = run_config_space.replace('\n', '')

    m = hashlib.md5()
    m.update(run_config.encode())
    md5_value = m.hexdigest()
    return md5_value
