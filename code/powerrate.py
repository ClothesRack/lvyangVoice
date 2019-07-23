import requests
import re
session = requests.session()
#num = input("输入寝室：")
list= []
a = 440101
'''while True:
    if a % 100 > 25:
        a += 76;
    if (a / 100) % 100 >= 12:
        a += 10000 - 1101;
    if a >= 490000:
        break;
    num = str(a)
    a += 1'''
def powerrate(stnum):
    room = {
        "room":stnum,
        "button":"查  询"
    }
    resp = session.post("http://www.xinhangxm.cn/power/index.php?c=main&a=show", data=room)
    m_tr = re.findall(r"<h1>(.*?)<\/h1>", resp.text, re.I | re.S | re.M)
    print("寝室:"+stnum+",剩余电费："+m_tr[1])

    if not m_tr[1] == "网络错误!":
        if stnum[2]=='0':
            return "寝室"+stnum[0:2]+"栋"+stnum[3:]+"还剩余电费："+m_tr[1]+"元"
        else:
            return "寝室:"+stnum[0:2]+"栋"+stnum[2:]+"还剩余电费："+m_tr[1]+"元"
    else:
        return "目前服务器网络错误，稍后一下再试吧。"
#list.append("寝室:%s,剩余电费：%s".format(num,m_tr[1]))

'''file = open("d:\\电费情况.txt",'a', encoding='utf-8')
for i in list :
    file.write(i)
file.close()'''
