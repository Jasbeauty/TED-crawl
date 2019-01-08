#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2018/9/4 4:37 PM
# @Author: jasmine sun
# @File  : TED.py
import json
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import pymysql as pymysql
from lxml import etree

import requests
from bs4 import BeautifulSoup
from requests import RequestException


def get_index(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    try:
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None





def get_urls():
    url = 'https://www.ted.com/talks'
    html = get_index(url)
    soup = BeautifulSoup(html, 'lxml')
    html = str(soup.find("div", class_="row row-sm-4up row-lg-6up row-skinny"))
    html = etree.HTML(html)
    # result = etree.tostring(html).decode('utf-8')

    # print(result.decode('utf-8'))
    html_data = html.xpath('//div[@class="col"]/div[@class="m3"]/div[@class="talk-link"]'
                           '/div[@class="media media--sm-v"]/div[@class="media__image media__image--thumb talk-link__image"]'
                           '/a/@href')

    # print(type(html_data))   # list类型
    # print(len(html_data))
    # print(html_data)

    for i in html_data:
        # 判断数据是否在文件里面
        # 如果在：跳出循环
        # 不在：将连接存入list, 保存，
        print(i)
        # save_to_local(i)
    return html_data


def save_to_mysql():
    data_list = get_urls()
    # 连接数据库
    # 每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
    # data_count = int(sqlCommand.get_LastId()) + 1
    send_to_email_list = []
    for url in data_list:
        # 把爬取到的每条链接组合成一个字典用于数据库数据的插入
        # urls_dict = {
        #     "id": str(data_count),
        #     "url": url
        # }

        # 插入数据，如果已经存在就不在重复插入
        result = MysqlCommand.insert_Data(url)
        if result is False:
            break
        elif result is True:
            send_to_email_list.append(url)
    if len(send_to_email_list) > 0:
        send_to_email(send_to_email_list=send_to_email_list)


def send_to_email(send_to_email_list, receiver="xxx@qq.com"):
    EMAIL_OAUTH = {
        # 发件人
        'sender': 'xxx@163.com',
        # 所使用的用来发送邮件的SMTP服务器
        'smtpServer': 'smtp.163.com',
        # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
        'username': 'xxx',
        'password': 'xxx'
    }
    mail_config = EMAIL_OAUTH
    sender = mail_config.get('sender')

    # 所使用的用来发送邮件的SMTP服务器
    smtp_server = mail_config.get('smtpServer')

    # 发送邮箱的用户名和授权码（不是登录邮箱的密码）
    username = mail_config.get('username')
    password = mail_config.get('password')

    mail_title = 'TED Link'
    mail_body = '''
    <h3>The Latest Links：</h3>
    '''
    for url in send_to_email_list:
        mail_body += '''<a href="https://www.ted.com/{}">https://www.ted.com/{}</a> <br>'''.format(url, url)

    # 创建一个实例
    message = MIMEText(mail_body, 'html', 'utf-8')  # 邮件正文
    message['From'] = sender  # 邮件上显示的发件人
    message['To'] = receiver  # 邮件上显示的收件人
    message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题
    try:
        smtp = smtplib.SMTP()  # 创建一个连接
        smtp.connect(smtp_server)  # 连接发送邮件的服务器
        smtp.login(username, password)  # 登录服务器
        smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
        smtp.quit()
    except smtplib.SMTPException as e:
        print("send email error: {}".format(e))


class MysqlCommand(object):
    # 类的初始化
    host = "localhost"
    port = 3306
    user = "root"
    password = "xxx"
    db = "ted"
    table = "ted"

    # 插入数据，插入之前先查询是否存在，如果存在就不再插入
    @staticmethod
    def insert_Data(url):
        conn = pymysql.connect(host=MysqlCommand.host, port=MysqlCommand.port, user=MysqlCommand.user,
                               password=MysqlCommand.password,
                               db=MysqlCommand.db, charset="utf8")
        cursor = conn.cursor()
        # 这里查询的sql语句url = ' %s '中 % s的前后要有空格
        sqlExit = "select url from ted where url='%s'" % (url)

        # result为查询到的数据条数如果大于0就代表数据已经存在
        result = cursor.execute(sqlExit)
        if result:
            print("The data has been existed", result)
            return False

        # 数据不存在, 执行下面的插入操作
        try:

            sql = "insert into ted (url) values ('%s')" % (url)
            try:
                result = cursor.execute(sql)
                # insert_id = self.conn.insert_id()
                conn.commit()
                # 判断是否执行成功
                if result:
                    # print("插入成功", insert_id)
                    return True
            except pymysql.Error as e:
                # 发生错误时回滚
                conn.rollback()
                # 主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    print("The data has been existed, no data will be inserted")
                else:
                    print("data inserted failed, Causes: %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("database error, Causes: %d: %s" % (e.args[0], e.args[1]))
        cursor.close()
        conn.close()


if __name__ == '__main__':
    save_to_mysql()
