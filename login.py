'''
登陆类
已经进行了单独封装
'''

from make_name import *
from selenium import webdriver
import time
from dump import *
import random
import os
from phone import *
import re

class Zhihu():
    def __init__(self,phone_num = None):
        if phone_num == None:
            pass
            #raise Exception("Zhihu()函数初始化错误！,缺少属性phone_num")


        #初始化Excel()
        self.excel = Excel()
        self.phone = Phone(d)

    def sleep(self,second): #睡眠并打印倒数
        print("进入休息,%d秒" % second)
        if second <= 3:
            time.sleep(3)
            return 0
        for i in range(second):
            print(second-i)
            time.sleep(1)

    def cap_again(self,driver,num):
        num = str(num)
        self.sleep(3)
        if "我们检测到您此次登录异常，请将 App 升级至新版本，按照提示进行安全验证。" in driver.page_source or '反作弊' in driver.page_source:
            """
            elem_input = driver.find_element_by_xpath('/html/body/div[4]/div/span/div/div[2]/div/div/div/div[3]/div/input')
            cap_but = driver.find_element_by_xpath('/html/body/div[4]/div/span/div/div[2]/div/div/div/div[3]/button')
            cap_but.click()
            elem_input.send_keys(self.phone.cap_match(self.phone.get_message(num)))
            driver.find_element_by_xpath('/html/body/div[4]/div/span/div/div[2]/div/div/div/div[5]/button').click()
            #由于没办法重新获取一个新的，所以每次用完出现异常问题只能释放
            """
            self.excel.state_update_by_num(num, value='0')
            print("%s号码不可用！" % (num))
            return False
        else:
            return True


    def guanzhu(self,driver,url):
        driver.get(url)
        self.sleep(3)
        if '已关注' in driver.page_source:
            return driver
        guanzhu_but = driver.find_element_by_xpath('//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[2]/div/button[1]')
        guanzhu_but.click()
        return driver







    def first_login(self,driver): #传入driver对象 此方法用于检测是否是第一次,只能传入已经登陆的账号。
        if "简单介绍自己，会为你挑选你可能感兴趣的话题" in driver.page_source:
            job_input_elem = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/div/div[2]/div[1]/div/input')
            job_input_elem.clear()
            job_input_elem.send_keys(random.choice(IO_nametxt(file_name="job.txt",split= ' ')))
            job_subit = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/div/div[2]/div[1]/button')
            job_subit.click()
            self.sleep(1)
        self.sleep(1)
        if '我们将根据你关注的话题定制首页推荐内容' in driver.page_source:
            driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[2]/div/div[2]/button').click()
        return driver

    def load_cookie(self,driver,num): #此方法用于加载cookie，并返回driver
        driver.get("https://www.zhihu.com")
        num = str(num)
        if os.path.exists(os.path.join(os.path.join(os.getcwd(),'cookie',str(num)+'.json'))):
            cookie = json_load(num)
            driver.delete_all_cookies()
            for i in cookie:
                driver.add_cookie(i)
            driver.get("https://www.zhihu.com")
            self.sleep(2)
            if '手机验证码登录' in driver.page_source or '注册即代表你同意' in driver.page_source:
                print('登陆失效！重新登陆！')
                cookie = self.login_check_state_and_get_cookie(num=num,first=True,driver=driver)
                if type(cookie) == int:
                    print("号码%s出现异常！请查看%s" % (num,cookie))
                    return False
                else:
                    print("已保存，路径为：" + json_dump(data=cookie, name=num))
                    driver = webdriver.Chrome()
                    self.load_cookie(driver=driver,num=num) #如果这里能正常，就能回到主页！
            if self.cap_again(driver=driver, num=num):
                return False
            return driver #如果这里执行正常就能回到主页
        else:
            return False #返回false代表失败，没有此手机号的cookie。

    def set_headimg(self,driver):
        driver.get('https://www.zhihu.com/people/edit')
        self.sleep(3)
        head_elem = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div[2]/div[1]/div/input')
        head_elem.send_keys(os.path.join(os.getcwd(),'img',random.choice(json_load('img'))))
        self.sleep(3)
        driver.find_element_by_xpath('/html/body/div[3]/div/span/div/div[2]/div/div[2]/div/div[3]/button').click()
        self.sleep(15)



    def login_check_state_and_get_cookie(self,num,first = False,driver = None): #返回1代表没有找到值，返回2代表账号已经确定不可用。
        num = str(num)
        date = self.excel.search_by_ABC(code="A",value=num)
        if len(date) == 0:
            return 1 #返回一代表找不到这个账号。
        else:
            password = date[0][1]
            username = date[0][2]
            if date[0][3] == None:
                state = '-1' #负1代表未检测
            else:
                state = str(int(date[0][3]))
            list_num = date[0][-1] #列表号码，取列表最后一个数
            if state == '0':
                return 2 #返回二代表这个账号已经被确认过无法登陆！
            if state == '1' and first == False:
                return 1 #返回一代表已经检测过了，可以用！
            else:
                if driver == None:
                    driver = webdriver.Chrome()
                driver.get("https://www.zhihu.com/signin")
                if "手机验证码登录" not in driver.page_source:
                    raise Exception("手机号%s出现异常！" % (num))

                username_elem = driver.find_element_by_name("username")
                username_elem.clear()
                username_elem.send_keys(num)

                password_elem = driver.find_element_by_name("password")
                password_elem.clear()
                password_elem.send_keys(password)

                password_elem.submit()
                self.sleep(3)
                for i in range(3):
                    if "请输入验证码" in driver.page_source or "请点击图中倒立的文字" in driver.page_source:
                        print("出现封IP!休息60秒")
                        driver.close()
                        self.sleep(60)
                        driver = webdriver.Chrome()
                        driver.get("https://www.zhihu.com/signin")

                        username_elem = driver.find_element_by_name("username")
                        username_elem.clear()
                        username_elem.send_keys(num)

                        password_elem = driver.find_element_by_name("password")
                        password_elem.clear()
                        password_elem.send_keys(password)

                        password_elem.submit()
                        self.sleep(3)
                        if "该手机号尚未注册知乎" in driver.page_source:
                            self.excel.state_update(list_num, value=0)
                            print("手机号失败！")
                            driver.close()
                            return 4  # 返回4代表此手机无法使用，并已经设定state！

                if "该手机号尚未注册知乎" in driver.page_source:
                    self.excel.state_update(list_num,value=0)
                    driver.close()
                    print("手机号失败！")
                    return 4 #返回4代表此手机无法使用，并已经设定state！
                cookie = driver.get_cookies()
                self.sleep(3)
                self.first_login(driver=driver)
                self.sleep(3)
                if self.cap_again(driver=driver,num=num) == False:
                    driver.close()
                    json_delete(num)
                    return 2
                if list_num == '-1':
                    self.set_headimg(driver=driver)
                driver.close()
                self.excel.state_update(list_num,value=1)
                return cookie

    def check_all_and_save_all(self,first = False):
        all_phone = self.excel.return_all(code='A')
        times = 0
        for i in all_phone:
            cookie = self.login_check_state_and_get_cookie(num=i,first = first)
            if cookie == 4:
                print("手机号无法登陆，休息60秒！")
                self.sleep(60)
            if cookie == 1:
                print("号码%s已经检测过，可以使用！如需要全部检测请在函数中输入first = True" % (i))
            elif type(cookie) == int:
                print("号码%s出现异常！返回值为%s，请查看！" % (i,cookie))
            else:
                print("已保存，路径为："+json_dump(data = cookie,name = i))
                times += 1
                self.sleep(30)

        print("检查完毕！并保存了%d个账号！" % (times))





    def every_zan(self,driver,url): #逐页点赞，必须传入一个登陆后得driver，以及一个用户主页的url,例如'https://www.zhihu.com/people/kong-41-52/'
        driver.get(url+'answers')
        zan_time = 0
        sleep_times = 0
        while True:
            a.sleep(5)
            elem_list = driver.find_elements_by_class_name('VoteButton--up')
            for i in elem_list:
                if zan_time > 27:
                    break
                if sleep_times >= 10:  # 每过10个赞休息30秒
                    sleep_times = 0
                    a.sleep(60)

                if 'is-active' in i.get_attribute('class'):
                    continue
                elif i.is_enabled():
                    a.sleep(3)
                    i.click()  # 每过10个赞休息30秒
                    zan_time += 1
                    sleep_times += 1
            try:
                driver.find_element_by_class_name('PaginationButton-next').click()
            except:
                break
        #最后返回driver
        self.sleep(360)
        return driver


    def super_zan(self,times,url):
        all_list = self.excel.search_by_ABC(code='D',value='1')
        list_len = len(all_list)
        if list_len == 0:
            raise Exception("已经没有可用账号！")
        for i in range(len(all_list)):
            bot_info = random.choice(all_list)
            all_list.remove(bot_info) #这里是随机选择账号，并在队列中去掉这个账号，防止一个账号反复点赞！
            bot_num = bot_info[0]
            bot_list_num = bot_info[-1]
            bot_pw = bot_info[1]
            driver = webdriver.Chrome()
            driver = self.load_cookie(num=bot_num,driver=driver) #加载它的cookie，返回的driver就是已经登陆好的了
            driver = self.first_login(driver=driver) #进行第一次进入检查
            if self.cap_again(driver=driver) == False: #如果不可用就执行删除
                driver.close()
                json_delete(num=bot_num)
                continue
            zan_time = 0

            #以下时进行关注！

            #以下是逐页点赞
            self.every_zan(driver=driver,url=url)
            #收集点赞次数，
            all_zan_time = self.zan_ci(driver=driver, url=url)





    def just_get_cookie(self,num,driver = None): #输入一个已经登陆进入的driver,获取cookie并检查账号是否可用
        num = str(num)
        cookie = driver.get_cookies()
        self.sleep(3)
        list_num = self.excel.find_list_num(num=num)
        self.first_login(driver=driver)
        self.sleep(3)
        if self.cap_again(driver=driver,num=num) == False:
            self.excel.state_update_by_num(num=num,value='0')
            json_delete(num)
            return False
        self.set_headimg(driver=driver)
        print("已保存，路径为：" + json_dump(data=cookie, name=num))
        self.excel.state_update_by_num(num=num, value='1')
        return True

    def deal_person(self,url,times = None):
        all_phone_list = self.excel.find_available_phone()
        all_phone_list = list(reversed(all_phone_list))
        all_zan = 0
        used_phone = 0
        for i in all_phone_list:
            phone_num = random.choice(all_phone_list)
            all_phone_list.remove(phone_num)
            if times != None:
                if all_zan > times:
                    break
            driver = webdriver.Chrome()
            driver.maximize_window()
            self.load_cookie(num=phone_num,driver=driver)
            self.guanzhu(driver=driver,url=url)
            self.every_zan(driver=driver,url=url)
            used_phone += 1
            driver.close()
        print("完成赞数：%s次",all_zan)
        print("完成关注号:%s个",used_phone)


    def answer_zan(self,url,times=None):
        all_phone_list = self.excel.find_available_phone()
        all_phone_list = list(reversed(all_phone_list))
        all_zan = 0
        used_phone = 0
        for a in all_phone_list:
            phone_num = random.choice(all_phone_list)
            all_phone_list.remove(phone_num)
            if times != None:
                if all_zan > times:
                    break

            driver = webdriver.Chrome()
            self.load_cookie(driver=driver,num=phone_num)
            for i in url:
                all_zan += self.answer_zan_one(driver=driver,url=i)
            driver.close()
        print("一共赞了%d个赞" % (all_zan))

    def answer_zan_one(self,driver,url):
        driver.get(url=url)
        elem_list = driver.find_elements_by_class_name('VoteButton--up')
        elem_my = elem_list[0]
        if 'is-active' not in elem_my.get_attribute('class'):
            elem_my.click()
            return 1
        return 0
if __name__ == '__main__':
    a = Zhihu()
    a.deal_person(url="https://www.zhihu.com/people/kong-63-62/")


    input("wait:")