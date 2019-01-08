# TED-crawl
获取TED url&amp;定时发送邮件

### 获取TED url
``` python
from lxml import etree

url = 'https://www.ted.com/talks'
    html = get_index(url)
    soup = BeautifulSoup(html, 'lxml')
    html = str(soup.find("div", class_="row row-sm-4up row-lg-6up row-skinny"))
    html = etree.HTML(html)
    
    html_data = html.xpath('//div[@class="col"]/div[@class="m3"]/div[@class="talk-link"]'
                           '/div[@class="media media--sm-v"]/div[@class="media__image media__image--thumb talk-link__image"]'
                           '/a/@href')
    # html_data是list类型
    return html_data
```
> etree 提供了HTML这个解析函数，然后可以直接对HTML使用xpath

> xpath 基本语法：
> * XPATH基本上是用一种类似目录树的方法来描述在XML文档中的路径。比如用 `/ ` 来作为上下层级间的分隔
> * `..` 和 `.` 分别被用来表示父节点和本节点
> * 为了缩小定位范围，往往还需要增加过滤条件。过滤的方法就是用 `[]` 把过滤条件加上。比如在HTML文档里使用 `/html/body/div[@id='main']` ，即可取出body里id为main的div节点
> * 其中 `@id` 表示属性id，类似的还可以使用如 `@name`, `@value`, `@href`, `@src`, `@class`...

### 将url保存在docker的mysql容器中
##### 建数据库和表
##### 连接数据库，并判断数据是否存在
##### 保存至数据库
### 发送邮件
### 生成并安装requirements.txt
* pip install pipreqs
> 可以通过对项目目录的扫描，自动发现使用了那些类库，自动生成依赖清单，但可能会有些偏差，需要检查并调整
* cat requirements.txt
> 查看文件内容
* pip install -r requirements.txt
> 安装requirements.txt依赖

### 部署服务器
* 生成证书`xxx.pem`
* 连接服务器
```
ssh -i "xxx.pem" ubuntu@xxxx
```
> @前面是远程用户名，@后面是远程IP

* 将本地修改的文件拷贝到远程
###### 执行下面语句需要和`xxx.pem`在 同一级目录下
本地执行
```
$ scp -i xxx.pem TED.py ubuntu@xxxx:/home/ubuntu
```
> * 格式：scp -i *.pem 本地文件路径  remote_username@remote_ip:remote_folder 
> * `-i` (identity_file) 表示 从指定文件中读取传输时使用的密钥文件，此参数直接传递给ssh 

* 查看服务器中docker正在运行的容器
```
$ sudo docker ps 
```

* 进入选定容器
```
$ sudo docker exec -it mypython bash
```
> `ctrl + D` 退出

* 将拷贝到远程的文件放到新建的文件夹中
* 配置定时任务

执行
```
crontab -e
```
添加
```
00 04 * * * nohup python /home/TED.py >> /home/logs.log 2>&1 &
```
> * 使用crontab指令来管理cron机制 (让系统在指定的时间，去执行某个指定的工作)
> * `-l` 可以列出crontab的内容
> * `-e` 可以使用系统预设的编辑器，开启crontab
> * crontab时间格式说明:
>    * minute(分)可以设置0-59分
>    * hour（小时）可以设置0-23小时
>    * day of month（日期）可以设置1-31号
>    * month（月份）：可以设置1-12月
>    * day of week（星期）：可以设置0-7星期几，其中0和7都代表星期天，或者也可以使用名称来表示星期天到星期一，例如sun表示星期天，mon表示星期一等等

> * crontab范例
>    * 每五分钟执行   `*/5 * * * *`
>    * 每小时执行     `0 * * * *`
>    * 每天执行       `0 0 * * *`
>    * 每周执行       `0 0 * * 0`
>    * 每月执行       `0 0 1 * *`
>    * 每年执行       `0 0 1 1 *`
