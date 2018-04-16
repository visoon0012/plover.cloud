from time import sleep

import paramiko


def config_ss(system_ip, system_name, system_pass, ss_port, ss_pass, is_share):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=system_ip, port=22, username=system_name, password=system_pass)
    # # 执行命令
    # stdin, stdout, stderr = ssh.exec_command('ls')
    # # 获取命令结果
    # result = stdout.read()
    # print(result)
    result = b''
    # 部署SS
    print('正在配置SS')
    shadowsocks = """
    {
        "server":"%s",
        "server_port":%s,
        "local_port":1080,
        "password":"%s",
        "timeout":600,
        "method":"aes-256-cfb"
    }
    """ % (system_ip, ss_port, ss_pass)
    run(ssh, "echo '%s' > /root/shadowsocks.json " % shadowsocks)
    run(ssh, "sudo apt-get update")
    run(ssh, "sudo apt-get install -y python-gevent python-pip -y")
    run(ssh, "sudo pip install setuptools")
    run(ssh, "sudo pip install shadowsocks")
    run(ssh, "sudo apt-get install -y python-m2crypto -y")
    # 部署 BBR
    print('正在配置BBR')
    run(ssh, "wget --no-check-certificate http://www.plover.cloud/shell/bbr.sh")
    run(ssh, "chmod +x bbr.sh")
    run(ssh, 'echo '' | ./bbr.sh')
    # sleep(30)
    # 关闭连接
    print('配置完成，并重启系统')
    run(ssh, 'reboot')


def reboot_ss(system_ip, system_name, system_pass, ss_port, ss_pass, is_share):
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=system_ip, port=22, username=system_name, password=system_pass)
    run(ssh, "ssserver -c /root/shadowsocks.json -d start")
    ssh.close()
    print('重启完成')


def run(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read()


async def async_run(ssh, command):
    ssh.exec_command(command)
