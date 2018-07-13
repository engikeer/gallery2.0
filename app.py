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
    rel_path = 'static/gallery'
    dir_list = []
    for parent, dir_names, file_names in os.walk(get_abspath(rel_path)):
        dir_list = dir_names
        break

    return render_template('menu.html', dir_names=dir_list)


@app.route("/img", methods=['GET'])
def get_img():
    param = unquote(request.args['dir'])
    rel_path = 'static/gallery/' + param
    rel_dir = 'gallery/' + param
    img_list = []
    for parent, dir_names, file_names in os.walk(get_abspath(rel_path)):

        for file_name in file_names:
            if 'jpg' in file_name.lower():
                full_name = os.path.join(rel_dir, file_name)
                img_list.append(full_name)
        break

    # 根据数字排序
    img_list.sort(key=sort_name)

    print(img_list)
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get('page', type=int, default=1)
    low = (page - 1) * 50
    up = min(page * 50, len(img_list))
    pagination = Pagination(page=page, total=len(img_list), per_page=50, search=search, record_name='img_list')
    return render_template('detail.html', img_names=img_list[low:up], title=param, pagination=pagination)


def get_abspath(rel_path):
    abs_dir = os.path.split(os.path.abspath(__file__))[0]
    path = os.path.join(abs_dir, rel_path)
    return path


def sort_name(name):
    name_elements = re.match(r'(\d+)([^\d]+)(\d+)\.jpg', name.split('/')[2])
    first_num = int(name_elements.group(1))
    second_num = int(name_elements.group(3))
    return first_num * 1000 + second_num


if __name__ == '__main__':
    app.run(host='0.0.0.0')
