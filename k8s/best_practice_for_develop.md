# best practice for develop

## pod init container

在`main container`启动之前，可以先执行一个`init container`用于做一些条件检查。直到条件符合之后，再启动`main container`。

具体的设置方法是在`pod`yaml中设置`spec.initContainers`。

虽然k8s支持通过`init container`控制app的依赖关系，但这并不是种良好的设计。

更合理的设计是在app内部增加当依赖不可用的逻辑，或是使用`readiness probe`控制pod之间的依赖关系。

## container的生命周期hook

- post-start hook
- spre-stop hooks

主要采取的方式: `执行一条command` or `向一个url发送get请求`

### post-start hook
- 在`main container`开始之后立即被调用，并不会等待`main container`完全启动完全，而且hook也无法确定何时`main container`完全启动。
- 如果hook执行失败，`main container`会被kill

### spre-stop hook
- 该hook在container被中断之前执行
- 不论hook是否成功执行，container最终都会被kill

## 理解pod的shut down

shut down的主要逻辑次序
1. 如果配置了`pre-stop hook`，则调用，并等待执行完毕
2. 发送`SIGTERM`信号container中的`main container`
3. 等待container被删除完全或`等待时间`耗尽
4. 强制向进程发送`SIGKILL`，如果container没有被删除干净

container的停止时间（temination grace period）能够通过`spec.terminatinGracePeriodSeconds`设置。

## 确保所有请求都被合理的处理

### 确保pod启动时，所有请求被合理处理

通过`readiness probe`实现

### 确保pod被终止时，所有请求被合理处理

- 当pod被删除时引发的一系列事件
  同时有两件事被触发，并且是并行执行
  - 删除pod
    1. api server通知kubelet删除pod
  - 更新endpoint和iptable
    1. api server通知`Endpoint controller`修改endpoint
    2. `Endpoint Controller`回复api server
    3. api server通知所有的`kube-proxy`并更新`iptables`

没有完美的解决方法，唯一能做的就是在pod被完全删除之前，等待一段时间。这里的主要目的是，等待已建立的连接尽可能的响应。当时间耗尽，就强制删除pod。

## 在k8s中合理控制和管理app
- 合理控制image的大小；但也需要包含若干便于调试的命令
- 添加多个、合理的lable
- 添加合理的annotation
  - 依赖的服务列表
  - 维护人员列表
- 记录容器被kill的信息
  - spec.containers[0].terminationMessagePath: 指定当container被中止时，信息被写入的文件路径。
- 处理app日志
  - 查看单一pod日志
    - kubectl logs (--previous)
    - 集中式管理日志
      - FluentD
