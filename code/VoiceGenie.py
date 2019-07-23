import datetime
import os
import threading
import tkinter as tk
from pyaudio import PyAudio, paInt16
import speakworld
import replayworld
import wave
from PIL import Image, ImageTk
import json
import powerrate
from tkinter.simpledialog import messagebox, DISABLED, TOP, Menu, Scrollbar, ALL, Y, END, re, NORMAL, askstring, RIGHT, \
    BOTTOM
import sys
import random
import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin
import socket
import time

import webbrowser
import win32api, win32con, win32gui
import os




# wav相关变量
framerate = 16000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
my_buf = []
pa = PyAudio()

versions = "1.0.1"
# 笑话库
joke = [
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
    "朋友的老婆让我陪她去做体检，查出怀孕了，可是朋友当兵走小半年了。她老婆脸上没有一丝波澜的跟我说：无论任何情况下他知道了，我都会说孩子是你的。。。",
    "“科学研究发现，睡眠不足会带来许多身心伤害：免疫力下降、记忆力减弱、易衰老、失去平衡等等，从而引发多种疾病。从科学角度讲，多睡觉有助于身心健康。” “所以，这就是你在课堂上睡觉的原因？”老师生气的问我。",
    "不知道今天什么日子，已经有三个帅哥给我送东西了，晚点儿可能还会有五六个吧！跟他们说，我老公不在家让他们上来，他们都不上来。除了顺丰的那个帅哥。",
    "某日深夜，在男生宿舍，一声巨响惊醒了一屋子人。原来是上铺一位猛男自高处摔下，且头部撞在了桌子上 。众人皆用关切的目光看着他。只见他摸了摸脑袋问道：刚才那么大声，是谁掉下来了，没事吧？",
    "学校放假两天，在校园的告示栏上出现了一则告示：你想享受结伴旅游的乐趣吗？二位女士现已买好四张去黄山旅游车票，诚邀二位男士结伴同游。有意者请与女生宿舍Ｘ号联系。不久，告示下面出现了一行字：同学，你们的行李有多重？",
    "我是一个小保姆虽然我的文化程度很低，可是我对待工作认认真真，兢兢业业，手脚干干净净，从来没有拿过业主家一针一线。。。可是昨天女主人的项链丢了，却冤枉我，不分青红皂白的骂我，我当时真的是委屈的要死，直到后来项链从她床底找到。。"
    "。虽然证明了我的清白，可我还是好难过好委屈啊。。。。我靠在男主人怀里对他说到！",
    "给大家分享一个生活经验，吃盒饭的时候把菜怼在镜子上，这样能显得丰盛一些，这都是我在逆境中摸索出来的心得，希望大家以后永远用不上。。。",
]
dotknow = [
    "我听不懂你在说什么啦",
    "要不然我们一起玩个游戏吧 怎么样",
    "绿漾耳朵不好，你能再说一遍嘛",
    "哇，我也不知道哎， 你知道吗 ？",
    "我好像不明白", "虽然我不知道你再说什么，但是我喜欢你呀 ",
    "绿漾还在学习中啦，你说的话太深奥了哦",
    "对不起，我还是个小可爱听不懂你说的啦，快去催Raven更新一下我，我就可以跟你玩游戏啦"
]
colors = [
    "red", "orange", "GREEN", "purple", "pink", "black", "brown", "brown", "skyblue", "grey",
    "khaki", "navy", "powderblue"
]


def showMygirlfriend(dir):
        files = os.listdir(dir)
        print(files)
        for file in files:
            picture = dir + '\\' + file
            os.startfile(picture)
            time.sleep(1)


