from bs4 import BeautifulSoup
from fetcher import Fetcher


class GetMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(mcs, name, bases, attrs)


class Getter(metaclass=GetMetaclass):
    def __init__(self):
        self.fetcher = Fetcher()

    def get_info(self, callback, url):
        crawl_func = eval('self.{0}'.format(callback))
        return crawl_func(url)

    def crawl_weixin(self, url):
        result = {}
        res = self.fetcher.get(url)
        soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf8')
        item_imgs = soup.select('#page-content img[data-src!=""]')
        imgs = [item_img['data-src'] for item_img in item_imgs]
        title = soup.select('h2#activity-name')[0].text.strip()
        result['url'] = url
        result['imgs'] = imgs
        result['title'] = title
        result['content'] = res.content
        return result

    def crawl_youdao(self, url):
        report = {}
        res = self.fetcher.get(url)
        soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf8')
        item_imgs = soup.select('.post-bd img[src!=""]')
        imgs = [item_img['src'] for item_img in item_imgs]
        report['url'] = url
        report['imgs'] = imgs
        report['content'] = res.content
        return report
