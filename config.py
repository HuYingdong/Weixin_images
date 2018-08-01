#! /usr/bin/env python
# -*- coding: utf-8 -*-
from huey import RedisHuey
huey = RedisHuey('huey_tasks', host='127.0.0.1')

env = 'local'

if env == 'local':
    task_db = {
        'mongo_uri': 'mongodb://127.0.0.1:27017/',
        'db': 'tasks'
    }

    store_db = {
        'mongo_uri': 'mongodb://127.0.0.1:31017/',
        'db': 'images'
    }

    backend_db = {
        'host': '127.0.0.1',
        'user': 'hyd',
        'passwd': '123456',
        'db': 'backend',
        'port': 3306,
        'charset': "utf8"
    }
