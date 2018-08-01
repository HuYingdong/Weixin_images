# -*- coding: utf-8 -*-
import time
import random
import uuid
import os
import requests
import hashlib
from uploader import Uploader


def download_imgs(img_dir, imgs):
    img_maps = []
    for img in imgs:
        img_map = {'source_url': img}
        # img补全
        if '/640' in img and 'wx_fmt=' not in img:
            img = img.split('/640')[0] + '/640?wx_fmt=png'
        ext = img.split('wx_fmt=')[-1]
        if len(ext) > 5:
            continue
        img_map['ext'] = ext
        res = requests.get(img)
        clength = dict(res.headers)['Content-Length']
        img_map['size'] = clength
        if not os.path.isdir(img_dir):
            os.mkdir(img_dir)
        path = img_dir + str(time.time()).replace('.', '_') + str(
            uuid.uuid4()).split('-')[0] + '.' + ext
        img_map['local_path'] = path
        with open(path, 'wb') as f:
            f.write(res.content)
        img_maps.append(img_map)
    return img_maps


def get_file_md5(file_path):
    md5 = ''
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            md5 = str(hash_code).lower()
    return md5


def upload(img_map):
    local_path = img_map['local_path']
    # 上传
    oss_path = 'wechat/' + local_path
    upload_res = Uploader.upload_file(oss_path, local_path)
    if upload_res:
        img_map['oss_path'] = oss_path
        os.remove(local_path)
        return img_map
    else:
        return False


def upload_art(report, oss_map):
    html_content = report['content']
    if 'data-src' in html_content:
        html_content = html_content.replace('data-src', 'src')

    for k, v in oss_map.items():
        v = 'http://abc-crawler.oss-cn-hangzhou.aliyuncs.com/' + v.encode('utf8')
        html_content = html_content.replace(k.encode('utf8'), v)

    html_dir = 'htmls/'
    if not os.path.isdir(html_dir):
        os.mkdir(html_dir)
    html_path = html_dir + get_random_name() + '.html'
    with open(html_path, 'wb') as fp:
        fp.write(html_content)
    size = os.path.getsize(html_path)
    report['file_size'] = size
    report['file_path'] = html_path

    # 上传
    if report['file_path'] != '':
        oss_path = 'wechat/' + str(uuid.uuid4()).replace('-', '') + '.html'
        upload_res = Uploader.upload_file(oss_path, report['file_path'])
        # upload_res = True
        if upload_res:
            report['oss_path'] = oss_path
            report['export_flag'] = False
            report['downloaded'] = True
            # 将本地临时文件删除
            os.remove(report['file_path'])
            report['oss_failed'] = False
        else:
            report['oss_failed'] = True
    else:
        report['oss_failed'] = True
    return report


def get_random_name():
    return str(int(time.time())) + get_zfill_random_number(3) + get_zfill_random_number(3)


def get_random_number(from_num, to_num=100):
    return random.randint(from_num, to_num)


def get_zfill_random_number(n):
    width = n
    if width < 1:
        width = 1
    s = "1"
    for i in range(1, width):
        s += "0"
    to_num = int(s)
    r = get_random_number(0, to_num)
    return str(r).zfill(width)

