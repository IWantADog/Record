# docker

## 需要回答的问题
- [x] docker和虚拟化技术之间的区别
  - 虚拟化技术虚拟的是硬件
  - docker是通过linux的namespace和cgroup将不同的服务隔离起来
- [x] docker run中--link的用法
  - link可将不同container之间的网络连接起来
- [x] docker run中--entrypoint的用法
  - default command to execute at runtime

## 1

### 什么是docker

docker使用的是linux namespace和cgroups

docker容器隔离包含8个方面
- pid命名空间：进程标识符和能力
- UTS命名空间：主机名和域名
- MNT命名空间：文件系统访问和结构
- IPC命名空间：通过共享内存的进程间通信
- NET命名空间：网络访问和结构
- USR命名空间：用户名和标识
- chroot()：控制文件系统根目录的位置
- croups： 资源保护

## 2

### 消除源数据冲突

docker create --cpid: 通过cpid文件创建container，

`docker run`与`docker create`的区别

## 3

docker load/save
将镜像导出为文件

## 4 持久化存储和卷间状态共享

将主机的文件系统挂载到容器中，这样及时容器被删除后，数据依然不会丢失。

docker中提供了两种挂载卷
- 绑定挂载卷：由用户指定主机上需要挂载到容器中的文件位置
- docker管理存储卷：由docker自行确定数据存储在主机上的位置，仅需要提供容器中的挂载路径
> 什么使用场景？？？

`--volumes-from`: 将其他容器中挂载的卷也同样挂载到当前容器。不过volumes-from也有一些限制：
- 不能修改容器中的挂载
- 当多个容器中的挂载点相同时，挂载点会冲突，无法获取完整的数据
- 无法修改挂载点的读写权限

## 5 网络访问

docker提供了四种容器的配置，隔离程度从高到低依次为:
- close
- joined
- bridge
- open

通过`--net`来进行设置

### close

无法与容器外部的网络通信，仅能访问容器内部接口

### bridge

可以连接到容器外的网络，同时也可以访问内部接口

通过`-p/-P/--expose`将容器的端口与主机的端口建立映射

### join

使多个容器之间共享网络接口。*可以理解为将多个容器在网络层面融合，将其视为一个容器。*

### open

直接与主机的网络相连

### include

将不同容器在网络层面链接起来。使用include时被连接的容器必须已经存在。

使用include建立的容器之间的连接是*静态的、单向的、不可传递的*。
- 静态：依赖方容器，绑定的是被依赖容器的ip地址，如果ip切换则依赖会无法使用。
- 单向：只能依赖方能访问别依赖方
- 不可传递： 如果A依赖B，B依赖C，但A无法直接访问C

## 6 隔离

### 共享内存

默认情况下docker为每个容器创建一个独立且唯一的IPC命名空间。linux的ipc命名空间共享内存单元。

### 跨容器的进程间通信

使用 *--ipc* 是多个容器共享同一个ipc命名空间。

### 开放内存容器

*--ipc host*：使容器与主机上的其他进程运行在同一个命名空间中，这样容器中的进程就能和主机上的进程进行通信。

## 7 在镜像中打包软件

docker镜像的分层

### 联合文件系统
- 当从联合文件系统中读取一个文件，系统会从存在该文件的最上面一层中读取。如果文件没有在最顶层被创建或者被修改，那么读取操作就会沿着层不断向下找，直到找到存在这个文件的层。
- 当一个文件被删除或修改，一个删除/修改记录就被写入最顶层，它会遮挡底层所有该文件的版本。
- copy-on-write：当在容器中对一个已存在的文件进行修改时，会先将该文件从容器的下层复制到最上层，再进行修改。并且仅有被修改的文件才会被复制到当前层。
- 联合文件系统由多个层以栈的形式构成，并且新的层会被添加到栈的最上方。这些层会被独立存储，每层包含这一成的改动信息和元数据。
- 一个镜像由多个层以栈的形式构成，首先会给一个顶层作为起始点，然后根据每层原数据中的父层ID将多个层自上而下地连接起来

#### 导入导出扁平文件系统

docker export/import

## 构建自动化和高级镜像设置

### dockerfile

每一个dockerfile指令都会创建一个镜像层，所以尽可能的合并指令，能够减少镜像的大小和层的数量。

onbuild: onbuild后面的命令在当前镜像build时，不会执行。而当将该镜像作为一个父镜像时，onbuild后面的命令才会生效。*不是很清楚使用场景*

entrypoint: 可以将一个检验容器环境变量是否配置正确的脚本作为容器的入口。这是entrypoint的一个使用场景。

### 初始化进程

init

## docker compose 声明式环境

docker compose: 通过yaml文件声明多个容器，便于多容器生命周期和容器之间关系的管理。

docker-compose build

docker-compose up: 不加限制的话，每次调用都会重新创建并启动全部服务。并且不会影响数据卷的挂载，即使容器新建并重新启动，数据也不会丢失。可以通过`--no-dep`，仅更新一个具体的服务。
- 但是如果多个容器之间存在依赖关系，在没有服务发现的环境下，如果某个服务需要重启，最好还是重启整个服务。如果仅重启单个应用，重启后服务ip地址的修改。会导致其他服务无法访问该服务。

docker-compose scale: 对一个具体的服务进行横向扩展。
> TODO: 不过不是很很明白，当服务扩展之后，如何控制流量进入那个服务。

## Best practices for writing Dockerfiles

[official link](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### understand build context

当使用`docker build`时，会将当前目录的所有文件作为*build context*发送给*docker daemon*。并且默认dockerfile在该目录下。不过也可以通过 `-f` 使用位于别处的dockerfile。

build可以读如来自stdin的数据，并且不带有`build context`。具体使用如下`docker build -`，需要注意`-`的使用。


### dockefile instructions

copy & add: copy和add的功能类似。copy仅支持将文件复制到容器中。add支持获取远程文件和解tar包等功能。
> 不过官方还是建议使用copy，至于获取远程文件可以考虑使用curl/wget等方式。理由是使用这种方式能够将不需要的数据及时清除，控制容器的大小。

### multi-stage build

[official document](https://docs.docker.com/build/building/multi-stage/)

主要目的：保证dockerfile编写的更易维护和理解，并且尽可能减少容器的体积（通过将build任务进行分层，在每个阶段容器中仅包含必须的部分）。
