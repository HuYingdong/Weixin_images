# coding=utf-8
import requests
from config import huey
from save_service import SaveService
import config
from mongo_helper import MongoHelper


# @huey.task(retries=3)
def save(_id, url, notice_url):
    spider = SaveService(url)
    success = spider.run_save(col_name='weixinimages')
    code = 1 if success else 0
    if code:
        client = MongoHelper(config.task_db)
        client.set_item(col_name='tasks', _id=_id)

    data = {'code': code, 'id': _id, 'url': url}
    requests.post(notice_url, data=data)

    # # 测试callback, 可删
    # response = requests.post(callback, data=data)
    # print(response.json())




