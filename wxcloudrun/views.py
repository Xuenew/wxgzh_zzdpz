# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1
import random
import time
import requests
import json
import pytz

from flask import Response
from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)

# xyy测试热更新
@app.route('/api/test', methods=['get', 'post'])
def wxgzh_zzdpz_project_test():

    return "薛忆阳：》》》》88888888888"+str(time.time()) #

# 获取实时天气预报
@app.route('/api/tianqiyubao', methods=['get'])
def wxgzh_zzdpz_project_tianqiyubao():
    response = requests.get("http://www.weather.com.cn/data/sk/101010100.html")
    response.encoding = response.apparent_encoding
    # print(response.text)
    # return  response.text#
    return make_succ_response(response.text)

# 获取用户信息
@app.route('/api/send_message', methods=['get', 'post'])
def wxgzh_zzdpz_project_send_message():
    params = request.get_json() #
    # params = {
    #     "ToUserName": "gh_064723a33050",
    #     "FromUserName": "oVzmb0vAA3Z2IZXLgiiUM6WoAVbY",
    #     "CreateTime": "",
    #     "Content": "北京",
    #
    # }  #
    #
    request_headers = request.headers
    user_send_to_server_message = params.get("Content","")
    if "天气" in user_send_to_server_message:
        # 和风API接口
        tianqi = requests.get("https://devapi.qweather.com/v7/weather/now?location=101010100&key=d4aa225a004440be8d7fe92bdb244bd9").json()
        # 获取名人名言
        response_mrmy = requests.get("http://api.xiaocongjisuan.com/life/dictum/get?appKey=FEokBpQdh4NY&openId=Yt5NYZtRJp4xE800&currentPage={}&pageSize=10&dType=json".format(random.randint(1,100))).json()
        # print(tianqi)
        city = "北京市"# 城市
        temp = tianqi.get("now",{}).get("temp","") # 温度
        feelsLike = tianqi.get("now",{}).get("feelsLike","") # 体感温度
        weather = tianqi.get("now",{}).get("text","") # 当前天气
        time_ = datetime.strftime(datetime.now().astimezone(pytz.timezone("Asia/Shanghai")), '%Y-%m-%d %H:%M:%S')
        mrmy_inf0 = random.choice(response_mrmy.get("data",{}).get("dictums",[]))
        famal_pepole_name = mrmy_inf0.get("author","")
        famal_pepole_conten = mrmy_inf0.get("content","")
        # text = "城市：{city}\n当前温度：{wd} 体感温度：{SD}\n当前时间：{time_}\n微信号：{wxh}\n{headers}".format(city=city,wd=temp,SD=SD,time_=time_,wxh=params.get("FromUserName",""),
        #                                                                                headers=request_headers)
        text = "城市: {city}\n温度: {temp} 体感温度: {feelsLike}\n今日天气: {weather}\n当前时间: {time_}\n{famal_pepole_name}---{famal_pepole_conten}".format(
            city=city,temp=temp,weather=weather,
            feelsLike=feelsLike,time_=time_,
            famal_pepole_name = famal_pepole_name,famal_pepole_conten=famal_pepole_conten,
            # headers=request_headers
        )
        info = {
            "ToUserName": params.get("FromUserName",""),
            "FromUserName": params.get("ToUserName",""),
            "CreateTime": params.get("CreateTime",""),
            "MsgType": "text",
            "Content": text
        }
        return json.dumps(info,ensure_ascii=False)
    else:
        info = {
            "ToUserName": params.get("FromUserName",""),
            "FromUserName": params.get("ToUserName",""),
            "CreateTime": params.get("CreateTime",""),
            "MsgType": "text",
            "Content": "查询天气请回复 北京天气，其余功能还在完善中。"
        }
        return json.dumps(info,ensure_ascii=False)
