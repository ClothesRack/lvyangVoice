#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.parse
import time
import urllib.request
import json
import hashlib
import base64
import replayworld

def main(st):
    f = open(st, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'audio': base64_audio}).encode(encoding="utf8")

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = '9905a557529123505a6374dbfab482a7'
    param = {"engine_type": "sms16k", "aue": "raw"}
    x_appid = '5b3b09ae'
    x_param = base64.b64encode((json.dumps(param).replace(' ', '')).encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)

    x_param = str(x_param,encoding="utf8")

    x_checksum = hashlib.md5((api_key + str(x_time) + x_param).encode("utf8")).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    urllib.parse.urlencode(x_header).encode(encoding='UTF8')
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    f.close()
    print("识别状态："+str(json.loads(result.decode('UTF-8'))['desc']))
    return result.decode('UTF-8')

if __name__ == '__main__':
    main()