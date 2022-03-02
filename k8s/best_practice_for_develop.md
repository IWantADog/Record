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


