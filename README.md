#   千鸟云 - 服务器端

##  每个app的作用
1. app_user 用户信息
1. app_message 用来存放消息，包括系统消息，用户消息
1. app_movie 爬虫搜索到的电影资源数据，和豆瓣上面的电影数据
1. app_spider 其他的爬虫

##  服务器部署时的一些指令

###### 1.  部署-激活环境

    source /root/python_env/python3/bin/activate

###### 2.  退出环境

    deactivate

###### 3.  uwsgi 应用配置

    uwsgi.ini

###### 4.  启动应用 - 需要在虚拟环境下 - 需要运行权限

    chmod +x start_server
    ./start_server

###### 5.  初次用 uwsgi 时，请先安装

    pip install uwsgi

###### 6.  强制更新远程端

    git fetch --all
    git reset --hard origin/master

###### 7.  定时任务

    python manage.py crontab add
    将任务添加并生效

    显示当前的定时任务
    python manage.py crontab show

    删除所有定时任务
    python manage.py crontab remove

    重启django服务。
    执行
    corntab -e

--------------------------------------------------------------


##  开发时常用指令
######1.  更新数据表 并 生成数据库
    python manage.py makemigrations & python manage.py migrate
######2.
    python manage.py migrate
######3.  创建管理员
    python manage.py createsuperuser
######4.  启动
    python manage.py runserver
######5.  新建app：
    python manage.py startapp app_app
######5.  移除app：
    python manage.py migrate your_app_name zero
######6.  生成 requirements.txt
    pip freeze >requirements.txt
######7.  使用 requirements.txt
    pip install -r requirements.txt
######8.  本地开发环境激活（Visoon）
    D:\workspace\python\python_ve\plover.cloud.ve\Scripts\activate.bat
    
######9. 收集静态数据
    python manage.py collectstatic
    
    
######10. 重启影梭
    #!/bin/sh
    ssserver -c /etc/shadowsocks.json -d restart
    supervisorctl restart kcptun
    service supervisord restart
    
    wget --no-check-certificate https://github.com/kuoruan/shell-scripts/raw/master/kcptun/kcptun.sh
    chmod +x ./kcptun.sh
    ./kcptun.sh
    
###### 反向代理
    sudo a2enmod proxy proxy_balancer proxy_http
    
    <VirtualHost *:80>
        #自定义域名
        ServerName example.com
        #off表示开启反向代理，on表示开启正向代理
        ProxyRequests Off
        #反代理要解析的ip 支持添加端口 
        ProxyPass / http://172.16.168.35:7001/
        ProxyPassReverse / http://172.16.168.35:7001/
    </VirtualHost>


###### mysql
    备份数据：mysqldump -u root -p plover_cloud > plover_cloud_20171109.sql

###### mysql

    自用的whl，有些在windows下面很难找