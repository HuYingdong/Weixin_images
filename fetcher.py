# -*- coding: utf-8 -*-

import time
import requests
import logging


class Fetcher(object):

    def __init__(self):
        self.client = requests.session()
        self.p = None
        self.logger = logging.getLogger('Fetcher')
        self.headers = {
            'Content-Type': 'application/json'
        }

    def set_p(self):
        p = requests.get('http://120.26.100.226/wechart/index.php?c=api&a=get_proxy').content
        self.p = {'http': p}

    def init_client(self):
        self.set_p()
        if self.client is not None:
            self.client.close()
        self.client = requests.session()

    def get(self, url):
        retry = 3
        while retry:
            try:
                res = self.client.get(url, proxies=self.p, headers=self.headers, timeout=10)
                res.raise_for_status()
                return res
            except Exception as e:
                self.logger.info('url connect failed:%s' % str(e))
                time.sleep(5)
                retry -= 1

    def post(self, url, data):
        res = self.client.post(url, proxies=self.p, data=data, headers=self.headers, timeout=10)
        return res


