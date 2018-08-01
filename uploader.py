# -*- coding: utf-8 -*-
# coding=utf-8
import oss2
import logging


# 线下上传配置
OSS_ACCESS_KEY = 'xxxxxx'
OSS_ACCESS_KEY_SECRET = 'xxxxxx'
OSS_BUCKET_NAME = 'xxxxxx'
OSS_ENDPOINT = 'http://example.com'


class Uploader(object):
    bucket = oss2.Bucket(oss2.Auth(OSS_ACCESS_KEY, OSS_ACCESS_KEY_SECRET), OSS_ENDPOINT, OSS_BUCKET_NAME)
    logger = logging.getLogger("Uploader")

    @classmethod
    def upload_file(cls, oss_path, local_path):
        try:
            result = cls.bucket.put_object_from_file(oss_path, local_path)
            cls.logger.info('upload oss result: %s, status : %s' % (result, result.status))
            if result.status != 200:
                cls.logger.error('upload file %s failed with result %s' % (local_path, result.status))
                return False
            else:
                cls.logger.info('upload file %s ok, now remove temp file' % local_path)
                return True
        except Exception as e:
            cls.logger.error('upload file %s failed, error %s' % (local_path, e))
            return False


