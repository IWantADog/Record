# vps出现多次未知失败登录问题

问题描述：

- 登录vps时系统提示出现多次未知ip的失败登录。应该是被扫描了端口，想通过ssh暴力登录。查看/var/log/secure发现都是通过root账户使用密码登录。

- vps版本为centos8

补救措施：

1、创建用户账号、停止使用root账号ssh登录

```sh
adduser userNmae -m

passwd userName

usermod -aG wheel userName
```

2、限制通过ssh登录的用户并禁止使用root账户连接ssh

/etc/ssh/sshd_config保存sshd服务配置信息。

```shell
# 默认端口号, 十分重要

Port 2345

# 阻止 root 登录：

PermitRootLogin no

# 运行特定用户使用ssh登录

AllowUsers alice bob
```

配置文件修改完毕后通过`service sshd restart`,重启sshd服务

3、ssh使用非标准端口

/etc/ssh/sshd_config中Port的默认端口为22，修改默认端口可以有效地减少攻击。

修改相关防火墙规则
`$ cp /usr/lib/firewalld/services/ssh.xml /etc/firewalld/services/ssh-custom.xml`

更改 /etc/firewalld/services/ssh-custom.xml 令端口与 ssh 配置文件内的相同：
`<port protocol="tcp" port="2345"/>`

最后，删除 ssh 服务，新增 ssh-custom 服务，并重启 firewalld 令改动生效：

```shell
$ firewall-cmd --permanent --remove-service='ssh'
$ firewall-cmd --permanent --add-service='ssh-custom'
$ firewall-cmd --reload
```

还需要更新 selinux，并正确地标签所选用的端口，否则 sshd 便不能访问它。举个例说：
`$ semanage port -a -t ssh_port_t -p tcp 2345 #请更改这处`

## semanage command cant find

yum install policycoreutils-python

__最后重启sshd服务__

4、防火墙过滤ssh连接

这里使用的防火墙是firewall, 关于iptable的使用参见连接[SecuringSSH](https://wiki.centos.org/zh/HowTos/Network/SecuringSSH)

采用 firwalld（CentOS 7）的加强规则局限 ssh 至特定的端口。来源地址可以是单一地址或是基本地址及位元掩码：

```sh
# 视乎已启用及现存的设置，选用 ssh 或　ssh-custom
$ firewall-cmd --permanent --remove-service="ssh"
$ firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="72.232.194.162" service name="ssh-custom" accept'
$ firewall-cmd --reload
```

SSH 亦对 TCP 包装函式有内置支持，因此 ssh 服务的访问权亦可同时用 hosts.allow 及 hosts.deny 来进行管制。

创建一条每分钟只指纳 4 个连接并记录所有连接的规则。

```shell
$ firewall-cmd --permanent --add-rich-rule='rule service name="ssh-custom" accept limit value="4/m" log' 
$ firewall-cmd --reload
```

5、使用ssh登录，放弃使用密码登录。

将本机的public key发送到vps。```ssh-copy-id username@host```

由于修改了ssh的端口，使用ssh登录时需要手动输入参数，为使用简便可配置~/.ssh/config

```vim
Host sshtest
    HostName ssh.test.com
    User user
    Port 2200
    IdentityFile ~/.ssh/id_rsa_test
```

配置完成后使用`ssh sshtest`即可简便登录。

## 参考链接

[SecuringSSH]([SecuringSSH](https://wiki.centos.org/zh/HowTos/Network/SecuringSSH)
)

[linux认识登录文件](http://cn.linux.vbird.org/linux_basic/0570syslog.php#syslogd_format)

## bbr

[Google BBR是什么？以及在 CentOS 7 上如何部署](https://tech.jandou.com/CentOS7-Google-BBR.html)
[为VPS开启BBR拥塞控制算法](https://xiaozhou.net/enable-bbr-for-vps-2017-06-10.html)

## 检测centos的版本及使用内核版本

`cat /etc/centos-release`

`uname -r`

## 简单点的话
1. 创建一个新用户
2. 仅允许该用户通过ssh登陆