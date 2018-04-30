'''
注册
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from make_name import *
from phone import *
from login import *


def reg(times):
    excel = Excel()
    zhihu = Zhihu()
    total = 0
    name_list = IO_nametxt()
    phone = Phone()
    while times > 0:
        num  = phone.get_phone()
        driver = webdriver.Chrome()
        driver.get("https://www.zhihu.com/signup")
        elem = driver.find_element_by_name("phoneNo")
        elem.clear()
        elem.send_keys(num) #输入号码
        elem1 = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/div/div/form/div[3]/div[1]/button')
        elem1.click()

        #检测是否可用此手机号
        time.sleep(3)
        if "该手机号已注册" in driver.page_source:
            print("手机号已注册%s" % (num))
            phone.addignore_phone(num)
            excel.update(phone_num=num)
            times -= 1
            excel.save()
            driver.close()
            zhihu.sleep(60)
            continue #直接跳过下面的循环

        if "请输入验证码" in driver.page_source or "请点击图中倒立的文字" in driver.page_source:
            print("出现封IP!休息60秒")
            driver.close()
            phone.release_phone(num)
            times -= 1
            excel.save()
            zhihu.sleep(120)
            continue
        cap = phone.get_message(num=num)#索取验证码
        if cap == False: #如果收不到信息，释放手机号，continue循环
            driver.close()
            print("手机号码：%s 不可使用！" % (num))
            phone.release_phone(num)
            times -= 1
            excel.save()  # 每一次循环都保存一次，防止丢失
            zhihu.sleep(60)
            continue
        elem2 = driver.find_element_by_name("digits")
        elem2.clear()
        elem2.send_keys(cap) #填写验证码
        sub = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/div/div/form/button')
        sub.click() #发送验证码
        driver.implicitly_wait(10) #未测试是否需要等待

        fullname = driver.find_element_by_name("fullname")

        username = random.choice(name_list)
        fullname.send_keys(username) #发送名字

        password = driver.find_element_by_name("password")
        pw = get_pw(10) #随机密码
        password.send_keys(pw) #发送密码
        password.submit()
        zhihu.sleep(3)
        excel.update(phone_num=num,password=pw,username=username)
        #此处未知需不需要等待！
        #进行初次登陆操作
        zhihu.just_get_cookie(driver=driver,num=num)
        driver.close()
        print("已保存！")
        times -= 1
        total += 1
        excel.save() #每一次循环都保存一次，防止丢失

    #关闭excel
    excel.save()
    excel.close() #保存
    print("完成注册！一共注册了%d个账号！" % (total))

if __name__ == '__main__':
    reg(50) #你需要输入需要注册多少个手机号，结果会自动保存在user.xlsx中