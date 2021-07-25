# About Service

由于pod的易变性、动态扩展通过ip直连pod十分麻烦。而`Service`的使用就是为了解决这个问题。

所有的`Service`在它的整个生命周期拥中有固定的`ip`和`port`。当`client`需要连接pod时，直接访问`service`，再由`service`将请求转移到某个`pod`。

## service affinity on the session

为了让`service proxy`将同一源位置的请求全部重定向到相同的`pod`。可以修改`session affinity`为`ClientIP`。

> Kubernetes支持两种类型的`service session affinity`: `None` & `ClientIP`。

## 为pod和service的端口设置别名

可以为`pod`和`service`的端口设置别名。这样使端口的信息更直观。而且这样做的最大的好处是，可以修改端口号而不用修改`pod`或`service`中的端口配置。

## pod如何知道service的信息

当一个pod被创建时，k8s会将当前时刻所有的`service`的信息都写入pod的环境变量中。当pod运行时会从环境变量中读取。

## 通过`FQDN`连接到service

FQDN: fully qualified domain name.

`backend-database.default.svc.cluster.local`。其中`backend-database`是service的名字，`default`是service的`namespace`，`svc.cluster.local`是集群中的通用配置前缀。

> 当相同namespace下的pod与service通信时，可以省略`svc.cluster.local`和namespace.实现的原理是每个pod下都有一个`/etc/resolv.conf`文件。

## understand why you can't ping a service ip

TODO: 虚拟ip，当ip和port同时存在时才有意义。

## Connecting to service living outside the cluster

`service`不仅仅可以在集群内部重定向请求，也可以将请求重定向到集群外部。

### service endpoints

`service`并不直接与`pod`链接。在service和pod之间还存在一层资源--`Endpoints`。

`Endpoints`本质上是暴露给`service`的`ip:port`列表。
> `endpoints`是一种k8s资源，并不是service的属性。

这里还涉及到service的`label-selector`。`endpoints`中的`ip:port`列表就是根据`label-selector`获取的。当请求连接到`service`，service proxy会从endpoints中选择一个`ip:port`将请求重定向。

### 手动修改service endpoints



## related command

kubectl expose

kubectl get svc

kubectl exec

kubectl get endpoints <service_name>