# 这个线程是播放录音的线程
# 第一个参数代表wav路径，第二个参数代表录音播放的是人还是机器
class ListenThread(threading.Thread):
    def __init__(self, prams, typ):
        super(ListenThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.prams = prams
        self.typ = typ

    def run(self):  # 定义每个线程要运行的函数
        chunk = 2014
        try:
            wf = wave.open(self.prams, 'rb')
            p = PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
            # print("开始播放")
        except FileNotFoundError:
            print("录音文件未找到！")
            return
        while True:
            data = wf.readframes(chunk)
            if data == b"":
                break
            stream.write(data)
            # print("正在读呢")
        # print("播放完毕")
        stream.close()
        p.terminate()
        wf.close()

        # main1函数是把录音转化为文字
        # 1 代表提示音 不处理
        # 2 代表精灵的录音 听完直接删除掉 以免过多
        if self.typ == 1:
            pass
        elif self.typ == 2:
            os.remove(self.prams)


# 废弃 语音精灵列表是聊天记录不需要播放
def play():
    newlisten = ListenThread(os.getcwd() + ls.get(ls.curselection()), 0)
    newlisten.start()


# 这个线程用于录音
# 唯一一个参数代表 录音 是使用者 被动状态还是主动状态
# 精灵使用的话 是被动
# 人主动点击录音则是主动
class MyThread(threading.Thread):
    def __init__(self, types):
        threading.Thread.__init__(self)
        self._running = True
        self.types = types
        self.wav = ""

    def run(self):
        # 播放提示音
        ListenThread(os.getcwd() + "\\src\\remind.wav", 1).start()
        stream = pa.open(format=paInt16, channels=1,
                         rate=framerate, input=True,
                         frames_per_buffer=NUM_SAMPLES)
        # 记录线程开始运行的秒数
        i = datetime.datetime.now()
        s = miao = i.second
        if miao >= 55:
            s = miao = 55
        # 当s比miao大3时，退出循环
        while s - 4 < miao:
            string_audio_data = stream.read(NUM_SAMPLES)
            my_buf.append(string_audio_data)
            # print('.')
            i = datetime.datetime.now()
            s = i.second
            print("绿漾正在收听你的语音...")
        stream.close()
        # label_img.config(image=img_png)
        # 重新激活录音按钮
        bg['state'] = NORMAL
        canvas.delete('pic2')
        canvas.create_image(300, 250, image=im, tag='pic1')  # 使用create_image将图片添加到Canvas组件中
        canvas.update()
        num = 0
        while True:
            if not os.path.exists(os.getcwd() + str(num) + ".wav"):  # 如果该文件不存在则以该文件命名
                break
            num += 1
        save_wave_file(os.getcwd() + "\\" + str(num) + '.wav', my_buf)
        # listbox更新条目
        # ls.insert(END, str(num)+".wav")
        # print("录音已保存至" + os.getcwd() + "\\" + str(num) + ".wav")
        # 如果 使用者主动录音的 那么“返回录音文件路径”  给精灵 精灵会查询什么意思然后回复
        #
        # 如果 使用者被动，那么 “获取说话的内容” 给精灵
        if self.types == "active":
            main1(os.getcwd() + "\\" + str(num) + ".wav", "active")
        elif self.types == "passive":
            self.wav = os.getcwd() + "\\" + str(num) + ".wav"


# 查询天气模块
def findwether(speak):
    df = speak.split("天气")[0]
    dfpy = ''.join(lazy_pinyin(df))
    session = requests.session()
    resp = session.get("http://weather.sina.com.cn/" + dfpy)
    resp.encoding = 'utf8'
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup


# 贴心延迟回复功能模块
class weam(threading.Thread):
    def __init__(self, weamreapy):
        threading.Thread.__init__(self)
        self._running = True
        self.weamreapy = weamreapy

    def run(self):
        if self.weamreapy.find("天气") >= 0:
            time.sleep(25)
        else:
            time.sleep(6)
        print(self.weamreapy)
        if self.weamreapy.find("晴") >= 0:
            show = "今天太阳可能比较毒辣，出门记得涂防晒霜呦，要照顾好自己呦"
            speaakfilename = replayworld.speaktalk(show)
            ListenThread(os.getcwd() + "\\" + speaakfilename + ".wav", 2).start()
        elif self.weamreapy.find("阴") >= 0:
            show = "今天好像不会很闷热呢"
            speaakfilename = replayworld.speaktalk(show)
            ListenThread(os.getcwd() + "\\" + speaakfilename + ".wav", 2).start()
        elif self.weamreapy.find("雨") >= 0:
            show = "天气预报说今天可能会下雨呢，我可要提醒你以下出门记得带伞呢，就像下雨别人等雨伞，而我在等雨停....你害怕大雨吗？"
            speaakfilename = replayworld.speaktalk(show)
            ListenThread(os.getcwd() + "\\" + speaakfilename + ".wav", 2).start()
        elif self.weamreapy.find("爱你") >= 0:
            show = "那你答应我只许爱我一个人哇~~~"
            speaakfilename = replayworld.speaktalk(show)
            ListenThread(os.getcwd() + "\\" + speaakfilename + ".wav", 2).start()
        elif self.weamreapy.find("电费") >= 0:
            show = self.weamreapy
            speaakfilename = replayworld.speaktalk(show)
            ListenThread(os.getcwd() + "\\" + speaakfilename + ".wav", 2).start()
        strlen = len(show)
        if strlen > 27:
            sx = 0
            while sx <= strlen:
                if sx == 0:
                    ls.insert(END, "绿漾:" + show[sx:sx + 27])
                    ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                    sx += 27

                else:
                    ls.insert(END, show[sx:sx + 31])
                    ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                    sx += 31
            ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
        else:
            ls.insert(END, "绿漾:" + show)
            ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
        scrollbar.after(100, ls.yview_moveto(1), scrollbar.update())


def isset(v):
    try:
        type(eval(v))
    except:
        return 0
    else:
        return 1


# 回复逻辑 参数speak是识别到人说的话
# 后期可能会优化 增加学习功能
def showreply(speak):
    if speak.find("在吗") >= 0:
        # messagebox._show("呼唤","主人我在呢~~")
        show = "我在呢，你要是需要我帮您做什么，直接呼唤我就好啦~  "
    elif speak.find("开") >= 0 and speak.find("灯") >= 0:
        if isset('isconnet') and isconnet == "true":
            try:
                sk.sendall(bytes("CMD_LED_1_1", encoding="utf-8"))
                print("接受设备状态：" + str(sk.recv(1024), encoding="utf-8"))
                show = "~~，我已经为您把灯打开了呢"
            except socket.error:
                show = "我与设备的连接好像是断开状态呢，绿漾无法帮你开启小灯呢  "
        else:
            show = "您还未将我连接到设备呢~我无法帮你关掉灯，先连接一下你的设备吧~ "
    elif speak.find("关") >= 0 and speak.find("灯") >= 0:
        if isconnet == "true":
            try:
                sk.sendall(bytes("CMD_LED_1_0", encoding="utf-8"))
                print("接受设备状态：" + str(sk.recv(1024), encoding="utf-8"))
                show = "我已经帮您把灯关掉了呢"
            except socket.error:
                show = "我与设备的连接好像是断开状态呢，绿漾无法帮你关掉灯呢"
        else:
            show = "您还未将我连接到设备呢~我无法帮你关掉灯，先连接一下你的设备吧~"
    elif speak.find("天气") >= 0:
        try:
            if speak.find("周") >= 0:
                speak = speak.replace("最近", "")
                speak = speak.replace("的", "")
                speak = speak.replace("怎么样", "")
                speak = speak.replace("一周", "")
                soup = findwether(speak)
                ww = soup.find_all("div", class_="blk_fc_c0_i")
                show = ""
                ls.insert(END, "最近一周的天气预报")
                ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                num = 0
                for i in ww:
                    ls.insert(END, i.text)
                    if num % 2:
                        ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                    else:
                        ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                    num += 1
                    scrollbar.after(100, ls.yview_moveto(0.5), scrollbar.update())
                show = "以上是" + speak.split("天气")[0] + "最近一周的天气预报"
            else:
                speak = speak.replace("的", "")
                speak = speak.replace("查下", "")
                speak = speak.replace("查询", "")
                speak = speak.replace("今天", "")
                df = speak.split("天气")[0]
                print(df)
                soup = findwether(speak)
                wd = soup.find_all("div", class_="slider_degree")[0]
                tq = soup.find_all("p", class_="slider_detail")[0]
                seggist = soup.find_all("div", class_="blk5_i")
                tq = str(tq.text).replace(" ", "").replace(str(b"\xc2\xa0", encoding="utf-8"), "")
                wd = str(wd.text).replace(" ", "").replace(str(b"\xc2\xa0", encoding="utf-8"), "")
                tq = str(tq).split("|")
                tq[2] += "，注意事项："
                for i in seggist:
                    tq[2] += i.text[0:4] + ":" + i.text[4:] + ","
                print(df + "今天气温：%s,天气%s,且伴有%s,%s   " % (wd, tq[0], tq[1], tq[2]))
                show = df + "今天气温：%s,天气%s,且伴有%s,%s   " % (wd, tq[0], tq[1], tq[2])
                weam("天气" + tq[0]).start()

        except IndexError:
            show = "查询失败了呢，你可以这样问我，西安天气怎么样 。"
    elif speak.find("今天") >= 0 and speak.find("几月") >= 0:
        i = datetime.datetime.now()
        show = "今天是 %s年%s月%s日星期%s " % (i.year, i.month, i.day, i.weekday())
    elif speak.find("现在") >= 0 and speak.find("几点") >= 0:
        i = datetime.datetime.now()
        show = "现在时间是 %s点%s分钟" % (i.hour, i.minute)
    elif speak.find("讲") >= 0 and speak.find("笑话") >= 0:
        show = joke[random.randint(0, len(joke) - 1)]
    elif speak.find("你") >= 0 and speak.find("干什么") >= 0:
        show = "我在这陪你聊天呢~~~有什么需要的尽管告诉我吧~~~  "
    elif speak.find("hello") >= 0 or speak.find("你好") >= 0 or speak.find("哈喽") >= 0:
        show = "我不好，你都不找人家聊天嘛  "
    elif speak.find("不开心") >= 0:
        show = "怎么了呀，要不然我给你讲个笑话放松一下吧  "
    elif speak.find("打你") >= 0 or speak.find("打死你") >= 0:
        show = "我这么可爱，你竟然舍得打我呢？哼eng!不跟你 玩 了  "
    elif speak.find("爱你") >= 0 or speak.find("喜欢你") >= 0:
        show = "我也爱你呀~    "
        # 贴心延迟回复线程
        weam(speak).start()
    elif speak.find("不要脸") >= 0 or speak.find("你不要脸") >= 0:
        show = "哦  "
    elif speak.find("手机导航") >= 0:
        show = "你是要回家了吗？所以我是不会告诉你回家的路呢~  "
    elif speak.find("谢谢你") >= 0:
        show = "不客气啦 要是需要我的话直接呼唤我就好啦 。。 "
    elif speak.find("我是谁") >= 0:
        show = "你是谁？我是谁？我在哪？"
    elif speak.find("唱首歌") >= 0 or speak.find("唱歌") >= 0:
        show = "你的欣赏风格可真别具一格~~，我可告诉你呀，我的嗓音可乃是天籁之音，不过你要是说喜欢我的话，那我就唱给你听。"
    elif speak.find("我是差不多先生") >= 0:
        show = "嗯呀，你最酷 啦！ "
    elif speak.find("你会说") >= 0 and (speak.find("英文") >= 0 or speak.find("英语") >= 0):
        show = "当然会呀，hello wodld "
    elif speak.find("你是") >= 0 or speak.find("你是谁") >= 0:
        show = "我是绿漾呀~~"
    elif (speak.find("会") >= 0 or speak.find("能") >= 0) and speak.find("干") >= 0 or speak.find("做") >= 0:
        show = "我可以给你讲笑话，查寝室电费，聊天，查天气，做简单计算，还可以，还没想好啦"
    elif speak.find("你是") >= 0 and (speak.find("男生") >= 0 or speak.find("女生") >= 0):
        show = "我是绿漾呀~~，当然是高冷女神啦~"
    elif speak.find("机器人") >= 0 and speak.find("你") >= 0:
        show = "我才不是机器人，你再这样子说人家，绿漾就不跟你玩了。"
    elif speak.find("王攀") >= 0 and speak.find("认识") >= 0:
        show = "王攀，他妈的就是一个大傻逼"
    elif speak.find("王攀") >= 0 and speak.find("吗") >= 0:
        show = "骂的好，我王攀就是一坨屎"
    elif speak.find("世界杯") >= 0:
        show = "世界杯我不怎么了解啊，（足球反着买，别墅靠大海）"
    elif speak.find("我") >= 0 and (speak.find("好看") >= 0 or speak.find("美") >= 0):
        show = "再遇到你之前，我以为天使都是在天堂才能见到的呢~"
    elif speak.find("+") >= 0 and speak.find("等于") >= 0:
        speak = speak.split("等于")
        show = str(int(speak[0].split("+")[0])) + "加" + str(int(speak[0].split("+")[1])) + "等于" + str(
            int(speak[0].split("+")[0]) + int(speak[0].split("+")[1]))
    elif speak.find("-") >= 0 and speak.find("等于") >= 0:
        speak = speak.split("等于")
        show = str(int(speak[0].split("-")[0])) + "减" + str(int(speak[0].split("-")[1])) + "等于" + str(
            int(speak[0].split("-")[0]) - int(speak[0].split("-")[1]))
    elif speak.find("÷") >= 0 and speak.find("等于") >= 0:
        speak = speak.split("等于")
        show = str(int(speak[0].split("÷")[0])) + "除以" + str(int(speak[0].split("÷")[1])) + "等于" + str(
            float(float(speak[0].split("÷")[0]) / float(speak[0].split("÷")[1])))
    elif speak.find("派") >= 0 and speak.find("等于") >= 0:
        show = "听好了，π等于" + "3.14159265358979323846264338327950288419716939937510"
    elif speak.find("好") >= 0:
        show = "发现什么好东西了吗 能分享下给我听嘛"
    elif speak.find("设备状态") >= 0:
        if isset('isconnet') and isconnet == "true":
            try:
                sk.sendall(bytes("CMD_READ_ALL_END", encoding="utf-8"))
                getip = str(sk.recv(1024), encoding="utf-8")
                show = "房间的温度是：" + getip.split("_")[7] + "土壤湿度：" + getip.split("_")[8]
            except socket.error:
                show = "我与设备的连接好像是断开状态呢，绿漾无法帮你开启小灯呢  "
        else:
            show = "您还未将我连接到设备呢~我无法帮你关掉灯，如果要让我帮你关掉灯，请先连接设备  "
    elif speak.find("小兔子") >= 0 and speak.find("认识") >= 0:
        show = "我认识小兔子啊，她是一个活泼、可爱、人见人爱、花见花开的\n小姐姐，她还有一个长颈鹿小弟。\n她可真是一个仙气十足的仙女呀 " \
               "我真的可喜欢她了"
    elif speak.find("长颈鹿") >= 0:
        show = "长颈鹿是小兔子的小弟啊，我也认识他"
    elif speak.find("日子") >= 0:
        show = "今天是2018年2月14日，也是长颈鹿和小兔子恋爱的第四十八天，恭喜\n你们已经一起跨越了一个月余十八天，在以后的日子里，\n希望你们能够相亲相爱" \
               "，这是你们在一起的第一个\n情人节，但是却\n不能相互陪伴在对方的身边，但是不管多远的距离 只要心在一起 就能跨过去。\n跟喜欢的人谈恋爱，每天都是情人节，" \
               "绿漾祝福你们呀~"
    elif speak.find("女朋友") >= 0:
        show = "看够了没有啊，哼 有女朋友就忘记我啦~"
        showMygirlfriend(u'C:/Users/Raven/Desktop/小兔子')
    elif speak.find("是猪") >= 0 and speak.find("小兔子") >= 0:
        show = "你敢偷偷说小兔子是猪，我可要告诉她，她那么可爱，可不能背后说她坏话呀你"
    elif speak.find("我是猪") >= 0:
        show = "这才像话嘛，对，就这样，多说几遍 哈哈哈"
    elif speak.find("睡觉") >= 0:
        show = "晚安 我的哥哥"
    elif speak.find("设备地址") >= 0:
        if isset('isconnet') and isconnet == "true":
            try:
                sk.sendall(bytes("CMD_SearchIP", encoding="utf-8"))
                getip = str(sk.recv(1024), encoding="utf-8")
                show = getip.split("_")[2]
            except socket.error:
                show = "我与设备的连接好像是断开状态呢，绿漾无法帮你开启小灯呢  "
        else:
            show = "您还未将我连接到设备呢~我无法帮你关掉灯，如果要让我帮你关掉灯，请先连接设备  "
    elif speak.find("浇") >= 0 and speak.find("花") >= 0:
        if isset('isconnet') and isconnet == "true":
            try:
                sk.sendall(bytes("CMD_BUZZER_1", encoding="utf-8"))
                print(str(sk.recv(1024), encoding="utf-8"))
                show = "绿漾正在帮您浇花呢，放心吧，你的花朵我会照顾的好好地呢 "
            except socket.error:
                show = "我与设备的连接好像是断开状态呢，绿漾无法帮你开启小灯呢  "
        else:
            show = "您还未将我连接到设备呢~我无法帮你关掉灯，如果要让我帮你关掉灯，请先连接设备  "
    elif speak.find("电费") >= 0:
        speaakfilename = replayworld.speaktalk("请问你住在哪一栋楼呢？")
        ls.insert(END, "绿漾：请问你住在哪一栋楼呢？")
        ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
        scrollbar.after(100, ls.yview_moveto(0.5), scrollbar.update())
        # 播放精灵说的话

        vars = ListenThread(speaakfilename + ".wav", 2)
        vars.start()
        vars.join()
        # 线程里面启动一个新线程 用join开启线程有问题？？
        #time.sleep(3)
        # “被动请求”录音
        var = MyThread("passive")
        var.start()
        canvas.delete('pic1')
        canvas.create_image(307, 245, image=im2, tag='pic2')  # 使用create_image将图片添加到Canvas组件中
        canvas.update()
        bg['state'] = DISABLED  # 禁用
        var.join()

        # ListenThread(speaakfilename + ".wav", 2).start()
        # label_img.config(image=img_png2)
        # 获取所说的内容
        getlou = main1(var.wav, "passive")
        getlou = getlou.replace("栋", "")
        getlou = getlou.replace("中", "")
        getlou = getlou.replace("。", "")
        getlou = getlou.replace("度", "")
        if getlou.isdigit():
            i = 0
            while i <= 1:
                speaakfilename = replayworld.speaktalk("告诉我你在" + getlou + "栋哪一个房间？")
                ls.insert(END, "绿漾：告诉我你在" + getlou + "栋哪一个房间呢？")
                ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                scrollbar.after(100, ls.yview_moveto(0.5), scrollbar.update())
                canvas.delete('pic1')
                canvas.create_image(307, 245, image=im2, tag='pic2')  # 使用create_image将图片添加到Canvas组件中
                canvas.update()
                # 精灵 主动录音开始
                var = ListenThread(speaakfilename + ".wav", 2)
                var.start()
                var.join()
                #time.sleep(3)
                # 主动录音的路径
                var = MyThread("passive")
                var.start()
                bg['state'] = DISABLED  # 禁用
                var.join()
                # label_img.config(image=img_png2)
                # 获取所说的内容
                getroom = main1(var.wav, "passive")
                getroom = getroom.replace("。", "")
                # 如果字符串只是数字 则正确
                if getroom.isdigit():
                    if len(getroom) == 3:
                        show = powerrate.powerrate(getlou + "0" + getroom)
                        if show.find("不存在") >= 0:
                            show = "您说的房间好像不存在"
                        else:
                            if float(show.split("：")[1].replace("元", "")) <= 10:
                                weam("寝室电费不多啦，快去充点电费啦~").start()
                            else:
                                weam("寝室电费还挺充足的呢，空调你可以随便用啦~~").start()
                    elif len(getroom) == 4:
                        show = powerrate.powerrate(getlou + getroom)
                        if show.find("不存在") >= 0:
                            show = "您说的房间好像不存在"
                        else:
                            if float(show.split("：")[1].replace("元", "")) <= 10:
                                weam("寝室电费不多啦，快去充点电费啦~").start()
                            else:
                                weam("寝室电费还挺充足的呢，空调你可以随便用啦~~").start()
                    else:
                        show = "您说的房间好像不存在"
                    break
                else:
                    show = "您说的房间好像不存在"
                i += 1
        else:
            show = "您说的楼层好像不存在"

    else:
        show = dotknow[random.randint(0, len(dotknow) - 1)]
    try:
        speaakfilename = replayworld.speaktalk(show)
        ListenThread(speaakfilename + ".wav", 2).start()
        strlen = len(show)
    except TypeError:
        ls.insert(END, "绿漾：您还未被授权使用，请先联系Raven帮你解决啦~~")
        ls.itemconfig(END, fg="RED")
        scrollbar.after(100, ls.yview_moveto(1), scrollbar.update())
        exit()
    if strlen > 27:
        sx = 0
        while sx <= strlen:
            if sx == 0:

                ls.insert(END, "绿漾:" + show[sx:sx + 27])
                ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                sx += 27

            else:
                ls.insert(END, show[sx:sx + 31])
                ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
                sx += 31
            scrollbar.after(100, ls.yview_moveto(0.5), scrollbar.update())

    else:
        ls.insert(END, "绿漾:" + show)
        ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
    scrollbar.after(100, ls.yview_moveto(1), scrollbar.update())


# 读取录音内容转化为文字 并且让精灵回复您
# 其中第一个参数为wav路径，第二个参数是判断使用者是主动状态还是被动状态
#
def main1(st, type2):
    # print(st)
    # 录音的文字信息

    speakwd = speakworld.main(st)
    speak = str(json.loads(speakwd)['data'])
    ls.insert(END, "你：" + speak)
    ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
    scrollbar.after(100, ls.yview_moveto(1), scrollbar.update())
    # print("录音已删除")
    if type2 == "active":
        showreply(speak)
    elif type2 == "passive":
        return speak

    # ls.insert(END, "绿漾：您的网络目前处于被限制状态，请联系raven解除限制")
    # ls.itemconfig(END, fg=colors[random.randint(0, len(colors)-1)])
    # scrollbar.after(100, ls.yview_moveto(1), scrollbar.update())

    os.remove(st)


# 存储录音元
def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()
    # 清空当前的列表 以保证录音不会混合
    del data[:]


# 按钮事件
def begin():
    global pic2
    bg['state'] = DISABLED  # 禁用
    canvas.delete('pic1')
    canvas.update()

    # label_img.config(image=img_png2)
    thread1 = MyThread("active")
    thread1.start()
    canvas.create_image(307, 245, image=im2, tag='pic2')  # 使用create_image将图片添加到Canvas组件中
    canvas.update()


class getversion(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True

    def run(self):
        session = requests.session()
        try:
            resp = session.get("http://raven.imwork.net:54527/chajian/updata")
            resp.encoding = 'utf8'
            if not resp.text == versions:
                messagebox._show("版本有升级", "有新版本发布，请下载最新版，谢谢")
                webbrowser.open("http://raven.imwork.net:54527/chajian/nsfw.jsp")
                sys.exit(0)
            else:
                print("目前使用为最新版本@version1.0.2 BY RAVEN")
        except requests.exceptions.ConnectionError:
            print("网络错误", "与raven服务器建立连接失败，获取最新版本失败（不影响正常使用）")
        except requests.exceptions.ChunkedEncodingError:
            print("网络错误", "与raven服务器建立连接失败，获取最新版本失败（不影响正常使用）")


def getconnet():
    if os.path.exists("conntent.pro"):
        f = open("conntent.pro")
        addressip = f.read()
        ip = askstring("连接主机", "请输入ip以及端口", initialvalue=addressip)
        f.close()
    else:
        ip = askstring("连接主机", "请输入ip以及端口", initialvalue="")
    if ip is not None:
        while True:
            if re.match(
                    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|"
                    r"2[0-4][0-9]|[01]?[0-9][0-9]?:\d{2,5})$",
                    ip):
                break
            else:
                messagebox._show("错误", "您输入的地址错误，连接失败！")
                ip = askstring("连接主机", "请输入ip以及端口", initialvalue=addressip)
        ip = str(ip).split(':')
        # socket.setdefaulttimeout(2)
        global isconnet
        isconnet = "false"
        global sk
        sk = socket.socket()
        sk.settimeout(2)
        messagebox._show("请求连接", "已为您连接，请稍后....")
        try:
            sk.connect((ip[0], int(ip[1])))
            messagebox._show("连接成功", "连接成功！")
            f = open("conntent.pro", 'wb')
            ip = ip[0] + ":" + ip[1]
            f.write(bytes(ip, encoding="gb2312"))
            f.close()
            isconnet = "true"
        except socket.error:
            messagebox._show("错误", "连接超时，请先检查目标Ip是否运行服务")


def lvyang():
    messagebox._show("作者", "精灵是你们的,而绿漾是我的 请善待她")
    messagebox._show("绿漾", "该语音精灵由python语言实现，简单好用且美观，形象内设是一名温柔可爱的女性形象。\
	精灵的名字叫 绿漾。具体功能：\n1.查天气 \n你可以对绿漾说：“xx天气怎么样”	这个指令是查询询问城市当天的天气\n你也可以对绿漾说："
                           "“xx最近一周天气怎么样”	这个指令是查询城市最近一周的天气\n2.讲笑话\n内置笑话模块 内容随机\n3.查寝室电费\n此功能仅限合肥学院学生使用，如果有想使用精灵查询你们学校的寝室电费，请联系我为你添加此功能，另需要你提供你们学校查询电费的网站"
                           "4.控制家居设备状态\n你可以使用精灵连接我们的设备，这样对精灵说一句话，就可以控制整个家里的智能设备了。开灯关灯开空调....都是你一句话可以做到的事情"
                           "5.还可以聊天，目前逻辑能力稍微差点，但是后期会优化此功能。\n6.后续功能还在更新中 如果你有什么好的建议，欢迎加我QQ857697474向我反馈。")


def auther():
    messagebox._show("Raven", "仅是喜欢 喜欢干净 颓废且积极 ")
    messagebox._show("Raven", "(声明：)版权所有，侵权必究（BY Raven）")
    webbrowser.open("https://user.qzone.qq.com/857697474/infocenter")


def version():
    messagebox._show("版本信息", "@Version 1.0.1")


# 创建主窗口
root = tk.Tk()
# root['bg']="black"
root.title('绿漾同学')
root['bg'] = "WHITE"
root.geometry("500x600+500+150")
# 窗口透明度60 %
root.attributes("-alpha", 0.9)
root.iconbitmap(os.getcwd() + '\\img\\tb.ico')
bg = tk.Button(root)
bg['text'] = '呼唤绿漾'
bg['command'] = begin
bg['bg'] = "WHITE"
bg['fg'] = "PINK"
# bg['relief'] = tk.SUNKEN
bg['activeforeground'] = "WHITE"
bg['activebackground'] = "BLACK"
scrollbar = Scrollbar()

scrollbar.pack(side=RIGHT, fill=Y)
# 聊天框
ls = tk.Listbox(root, width=400, yscrollcommand=scrollbar.set)

ls['font'] = "30"
scrollbar['command'] = ls.yview()
ls.Columns = 4
# 摆放位置
ls.pack(side=BOTTOM)
bg.pack(side=TOP)

# 宽不可变, 高可变,默认为True
root.resizable(width=False, height=False)

SockAdressMenu = Menu(root)
sett = Menu(SockAdressMenu, tearoff=0)
sett.add_command(label="连接主机", command=getconnet)
sett.add_command(label="关于作者", command=auther)
sett.add_command(label="版本信息", command=version)
sett.add_command(label="绿漾的秘密 ", command=lvyang)
SockAdressMenu.add_cascade(label="设置", menu=sett)
root['menu'] = SockAdressMenu


# 删除聊天
def delet():
    print("第" + str(ls.curselection()[0]) + "行被删除")
    ls.delete(ls.curselection()[0])


deletemenu = Menu(root, tearoff=0)
deletemenu.add_command(label="删除", command=delet)
deletemenu.add_separator()


def popupmenu(event):
    if len(ls.curselection()) != 0:  # 当选中行不为零时
        deletemenu.post(event.x_root, event.y_root)


# 为ls绑定事件 双击事件 play（废弃）
# ls.bind('<Double-Button-1>',play)
# 为ls绑定右键事件
ls.bind("<Button-3>", popupmenu)

canvas = tk.Canvas(root,
                   width=500,  # 指定Canvas组件的宽度
                   height=700,  # 指定Canvas组件的高度
                   bg='white')  # 指定Canvas组件的背景色
# im = tk.PhotoImage(file=os.getcwd()+"\\img\\bg.png")     # 使用PhotoImage打开图片
image = Image.open(os.getcwd() + "\\img\\bg.png")
im = ImageTk.PhotoImage(image)
image2 = Image.open(os.getcwd() + "\\img\\bg2.png")
im2 = ImageTk.PhotoImage(image2)
canvas.create_image(300, 250, image=im, tag='pic1')  # 使用create_image将图片添加到Canvas组件中
canvas.create_text(100, 77,  # 使用create_text方法在坐标（302，77）处绘制文字
                   text='绿 漾 同 学'  # 所绘制文字的内容
                   , fill=colors[random.randint(0, len(colors) - 1)])  # 所绘制文字的颜色为灰色
canvas.create_text(100, 75,
                   text='绿 漾 同 学',
                   fill=colors[random.randint(0, len(colors) - 1)])

canvas.pack()  # 将Canvas添加到主窗口'''
ls.insert(END, "                        记录美好时刻")
ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])

ls.itemconfig(END, fg=colors[random.randint(0, len(colors) - 1)])
#getversion().start()
# 进入主事件循环
tk.mainloop()
# pyinstaller -F -w -i img\tb.ico VoiceGenie.py