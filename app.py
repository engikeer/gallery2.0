import re
from urllib.parse import unquote

from flask import Flask
from flask import render_template
from flask import request
from flask import Blueprint
from flask_paginate import Pagination
import os

app = Flask(__name__, static_url_path='')

mod = Blueprint('img_list', __name__)


@app.route('/', methods=['GET'])
def get_menu():
    # 返回目录名
    root_dir = 'static/gallery'
    dir_list = []
    for parent, dir_names, file_names in os.walk(root_dir):
        dir_list = dir_names
        break

    return render_template('menu.html', dir_names=dir_list)


@app.route("/img", methods=['GET'])
def get_img():
    param = unquote(request.args['dir'])
    page = request.args.get('page', type=int, default=1)
    dir = 'static/gallery/' + param
    rel_dir = 'gallery/' + param
    img_list = []
    for parent, dir_names, file_names in os.walk(dir):

        for file_name in file_names:
            if 'jpg' in file_name.lower():
                full_name = os.path.join(rel_dir, file_name)
                img_list.append(full_name)
        break

    # img_list.sort(key=lambda d: int(d.split('/')[-1].split('.')[0]))

    # 根据数字排序
    img_list.sort(key=
                  lambda x: int(re.match(r'(\d+)([^\d]+)(\d+)\.jpg', x.split('/')[2]).group(1)) * 10
                            + int(re.match(r'(\d+)([^\d]+)(\d+)\.jpg', x.split('/')[2]).group(3)))

    print(img_list)
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get('page', type=int, default=1)
    low = (page - 1) * 25
    up = min(page * 25, len(img_list))
    pagination = Pagination(page=page, total=len(img_list), per_page=25, search=search, record_name='img_list')
    return render_template('detail.html', img_names=img_list[low:up], title=param, pagination=pagination)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
