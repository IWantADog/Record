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

`service`不仅可以将进入集群内部的请求重定向，也可以将内部的请求重定向到集群外部。

> 对于重定向到外部的请求，简单点理解就是在集群内部定义一个`service`，这个`service`后边对接的就是集群外部的`API`。

### service endpoints

`service`并不直接与`pod`链接。在service和pod之间还存在一层资源--`Endpoints`。

`Endpoints`本质上是暴露给`service`的`ip:port`列表。
> `endpoints`是一种k8s资源，并不是service的属性。

这里还涉及到service的`label-selector`。`endpoints`中的`ip:port`列表就是根据`label-selector`获取的。当请求连接到`service`，service proxy会从endpoints中选择一个`ip:port`将请求重定向。

## Exposing services to external clients

将service暴露给外部。
- `NodePort`
    
    对于一个`Nodeport`服务，集群中的每个`node`都会开放一个端口并且将经过这个端口的所有请求都重定向到下层的服务。

    > `NodePort` service不仅仅可以通过被分配的静态ip连接，也可通过`node`的ip和暴露的port访问。

- `LoadBalancer`

    `NodePort`类型的扩展。需要云服务提供商提供负载均衡功能。如果无法提供负载均衡功能，则`LoadBalancer`实际功能会退化为`NodePort`。

    `LoadBalancer`的主要功能是保证请求始终会进入一个正常运行的`node`，不会因为某个`node`的崩溃导致请求无法被相应。

- `Ingress`

    详细参见 -- 关于`Ingress`

### 关于`Ingress`

从概念上讲，`Ingress`位于`Servers`的更上层。

request -> Ingress -> Service -> Endpoint -> pod

#### 理解为什么需要`Ingresses`

一个很重要的理由是每个`LoabBalancer` service都需要一个专属于它的公开ip。而`Ingress`仅需一个ip地址。

当请求进入`Ingress`时，`Ingress`可以根据`host`和`path`将不同的请求重定向到合适的`service`。

并且`Ingress`作用在`http`层可以提供一些基于cookies的功能。

#### 关于`Ingress Controller`

如果想要`Ingress`工作，必须要有一个`Ingress Controller`存在集群内部。这个功能一般由云厂商提供。


### 关于`externalTrafficPolicy`

当一个请求通过`service`随机选择了一个`pod`时，选中的`pod`可能并不运行在相同的`node`。这时请求为了找到被分配的pod，会花费额外的时间并且这并不是我们希望的。

为了防止这种情况的发生，可以设置`externalTrafficPolicy: Local`。当一个外部的请求进入时`service`会从当前`node`上选择一个`pod`，如果不存在一个pod，请求会被挂起。

### 通过`Ingress`暴露多个services

Ingress支持两种方式
- 通过指定`path`
- 通过指定`host`


## related command

kubectl expose

kubectl get svc/ingresses

kubectl exec

kubectl get endpoints <service_name>

kubectl create secret tls

