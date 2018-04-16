from fabric.api import *

"""
Plover自动化运维脚本
"""

env.user = 'root'
env.password = 'Chenshun1991'
env.hosts = ['101.200.36.42']  # 如果有多个主机，fabric会自动依次部署
#
env.command_timeout = 10  # 10秒超时
env.current_ip = 0  # 当前执行到的ip

"""
fab -f fabfile.py -H '140.82.36.100' -p 'q,Q1%ySN6)f#cr7-'
常用命令
 
lcd(dir): 进入本机某目录
local(cmd): 本机上执行命令
cd(dir): 进入服务器某目录
run(cmd):服务器上执行命令

运行：
fab update
"""


def update():
    with settings(warn_only=True):
        with cd('/root/plover.cloud'):
            run('pkill -9 uwsgi')
            run('pwd')
            run('git pull')
            try:
                run('source /root/python_env/python3/bin/activate && setsid uwsgi uwsgi.ini')
            except Exception as e:
                print(e.args)
    print('更新完毕')
