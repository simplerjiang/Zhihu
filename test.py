'''
前期进行试验用的，未维护
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import xlwings
import requests
def reg(ci):
    while ci > 0:
        num = "13714692666"  # 取得手机号
        driver = webdriver.Chrome()
        driver.get("https://www.zhihu.com/signup")
        elem = driver.find_element_by_name("phoneNo")
        elem.clear()
        elem.send_keys(num) #输入号码
        elem1 = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/div/div/form/div[3]/div[1]/button')
        elem1.click()
        time.sleep(1)
        if "该手机号已注册" in driver.page_source:
            print("成功")
        ci -= 1

def excel():
    wb = xlwings.Book("test.xlsx")
    sheet = wb.sheets[0]
    sheet.range('A1').value = ["a","b","c","d"]
    print(sheet.range("A1").value)

def test():
    url = "http://www.qichacha.com/firm_17b333550d46b4a8fdd2d7fe460b2b52.html"
    headers = {'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    request = requests.get(url,headers=headers)
    print(request)
    print(request.text)

if __name__ == '__main__':
    test()