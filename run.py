# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1

# 创建应用实例
import sys

from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
