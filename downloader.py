# -*- coding:UTF-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
import time


server='http://www.99lib.net/'
driver=webdriver.PhantomJS(executable_path="phantomjs.exe")
target = 'http://www.99lib.net/book/3489/index.htm'  #小说目录地址

driver.get(target)
menu_html=driver.page_source #获取小说目录的html

dirs_bf=BeautifulSoup(menu_html,"lxml")
dirs=dirs_bf.find_all(id="dir")  #获取html中的章节目录部分

a_bf=BeautifulSoup(str(dirs[0]),"lxml")
a=a_bf.find_all('a')
num=len(a)
print("一共有",num,"个章节需要下载！")

for each in a:
    print("正在下载：",each.string)
    name=each.string+".txt"
    url=server+each.get('href')
    current = webdriver.PhantomJS(executable_path="phantomjs.exe")
    current.get(url)
    for i in range(10):
        current.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
    text = current.find_element_by_id(id_="content")
    out=open(name,"w")
    out.write(text.text)
    current.quit()
    print("........下载完成")

print("全书下载完成！")
driver.quit()
