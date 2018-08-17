# coding=utf-8
import requests
from config import huey
from save_service import SaveService
import config
from mongo_helper import MongoHelper


@huey.task(retries=3)
def save(task_id, url, notice_url):
    spider = SaveService(url)
    success = spider.run_save(col_name='wximage')
    code = 1 if success else 0
    if code:
        client = MongoHelper(config.task_db)
        client.set_item(col_name='tasks', task_id=task_id)

    data = {'code': code, 'task_id': task_id, 'url': url}
    requests.post(notice_url, data=data)





