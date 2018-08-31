# heibanke
spider challenge

## 项目初衷
晚上刷知乎的时候发现有一个爬虫挑战的网站[黑板客](http://www.heibanke.com/)，刚好最近一直想找一些项目练手，
感觉比较有意思，因此花了一天多时间来完成这个挑战。本次挑战还有许多可以改进的地方，比如使用多线程来提高速度，
训练自己的字库来提高验证码识别准确度。

## 需要安装的第三方库
<br> pip install requests </br>
<br> pip install beautifulsoup4 </br>
<br> pip install lxml </br>
<br> pip install tesserocr </br>
<br> 其中tesserocr库只是对tesseract做的一层python API封装，因此安装tesserocr库之前，需要先安装tesseract，
tesseract下载地址：https://digi.bib.uni-mannheim.de/tesseract/ </br>

## challenge 1
<br> [第一关](http://www.heibanke.com/lesson/crawler_ex00/)挑战比较简单，只需要提取网页中的关键内容作为下一个url的一部分即可，主要考察对正则表达式的应用 </br>
<br> </br>
![result1](https:)

## challenge 2
<br> [第二关](http://www.heibanke.com/lesson/crawler_ex01/)挑战同样比较简单，需要模拟登录，分析post提交的表单，需要三个信息，分别为token, username, password;
首先我们需要提取网页中隐含的token，用户名可以随便输入，但是密码不确定，提示为30以内的数字，那我们可以写一个for循环一个个去试，
若是网页中出现我们所需要的关键字则表示登录成功，然后将登录成功后的提示提取出来并打印 </br>
<br> </br>
![result2](https:)

## challenge 3
<br> [第三关](http://www.heibanke.com/lesson/crawler_ex02/)开始有点难度了，需要先在该网站注册一个账号，登录成功之后维持此对话，然后重复第二关的工作，寻找密码。此挑战考察了会话的维持，
因此我们新建一个Login类，然后使用session来维持会话，最终成功找到结果 </br>
<br> </br>
![result3](https:)

## challenge 4
<br> [第四关](http://www.heibanke.com/lesson/crawler_ex03/)实现起来很简单，但是优化起来比较难。首先使用自己注册的账号登录成功，然后维持此对话，在接下来的提示中寻找有用信息，解析出密码，
此处需要对数据比较敏感；提示信息有十三页，每页都有几组pos对应的value,通过观察发现，pos为100以内的数字，并且无规律分布，很自然的想到密码为
从1-100对应的val；可是发现爬完这十三页的pos值不够100，只能加一个死循环，让他一直重复，直至将1-100对应的值全都得到 </br>
<br> 爬取过程中发现速度特别慢，因此想用多线程来解决这个问题，因此开了十三个线程同时开始，但是发现有11个线程总是获取不到数据，查了很多资料也没找到原因，
因此最终只开了两个线程，这个问题等我日后水平提高了再来优化 </br>
<br> </br>
![result4](https:)

## challenge 5
<br> [第五关](http://www.heibanke.com/lesson/crawler_ex04/)在测试密码的时候设置了验证码，因此我引入了tesserocr库和PIL库,但是验证码识别的准确率还是特别低，不到10%，因此耗费的时间也比较长；这个问题
可以通过训练字库来解决，需要用到一些机器学习的知识，和我将来想要研究的方向相同 </br>
<br> </br>
![result5](https:)
