# txt_downloader
Python爬虫个人练习代码，克服网站自带的反爬虫机制，从在线阅读网站下载小说保存为txt格式


# 实验环境

Python ：3.5.3

selenium ：3.7.0

chrome ：60.0.3112.90

phantomjs ：2.1.1



# 坑点：在线阅读网不是直接爬html就可以的

参考教程如下：

http://www.cuijiahua.com/blog/2017/10/spider_tutorial_1.html

原文中的例子：

```python
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
if __name__ == "__main__":
     target = 'http://www.biqukan.com/1_1094/5403177.html'
     req = requests.get(url = target)
     html = req.text
     bf = BeautifulSoup(html)yixie
     texts = bf.find_all('div', class_ = 'showtxt') 
     print(texts)
```

爬到的内容：

```html
[<div id="content"><h2 class="h2">第一章 闸桥底下的水怪</h2><div>村民们为了求条活路，只好盖起一座庙祭拜旱魔大仙，还被迫准备了童男童女活祭，童男童女是抓阄选出来的，赶上哪家的孩子哪家便认倒霉，村里有个常年吃斋年佛的老太太，她孙女不幸被选中去做活祭，老太太舍不得这小孙女，但也无可奈何，一个人在屋里拜佛求神，哭得眼都快瞎了，夜里忽然做了个梦.......
```



后来仔细一看，不对啊，开头怎么不是熟悉的“九河下梢天津卫，两道浮桥三道关”呢！

然后用谷歌浏览器查看了之后才发现，查看到的内容和之前直接爬的源代码内容根本就不一样啊。

估计是这些在线阅读网站的防复制机制，它的Elements当中的文章段落也是乱序的，有很多的冗余段落，是按照从当前开始，向下数的第6个段落才是真正的下一段。

```html
0：<div>当前段落</div>
1：<div>假的！</div>
2：<div>假的！</div>
3：<div>假的！</div>
4：<div>假的！</div>
5：<div>假的！</div>
6：<div>真正的下一个段落</div>
```



# 转向selenium

于是就开始查找如何爬到Elements

先安装selenium，pip安装即可。一开始我选择的是Chrome浏览器，即webdriver.Chrome

## selenium+Chrome

#### 下载chromedriver

要对应自己的chrome浏览器，可以在网上找到对应规则

http://chromedriver.storage.googleapis.com/index.html?path=2.33/ 



使用时这里要注意地址是chromedriver.exe的，不是chrome.exe!

http://bbs.csdn.net/topics/391982455 

```
browser=webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
```



#### 目前的代码

```python
# -*- coding:UTF-8 -*-
from selenium import webdriver

browser=webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
target = 'http://www.99lib.net/book/3489/118172.htm'
browser.get(target)
text=browser.find_element_by_id(id_="content")
print(text.text)

browser.quit()
```

然而，虽然这下子的结果是正确的了，但是却不全。

```
D:\home_for_python\python.exe D:/workspace/test.py

第一章 闸桥底下的水怪

九河下梢天津卫，两道浮桥三道关；

南门外叫海光寺，北门外是北大关；

南门里是教军场，鼓楼炮台造中间；

三个垛子四尊炮，黄牌电车去海关。

这个顺口溜，是说旧时天津城的风物，民国那时候，南有上海滩，北有天津卫，乃是最繁华的所在。河神的故事，大部分发生在天津，首先得跟您讲明了，我可不敢保证全都是真人真事，毕竟年代久远，耳闻口传罢了，我一说您一听，信则有不信则无，不必深究。

上岁数的人们，提到天津经常说是“天津卫”，天津卫的卫当什么讲？明朝那时候燕王扫北，明成祖朱棣在天津设卫，跟当时的孝陵卫锦衣卫一样，属于军事单位，是驻兵的地方，大明皇帝把从安徽老家带过来的子弟兵驻防于天津，负责拱卫京师，所以管这地方叫天津卫，到了清朝末年，天津已是九国租借，城市空前繁荣，三教九流聚集，鱼龙混杂，奇闻轶事层出不穷。


Process finished with exit code 0
```



后来查看了body内容 发现也是这么少，但是出现了“继续加载”这样的字样，想到了浏览器是在向下滚的过程中加载更多的文字的，即网页其实是动态的。



## selenium+phantomjs

下面要解决的问题就是，如何模拟出鼠标的滚动效果，使得爬到的内容是完整的。接着在网上找办法，看到有人说phantojs非常好用，于是就改变了策略。

#### phantomjs官网

http://phantomjs.org/download.html

但是官网下载速度很慢，可以去一些软件之家之类的网站下载，速度比它快太多了。



安装好后，模拟出鼠标滚轮的效果：

browser.execute_script("window.scrollTo(0,document.body.scrollHeight)") 

可以使爬到的数据变多，但还不是全部的，不过通过多次滚动后可以得到全部的内容



#### 目前的代码

```python
# -*- coding:UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #引入ActionChains鼠标操作类
import time

driver=webdriver.PhantomJS(executable_path="phantomjs.exe")
target = 'http://www.99lib.net/book/3489/118172.htm'""
driver.get(target)
for i in range(10):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
text=driver.find_element_by_id(id_="content")
#out=open("heshen.txt","w")
#out.write(text.text)
driver.quit()
```

这下就可以获取到单独一章的完整内容啦。



# 批量下载

小说的首页是：http://www.99lib.net/book/3489/index.htm

可以在这里获取到全书的链接，不过这里需要点击才能查看全部章节，可以用click()实现。

不过后来我发现直接获取网页的html也挺方便的。



可以看出目录的**id="dir"**，我们就可以通过这个来找到目录地址的表了：

```html
<dl id="dir"><dd><a href="/book/3489/118172.htm">第一章 闸桥底下的水怪</a></dd><dd><a href="/book/3489/118173.htm">第二章 魏家坟镜子阵</a></dd><dd><a ...</a></dd></dl>
```

经过整理之后得到各个章节的地址，当前代码为：

```python
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

for each in a:
    print(each.string,server+each.get('href'))
driver.quit()
```

得到的结果：

第一章 闸桥底下的水怪 http://www.99lib.net//book/3489/118172.htm
第二章 魏家坟镜子阵 http://www.99lib.net//book/3489/118173.htm
...



这下就离成功不远啦，只要把之前下载单个目录的方法重复就好了。



# 最终代码

```python
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
```



第一次写爬虫没啥经验，没有使用多线程之类的提高效率，每个章节大概是20KB，最后下载完成整本书大概要3分钟。
