import logging
import re
from fetch_tool import download_imgs
from fetcher import Fetcher
from mongo_helper import MongoHelper
import config
from crawl_func import Getter


class SaveService:
    def __init__(self, target_url):
        self.url = target_url
        self.logger = logging.getLogger('SaveService')
        self.fetcher = Fetcher()
        self.getter = Getter()
        self.url_info = {}
        self.client = MongoHelper(config.store_db)

    def run_save(self, col_name, save=True):
        self.get_info()
        self.logger.debug('failed to get url info')
        if not self.url_info.get('imgs') or not self.url_info.get('title'):
            self.logger.error('failed to get url info.')
            return False
        title = self.url_info.get('title').replace(' ', '').replace('|', '_').replace('/', '_')
        self.logger.info('get url title:%s', title)
        self.url_info['title'] = title
        if save:
            self.logger.info('start save images...')
            self.save_images(img_dir='./imgs/' + title)
            if not self.url_info.get('images_info'):
                self.logger.error('failed to save images')
                return False
        if self.save_mongo(col_name):
            return True
        else:
            return False

    def get_info(self):
        for crawl_func in self.getter.__CrawlFunc__:
            name = re.search('crawl_(.*)', crawl_func).group(1)
            if name in self.domain_url:
                self.url_info = self.getter.get_info(crawl_func, self.url)
                break
        else:
            self.logger.info('Crawl Function Undefined')

    @property
    def domain_url(self):
        try:
            return re.search('http(?:s:|:)//(.*?)\.(?:com|cn)', self.url).group(1)
        except AttributeError as e:
            self.logger.error(e)

    def save_images(self, img_dir):
        imgs = self.url_info.get('imgs')
        try:
            self.url_info['images_info'] = download_imgs(img_dir, imgs)
        except Exception as e:
            self.logger.error('save error: %s, %s ' % (self.url_info.get('url'), e))

    def save_mongo(self, col_name):
        if self.client.db[col_name].insert_one(self.url_info):
            self.logger.info('successfully saved to mongo: ' + self.url_info.get('url'))
            return True


if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/s?__biz=MzU1MzEwMTY2Mw==' \
          '&mid=2247489981&idx=1&sn=013d830fcf26b0de2fcf3ae8e87ed19f&scene=21' \
          '#wechat_redirect'
    save = SaveService(url)
    save.run_save(save.domain_url)
