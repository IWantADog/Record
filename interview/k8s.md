# k8s

## node

k8s有多个node构成。node有两种master, worker。master负责管理整个集群，worker负责运行具体的app。

master的构成
- kubernetes api server: 提供接口修改etcd
- scheduler: 为applicaiton分配node
- controller manager: 
- etcd: 分布式数据存储，保存集群的配置信息

worker的构成
- kubectl
- 容器
- kubernetes server proxy:

## pod

pod本质一组相关容器的组合体。一个pod中的所用容器运行在同一个nodes上。

每个pod自己的ip、hostname、process。可以将pod想象为一个独立的机器，不同pod之间相互独立，互不干扰。但pod之间可以通过ip通讯。

虽然一个pod可以拥有多个container，不过一般一个pod中应该仅有一个container。

主要的原因是一个pod中的多个container仅能运行在一个worker上，无法重复使用资源；而且可能带来版本管理的问题，例如仅需要升级某一个container的版本，而不得不重启所有的容器；当某一个container的app崩溃了，需要开发自己实现重启的逻辑。

## probe

- liveness probe: 决定何时重启container
- readiness probe: 决定何时一个pod开始接受流量
- startup probeL: 确定container中的application是否已启动

### 使用probe的注意事项
- prod对应的endpoint必须足够轻量级，并且不需要认证，不能包含复杂的逻辑
- probe主要的功能是为了检测container中application是否还在正常运行。


## service

由于k8s中的pod挥别kill、重启、动态扩容。所以通过ip直连pod十分麻烦。service及时用来解决这个问题。

每个service在其生命周期中，拥有固定的port和ip。当client需要连接pod时，直接访问service，再有service将请求转移给pod。

## Ingress

ingress用来将服务暴露给外部。

request -> ingress -> service -> endpoints -> pod

## configmap

- 设置环境变量
- 挂载文件系统

## 常用命令

kubectl logs

kubectl top

kubectl exec

kubectl get

kubectl describe

kubectl cp
