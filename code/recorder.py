import datetime
from tkinter import *
import os
import threading
import tkinter as tk
from pyaudio import PyAudio,paInt16
import wave
import urllib.parse
import time
import urllib.request
import json
import hashlib
import base64
import replayworld
from tkinter.simpledialog import*
import random
import requests
from bs4 import BeautifulSoup
from pypinyin import pinyin, lazy_pinyin
# wav相关变量
framerate = 16000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
my_buf = []
pa = PyAudio()
import socket


joke =[
    "最近早上起床，看到枕头上有不少头发，于是上网查一下怎样治脱发。老婆看到了说：“你应该先查一下怎样治打呼噜。”我：“打呼噜和脱发有关系？”\
    她：“你不打呼噜吵着我，我揪你头发干嘛？”我。。。",
    "最近减肥，感觉瘦了1公斤，想想不久的将来我瘦瘦靓靓的模样，不禁一阵心喜，冲着儿子开心滴说：“儿子，你马上就要有个漂亮妈妈喽！哈哈哈。”\
    一旁的老公大喜道：“你是说我可以二婚啦？” 尼玛！",
    "老婆从厕所出来说：真痛快，拉出来得有二斤！不行，我得称一下。\
    我特么真是服了，说：你怎么能干这么恶心的事？我就没见过谁把大便放秤上称的！抬眼望去，老婆站在电子秤上一脸杀气地看着我。。",
    "“你做过最徒劳的一件事是什么？”“脱光衣服站在体重秤上。”",
    "“知道为什么长得丑的有优先发言权吗？”“为什么啊？”“因为‘我丑话说在前面啊。’”",
    "昨天下雨了，刚回家没多久，就传来了急促的敲门，开门看到是隔壁邻居李大爷，问我家是不是起火了？说他闻到有焦臭味，熏得他睁不开眼睛！\
    李大爷还进屋四处查看，还纳闷说，为何没看到烟呢？李大爷，我不过就是袜子被雨水弄湿了，用电吹风吹干而已！",
    "朋友的老婆让我陪她去做体检，查出怀孕了，可是朋友当兵走小半年了。她老婆脸上没有一丝波澜的跟我说：无论任何情况下他知道了，我都会说孩子是你的。。。"
]

# 这个线程用于录音
class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
    def terminate(self):
        self._running = False
    def run(self):
        stream = pa.open(format=paInt16, channels=1,
                         rate=framerate, input=True,
                         frames_per_buffer=NUM_SAMPLES)
        while self._running:
            string_audio_data = stream.read(NUM_SAMPLES)
            my_buf.append(string_audio_data)
            #print('.')
        stream.close()
#回复逻辑
def showreply(speak):
    show = " "

    if  speak.find("在吗") >= 0:
        # messagebox._show("呼唤","主人我在呢~~")
        show = "主人我在呢~~你要需要我帮您做什么，请直接呼唤我就好啦~"
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    elif speak.find("开") >= 0 and speak.find("灯") >= 0:
        # messagebox._show("呼唤", "主人，我已经为您把灯打开了")
        show = "主人~~，我已经为您把灯打开了呢"
        sk = socket.socket()
        sk.connect(("127.0.0.1", 8989))
        sk.sendall(bytes("开灯", encoding="utf-8"))
        sk.close()
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    elif speak.find("关") >= 0 and speak.find("灯") >= 0:
        # messagebox._show("呼唤", "主人，我已经为您把灯关掉了呦")
        sk = socket.socket()
        show = "主人，我已经为您把灯关掉了呦"
        sk.connect(("127.0.0.1", 8989))
        sk.sendall(bytes("关灯", encoding="utf-8"))
        sk.close()
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    elif speak.find("天气") >=0 :
        df = speak.split("天气")[0]
        dfpy = ''.join(lazy_pinyin(df))
        print(df)
        session = requests.session()
        resp = session.get("http://weather.sina.com.cn/"+dfpy)
        resp.encoding = 'utf8'
        soup = BeautifulSoup(resp.text, "html.parser")
        wd = soup.find_all("div", class_="slider_degree")[0]
        tq = soup.find_all("p", class_="slider_detail")[0]
        tq = str(tq.text).strip().replace(" ", "")
        wd = str(wd.text).strip().replace("\n", "")
        tq = str(tq).split("|")
        print(df+"今天气温：%s天气%s,且伴有%s,%s" % (wd, tq[0], tq[1], tq[2]))
        show = df+"今天气温：%s天气%s,且伴有%s,%s" % (wd, tq[0], tq[1], tq[2])
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    elif speak.find("今天") >=0 and speak.find("几月") >=0 :
        i = datetime.datetime.now()
        show = "今天是 %s年%s月%s日星期%s " %(i.year,i.month,i.day,i.weekday())
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    elif speak.find("现在") >=0 and speak.find("几点") >=0 :
        i = datetime.datetime.now()
        show = "现在时间是 %s点%s分钟" % (i.hour,i.minute)
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    elif speak.find("讲") >=0 and speak.find("笑话") >=0 :
        show = joke[random.randint(0,6)]
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    elif speak.find("你") >=0 and speak.find("干什么") >=0 :
        show = "我在这陪你聊天呢~~~有什么需要的尽管告诉我吧~~~  "
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    else:
        #messagebox._show("我好像不太明白你的意思呢")
        show = "我好像不太明白..."
        speaakfilename = replayworld.speaktalk(show)
        listenThread(speaakfilename + ".wav", 1).start()
    ls.insert(END,"小siri:"+show)
