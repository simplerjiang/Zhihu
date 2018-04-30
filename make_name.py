#coding:utf-8
'''
将注册后的手机号保存至Excel中，原本是想着不需要安装数据库为最方便方法
但是Excel在处理多线程打开一个文件的时候会出现问题，并且会出现关闭Excel主程序无法的问题，没有解决。
其他封装检查过并没有Bug
'''
from random import choice
import os
import xlwings

def get_pw(num=10): #获取随机密码，通过传入位数。
    a = "1234567890"
    b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(num//2):
        sa.append(choice(b))
        sa.append(choice(a))
    sa = "".join(sa)
    return sa

#由于为了简单些，用excel储存用户名，A列储存“电话号”，B列储存密码，C列储存用户名

def save_excel(phone_num='',password='',username=''): #已测试
    if not os.path.exists(r"cookie/user.xlsx"):
        app = xlwings.App(visible=True,add_book=False)
        wb = xlwings.books.add()
        wb.save(r"cookie/user.xlsx")
        print('新建user.xlsx中...')
    else:
        app = xlwings.App(visible=True,add_book=False)
        app.display_alerts = False
        app.screen_updating=False
        wb = xlwings.Book(r"cookie/user.xlsx")
        print("打开user.xlsx中...")
    sheet = wb.sheets[0]
    print(sheet.range("A1:A2").value)
    wb.save()
    wb.close()
    app.quit()

class Excel(): #使用Excel储存

    first_code = "A"  #用来设置列的长度，first_code 不要改，是存放手机号的列
    last_code = "D"  #如果未来有更多的账号信息就修改这里的长度！

    def __init__(self):
        if not os.path.exists(r"cookie/user.xlsx"):
            self.app = xlwings.App(visible=True, add_book=True)
            self.wb = xlwings.books.add()
            self.wb.save(r"cookie/user.xlsx")
            print('新建user.xlsx中...')
            self.sheet = self.wb.sheets[0]
        else:
            self.app = xlwings.App(visible=True, add_book=False)
            self.app.display_alerts = False
            self.app.screen_updating = False
            self.wb = xlwings.Book(r"cookie/user.xlsx")
            print("打开user.xlsx中...")
            self.sheet = self.wb.sheets[0]

    def close(self): #已测试，就是app窗口好像关不掉
        self.wb.close()
        self.app.quit()

    def save(self): #已测试
        self.wb.save()

    def update(self,phone_num, password = None, username = None): #已测试，如果成功就返回添加的内容，如果失败就返回False
        line = self.line_num() + 1
        if self.sheet.range(self.first_code + str(line)).value == None:
            Plist = [phone_num,password,username]
            self.sheet.range(self.first_code + str(line)).value = Plist
            self.save()
            return Plist
        else:
            raise Exception("Update函数出错")

    def update_by_hand(self,place,values): #已测试
        self.sheet.range(place).value = values
        self.save()

    def output_date_by_hand(self,place): #已测试
        value = self.sheet.range(place).value   ##手机号传出来的时候会编程浮点数，所以要str(int(phone_num))再使用 ，或者直接int()
        return value #返回

    def delete_date_by_hand(self,place): #已测试 可以全部删除也可以只删除一个！
        #测试
        self.sheet.range(place).value = None
        self.save()

    def line_num(self): #已测试
        self.sheet = self.wb.sheets[0]
        i = 1
        while True:
            if self.sheet.range(self.first_code+str(i)).value == None:
                i -= 1
                break
            else:
                i+=1
        return i
    def state_update_by_num(self,num,value):
        num = str(num)
        for i in range(self.line_num()):
            i += 1
            a = self.sheet.range('A' + str(i)).value
            if num == str(int(a)):
                self.sheet.range('D' + str(i)).value = str(value)


    def state_update(self,line,value,code = "D"):
        self.sheet.range(code+str(line)).value = str(value)
        self.save()

    def return_all(self,code = None): #已测试
        all_list = []
        if code == None:
            for i in range(self.line_num()):
                i += 1
                all_list.append(self.output_date_by_hand(self.first_code + str(i) + ":" + self.last_code + str(i)))
        elif code == self.first_code:
            for i in range(self.line_num()):
                i+=1
                all_list.append(str(int(self.output_date_by_hand(self.first_code+str(i)))))
        else:
            for i in range(self.line_num()):
                i+= 1
                all_list.append(self.output_date_by_hand(self.first_code+str(i)))

        return all_list

    def search_by_ABC(self,code = None, value = None):  #已测试
        if code == None or value == None:
            print("函数Search_bby_ABC未输入值！")
            raise Exception("函数Search_bby_ABC未输入值！")
        value = str(value)
        answer = []
        for i in range(self.line_num()):
            i += 1
            a = self.sheet.range(code + str(i)).value
            if code == self.first_code or code == "D":
                a = str(int(a))
            if a == value:
                sp_list = self.sheet.range(self.first_code+str(i)+":"+self.last_code+str(i)).value
                sp_list.append(i)
                answer.append(sp_list)

        return answer #返回一个列表，如果只有一个答案，那么就在answer[0]，如果有多个就可以进行循环 #如果没有值就返回空列表

    def find_available_phone(self):  #已测试
        value = '1'
        answer = []
        for i in range(self.line_num()):
            i += 1
            a = self.sheet.range('D' + str(i)).value
            if a == None:
                continue
            a = str(int(a))
            if a == value:
                phone = self.sheet.range(self.first_code+str(i)).value
                answer.append(str(int(phone)))

        return answer #返回一个列表，如果只有一个答案，那么就在answer[0]，如果有多个就可以进行循环 #如果没有值就返回空列表


    def return_filter(self,phone_num = None, password = None, username = None):
        pass #暂时还没想好，而且目前好像不需要！

    def find_list_num(self,num):
        num = str(num)
        for i in range(self.line_num()):
            i += 1
            a = self.sheet.range('A'+str(i)).value
            if str(int(a)) == num:
                return str(i)

        return "Not Found"


def IO_nametxt(file_name = "name.txt",split = None):
    f = open(file_name,encoding="utf-8")
    if split == None:
        content = f.read().splitlines()
    else:
        content = f.read().split(split)
    answer = []
    for i in range(len(content)):
        a = content[i]
        if a == '':
            continue
        answer.append(content[i])
    return answer #返回一个列表，应该永久储存在程序中，不多次引用。






##test##

"""
if __name__ == '__main__':
    excel = Excel()
    print(excel.search_by_ABC(code= "A",value= "13714692630"))
    excel.save()
    input("等待")
    excel.close()
"""

if __name__ == '__main__':
    excel = Excel()
    print(excel.find_available_phone())