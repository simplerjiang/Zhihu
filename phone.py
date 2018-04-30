'''
这里是用收码平台的API,我用的是http://www.51ym.me 的API
如果需要使用，请自行更改
'''

import requests
import time
import re
class Phone():


    def __init__(self):
        self.TOKEN = "TOKEN"
        self.itemid = "itemid"


    def make_list(self,b):
        a = []
        text = str(b.content,encoding='utf-8')
        if "|" in text:
            a = text.split('|')
            return a
        else:
            return text

    def user_info(self):
        params = {"action":"getaccountinfo","token":self.TOKEN}
        back = requests.get("http://api.fxhyd.cn/UserInterface.aspx",params=params)

        return self.make_list(back)

    def get_phone(self):
        params = {"action":"getmobile","token":self.TOKEN,"itemid":self.itemid}
        back = requests.get("http://api.fxhyd.cn/UserInterface.aspx",params=params)
        list = self.make_list(back)
        if list[0] == 'success':
            return list[1]
        else:
            raise Exception("get_phone方法出现错误，错误码：%s" % (str(back.content,encoding='utf-8')))

    def cap_match(self,string):
        after_match = re.findall("[0-9]{6}",string)
        return after_match[0]


    def get_message(self,num):
        params = {"action":"getsms","token":self.TOKEN,"itemid":self.itemid,"mobile":num,"release":"1"}
        for i in range(12):
            back = requests.get("http://api.fxhyd.cn/UserInterface.aspx",params=params)
            string = str(back.content,encoding='utf-8')
            if "3001" in string:
                time.sleep(5)
                print("等待验证码中...")
                continue
            elif "success" in string:
                list_already = self.make_list(back)
                print("验证码已返回！")
                return str(self.cap_match(list_already[1]))
            else:
                raise Exception("get_message方法出现错误，错误代码：%s" % (string))

        return False



    def release_phone(self,num):
        params = {"action":"release","token":self.TOKEN,"itemid":self.itemid,"mobile":num}
        back = requests.get("http://api.fxhyd.cn/UserInterface.aspx",params=params)
        return str(back.content,encoding='utf-8')

    def addignore_phone(self,num):
        params = {"action":"addignore","token":self.TOKEN,"itemid":self.itemid,"mobile":num}
        back = requests.get("http://api.fxhyd.cn/UserInterface.aspx",params=params)
        string = str(back.content,encoding='utf-8')
        if 'success' in string:
            print("拉黑成功！手机号：%s" % (num))

        else:
            raise Exception("addignore_phone方法出现错误，错误代码：%s" % (string))


if __name__ == '__main__':
    TOKEN = "00481029174fb90d91aa7e055d5a3e5f7afe41f8"
    itemid = "891"
    a = Phone(TOKEN,itemid)
    num = a.get_phone()
    print(num)
    input("等待：")
    print(a.get_message(num=num))