# 创建应用实例
import sys
import time

from wxcloudrun import app
# xyy测试热更新
@app.route('/api/test', methods=['get', 'post'])
def wxgzh_zzdpz_project_test():
        return "薛忆阳：》》》》"+str(time.time()) #

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
