# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1
import json

from flask import Response


def make_succ_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def make_succ_response(data):
    data = json.dumps({'code': 0, 'data': data})
    return Response(data, mimetype='application/json')


def make_err_response(err_msg):
    data = json.dumps({'code': -1, 'errorMsg': err_msg})
    return Response(data, mimetype='application/json')
