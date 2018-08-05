from datetime import datetime
import pymongo
import logging


class MongoHelper:
    def __init__(self, info_db):
        self.db = pymongo.MongoClient(info_db['mongo_uri'])[info_db['db']]
        self.logger = logging.getLogger('MongoHelper')

    def add_item(self, col_name, doc):
        try:
            if self.db[col_name].insert_one(doc):
                info = {'status': 'new', 'create_time': datetime.now(), 'done_time': ''}
                self.db[col_name].update_one({'_id': doc['_id']}, {'$set': info})
                return True
        except Exception as e:
            self.logger.error(e)
            return False

    def set_item(self, col_name, task_id):
        try:
            info = {'status': 'done', 'done_time': datetime.now()}
            self.db[col_name].update_one({'task_id': task_id}, {'$set': info})
        except Exception as e:
            self.logger.error(e)
            return False

    def get_info(self, col_name):
        new_num = self.db[col_name].count({'status': 'new'})
        done_num = self.db[col_name].count({'status': 'done'})
        return {'new_tasks': new_num,
                'done_tasks': done_num}
