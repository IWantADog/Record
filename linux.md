# linux相关命令总结及说明

## server login info

w: 服务器当前谁在登录

last：最近谁登录过。登录的信息存放在/var/log/wtmp二进制文件中（容易被删除）。

history：最近使用的命令。历史命令的信息存放在~/.bash_history中（容易被删除）。

strace -p PID: 显示进程调度的资源

lsof -p PID: 程序打开的文件。（句柄）

lsof -i or netstat -plunt：列出正在联网的进程

/var/log/secure: 记录主机的安全信息

/etc/passwd: 用户、用户密码、shell信息

## ssh info

ssh-copy-id: 将公匙发送到目标主机

/.ssh/authorized_keys: 记录所有的公匙信息，也可手动将公匙加入文件的最后。

## user

adduser username

passwd username

usermod -aG wheel username

## iperf3

一个网络性能测试工具。iperf可以测试TCP和UDP带宽质量、报告带宽、延迟抖动和数据包丢失。[detail](https://man.linuxde.net/iperf)

```sh
# 服务器启动服务端
iperf3 -s

# 本地启动服务端
iperf3 -c host -p port
```

## netstat

统计linux的网络状态。

```sh
# 统计所有端口
netstat -a

# 统计所有tcp端口
netstat -at

# 统计所有udp端口
netstat -au

# 统计所有监听中的端口
netstat -l

# 统计所有监听中的tcp端口
netstat -lt

# 统计所有监听中的udp端口
netstat -lu
```

## rpm

`rpm -qf package`

## control user login shell


## how to use search in vim

命令基本形式`:[range]s/{pattern}/{string}/[flags] [count]`
- range: 命令搜寻返回
- pattern: 搜寻的样式
- string: 需要被替换的内容
- count: 重复命令的次数
> 如果没有`[range]`和`[count]`，则仅替换当前游标行所处的行的第一个匹配的数据。

`:s/foo/bar/`: 替换当前行的第一个匹配项

`:s/foo/bar/g`: 替换当前行的所有匹配项

`:%s/foo/bar/g`: 替换整个文件下的所有匹配项

`:s/foo//g`: 如果`{string}`被省略，将所有匹配项替换为`空字符串`

`:s/foo/bar/gc`: 每次替换前询问

`:s/foo/bar/gi`: 设置忽略大小写（默认为大小写敏感）

`:3,10s/foo/bar/g`: 设置替换的范围（line3-line10）
  - `.`: 游标的当前行
  - `$`: 文件的最后一行
  - 通过`+/-`指定范围。
    `:.,+4s/foo/bar/g`: 表示替换当前游标的后4行

`:s/\<foo\>/bar/`: 查找完整的单词。

https://linuxize.com/post/vim-find-replace/