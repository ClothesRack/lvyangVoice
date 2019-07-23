#-*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
URL = "http://api.xfyun.cn/v1/service/v1/tts"
APPID = "5b3b09ae"
API_KEY = "b7c40c16ab83880566a1924ca95ecd2f"
def getHeader(auf, aue, voiceName, speed, volume, pitch, engineType, textType):
        curTime = str(int(time.time()))
        param = "{\"auf\":\""+auf+"\""
        if aue != "":
            param +=",\"aue\":\" " + aue +"\""

        if voiceName != "":
            param +=",\"voice_name\":\"" + voiceName + "\""

        if speed != "":
            param +=",\"speed\":\"" + speed + "\""

        if volume != "":
            param +=",\"volume\":\"" + volume + "\""

        if pitch != "":
            param +=",\"pitch\":\"" + pitch + "\""

        if engineType != "":
            param +=",\"engine_type\":\"" + engineType + "\""

        if textType != "":
            param +=",\"text_type\":\"" + textType + "\""

        param +="}"

        paramBase64 = base64.b64encode(param.encode("utf-8"))
        paramBase64 = str(paramBase64,encoding="utf-8")

        m2 = hashlib.md5()


        m2.update((API_KEY + curTime +paramBase64).encode("utf8"))
        checkSum = m2.hexdigest()
        header ={
            'X-CurTime':curTime,
            'X-Param':paramBase64,
            'X-Appid':APPID,
            'X-CheckSum':checkSum,
            'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

def getBody(text):
	data = {'text':text}
	return data

def writeFile(file, content):
    with open(file, 'wb') as f:
    	f.write(content)
    f.close()
def speaktalk(strtalk):
    r = requests.post(URL,headers=getHeader("audio/L16;rate=16000", "raw", "xiaoyan", "50", "50", "50", "", "text"),data=getBody(strtalk))
    contentType = r.headers['Content-Type']
    if contentType == "audio/mpeg":
        sid = r.headers['sid']
        writeFile(sid+".wav", r.content)
        #print "success, sid = " + sid
       # print ("sid"+sid)
        #print("绿漾回复语音建立完毕")
        return sid
    else :
        print (r.text)