# 读取录音内容转化为文字 并且读出来
#其中第一个参数为wav路径，第二个参数为 判断双击还是精灵回复
def main1(st,type):
    print(st)
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
        #录音的文字信息
    #print(result)
    result = result.decode('UTF-8')
    #print(json.loads(result)['data'])
    f.close()
    speak = str(json.loads(result)['data'])
    ls.insert(END, "你：" + json.loads(result)['data'])
    if type :
       showreply(speak)
    else:
        messagebox._show("您所说的内容：", json.loads(result)['data'])

    return


# 存储录音元
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()
    #清空当前的列表 以保证录音不会混合
    del data[:]
# 录音线程对象
#thread1 = myThread()

# 按钮事件
def begin():
    global thread1
    thread1= myThread()
    thread1.start()
    bg['state'] = DISABLED#禁用
    ov['state'] = NORMAL
    label_img.config(image=img_png2)
def over():
    thread1.terminate()
    label_img.config(image=img_png)
    bg['state'] = NORMAL  ###重新激活
    ov['state'] = DISABLED#禁用
    num = 0;
    while True:
        if not os.path.exists(str(num)+".wav"):#如果该文件不存在则以该文件命名
            break;
        num += 1
    save_wave_file(str(num)+'.wav', my_buf)
    #listbox更新条目
    #ls.insert(END, str(num)+".wav")
    print("录音已保存至"+os.getcwd()+"\\"+str(num)+".wav")
    #这条语句是说完话播放自己说的话
    #listenThread(str(num)+".wav",0).start()
    # 为了实现语音精灵 可以不要播放自己说的话 直接让精灵回复您
    main1(os.getcwd()+"\\"+str(num)+".wav",1)

root = tk.Tk()
root.title('智能语音精灵')
root.geometry("500x400+500+150")

bg = tk.Button(root)
bg['text']='开始录音'
bg['command'] = begin

ov = tk.Button(root)
ov['text']='停止录音'
ov['command'] = over
ov['state'] = DISABLED
ls = tk.Listbox(root,width=500)

#摆放位置
ls.pack(side = BOTTOM)
bg.pack(side = TOP)
ov.pack(side = TOP)


root.resizable(width=False, height=True) #宽不可变, 高可变,默认为True
#获取当前目录的所有文件名
fileList = os.listdir(os.getcwd())
for filename in fileList:
    if filename[-4:] == '.wav':
        ls.insert(END,filename)
# 这个线程是播放录音的线程
#第一个参数代表wav路径，第二个参数代表录音播放的是人还是机器

class listenThread(threading.Thread):

    def __init__(self, prams, type):
        super(listenThread, self).__init__()#注意：一定要显式的调用父类的初始化函数。
        self.prams = prams
        self.type = type
    def run(self):#定义每个线程要运行的函数
        chunk = 2014
        wf = wave.open(self.prams, 'rb')
        p = PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=
        wf.getnchannels(), rate=wf.getframerate(), output=True)
        print("开始播放")

        while True:
            data = wf.readframes(chunk)
            if data == b"":
                break
            stream.write(data)
            #print("正在读呢")
        print("播放完毕")
        stream.close()
        p.terminate()
        wf.close()

 # main1函数是把录音转化为文字 如果是双击的话，那么把录音读出来，
        # 如果是机器说话的话，把他说的文件删掉！以免过多
        if self.type == 0:
            main1(self.prams,0)
        else:
            os.remove(self.prams)

def play(event):
    newlisten = listenThread(ls.get(ls.curselection()), 0)
    newlisten.start()


def delet():
    print("第"+str(ls.curselection()[0])+"行被删除")
    os.remove(ls.get(ls.curselection()[0]))
    ls.delete(ls.curselection()[0])
deletemenu = Menu(root, tearoff=0)
deletemenu.add_command(label="删除",command =delet)
deletemenu.add_separator()
def popupmenu(event):
    if  len(ls.curselection())!=0:
        deletemenu.post(event.x_root, event.y_root)

#为ls绑定事件 play
ls.bind('<Double-Button-1>',play)
ls.bind("<Button-3>", popupmenu)
#进入主事件循环
tk.mainloop()

