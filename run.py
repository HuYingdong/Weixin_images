# coding=utf-8
from tasks import save
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import logging
import config
from mongo_helper import MongoHelper

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SECRET_KEY'] = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:' \
                           'U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        data = request.form.to_dict()
        url = data.get('url')
        task_id = data.get('task_id')
        notice_url = data.get('notice_url')

        if not url or not task_id or not notice_url:
            flash('请输入完整的信息！')
            return redirect(url_for('main'))

        task = {
            'task_id': task_id,
            'url': url,
            'notice_url': notice_url,
        }
        logger.info('get task: %s', task)

        client = MongoHelper(config.task_db)
        if client.add_item(col_name='tasks', doc=task):
            task['recorded'] = True
        else:
            task['recorded'] = False

        if task['recorded']:
            flash('添加任务成功: ' + url)
            save(task_id, url, notice_url)
        else:
            flash('添加任务失败: ' + url)
        return redirect(url_for('main'))

    client = MongoHelper(config.task_db)
    tasks_info = client.get_info(col_name='tasks')

    return render_template('index.html', tasks=tasks_info)


# 测试 notice_url
@app.route('/notice', methods=['POST'])
def notice():
    job_form = request.form.to_dict()
    return jsonify(job_form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

# 启动huey
# python huey_consumer.py tasks.huey --logfile=./logs/huey.log
