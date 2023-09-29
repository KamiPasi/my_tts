from flask import request, Flask, Response
import json
import edge_tts
import uuid
import os
import asyncio


server = Flask(__name__)


@server.route('/', methods=["GET"])
def index():
    print('接收')
    # print(request.json())
    # print(request.headers)
    print(str(request.data, 'utf-8'))
    return f"你好，钉钉机器人逻辑处理端已启动<br/>"


@server.route("/", methods=["POST"])
def get_data():
    # 第一步验证：是否是post请求
    # print(request.data)
    # print(str(request.tex, 'utf-8'))
    params = json.loads(str(request.data, 'utf-8'))
    text = params['text'].strip()
    print(text)
    name = str(uuid.uuid1()) + '.mp3'
    path = 'yy/' + str(os.path.sep) + name
    if 'rate' in params.keys():
        print(params['rate'], type(params['rate']))
        rate = int(params['rate'])
        rate = f'+{rate*2}%'
        communicate = edge_tts.Communicate(text, 'zh-CN-YunjianNeural', rate=rate)
    else:
        communicate = edge_tts.Communicate(text, 'zh-CN-YunjianNeural')
    asyncio.run(communicate.save(path))
    def data():
        with open(path, 'rb') as f:
            d = f.read(1024)
            while d:
                yield d
                d = f.read(1024)

    return Response(data(), mimetype='audio/mpeg')


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8999)