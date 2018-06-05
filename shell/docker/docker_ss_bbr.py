from fabric.api import *

"""
Plover自动化运维脚本
"""
env.hosts = [
    'root@45.76.162.112',
]
env.passwords = {
    'root@45.76.162.112:22': 'k2)HZ8Fo}q2ta2WC',
}
"""
1、初始化
fab -f docker_ss_bbr start
2、重启
fab -f docker_ss_bbr restart
3、停止命令：
docker rm -f shadowsocks lkl
"""


def start():
    with settings(warn_only=True):
        run('sudo wget -qO- https://get.docker.com/ | bash')
        run('sudo docker run -d -e PASSWORD=plover.cloud -p 8388:8388 --name shadowsocks wuqz/sss:latest')
        run('sudo docker run -d --privileged --link shadowsocks:myhost -e TARGET_HOST=myhost -e TARGET_PORT=8388 -p 8888:8888 --name lkl wuqz/lkl:latest')
    print('更新完毕')


def restart():
    with settings(warn_only=True):
        run('sudo docker run -d -e PASSWORD=plover.cloud -p 8388:8388 --name shadowsocks wuqz/sss:latest')
        run('sudo docker run -d --privileged --link shadowsocks:myhost -e TARGET_HOST=myhost -e TARGET_PORT=8388 -p 8888:8888 --name lkl wuqz/lkl:latest')
    print('更新完毕')


def stop():
    with settings(warn_only=True):
        run('sudo docker rm -f shadowsocks lkl')
    print('已停止')
