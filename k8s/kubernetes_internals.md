# kubernetes internals

## Understand the architecture

control plane
- etcd
- api server
- scheduler
- controller manager

work node
- kubelet       
- kubernetes service proxy
- container runtime

add-on components
- kubernetes dns server
- dashboard
- ingress controller
- heapster
- container network interface

### control plane

- 检查control plane各个组件的状态`kubectl get componentstatuses`
- 各个组件之间的交互情况
  - 各个组件都仅与`api server`交互
  - 只有`api server`可与`etcd`交互。其他组件想要修改`etcd`也只能通过`api server`
- `api server`和`etcd`可以同时共存多个实例。而对于`scheduler`和`controller manager`同一时刻只能存在一个。
- 关于etcd的相关概念
  - 一个快速、分布式、一致性的key-value存储结构。
  - 是k8s中唯一用于存储集群信息的地方
  - 使用`optimistic concurrnecy control`来保证数据的一致性
    - [optimistic concurrency control 乐观锁](https://en.wikipedia.org/wiki/Optimistic_concurrency_control)
  - 为了达到高可用性，etcd一般会同时运行多个实例。为了保证多个实例之间的一致性，k8s使用了`RAFT consensus algorithm`。
    - 逻辑可以简化为：在给定某个时刻，集群中所有节点的状态是集群中**多数节点**同意后通过的状态，或是之前同意的状态之一。
    - [RAFT consensus algorithm](https://en.wikipedia.org/wiki/Raft_(algorithm))
  - api server是ectd唯一的客户。
- 关于api server的相关概念
  - api server仅负责提供接口和修改etcd，其他功能由其他组件提供。
  - 订阅机制。订阅者保持一个与`api server`的http连接，当订阅者关注资源的状态发生改变时，订阅者会收到资源的改变信息。
- 关于`scheduler`的相关概念
  - scheduler的大致逻辑
    1. 通过订阅`api server`监控新的pod是否被创建，如果有pod需要被创建，则为其分配一个合适的node。
      - 为pod选择合适node的逻辑很多、也很复杂（直接跳过）
    2. 通过`api server`更新pod的定义数据。
    3. `api server`通过订阅机制通知目标node上的`kubectl`。
    4. `kubectl`创建并运行容器。
- 关于`controller managers`
  - 控制实际的组件达到制定的状态（例如，控制pod达到制定的数量）。
    1. 通过`api server`的订阅机制获取资源实际状态。
    2. 对比`实际状态`和`指定状态`即配置文件中指定的状态。
    3. 向`api server`发送请求，更新资源的状态。
  - 不同的controller之间不相互通讯，甚至不知道之间的存在。
- 关于`kubelet`的相关概念
  - `kubelet`运行在`work node`上。(其他的组件都运行在`master node`上)
  - 主要职责: 
    1. 注册`kubelet`运行的node到`api server`。
    2. 从`api server`订阅分配到该node上pod的信息，当pod状态改变通知`container runtime`。
    3. 持续关注运行在该node上的容器，将其状态发送给`api server`。
    4. 运行`liveness prode`。
    5. 重启和删除`container`。
- 关于`kubernetes service proxy`的相关概念
  - `kube-proxy`运行在`worker`上
  - `kube-proxy`负责将访问`service`的请求负载均衡到连接在`service`后的`pod`上。
    - 内部通过`iptables`实现
- 关于add-ons
  - 关于`DNS server`
    - `DNS server`主要用于方便`pod`通过name连接到`service`或是连接到`headlesss service`的pod。
    - 默认名字为`kube-dns`
    - 实现原理：通过`api server`订阅功能，订阅`service`和`endpoint`的变化。一旦发生变化，更新集群内部所有`container`的`/etc/resolv.conf`文件。

## How services are implemented

- about kube-proxy
  - 所有到service的连接都由该`node`上的`kube-proxy`进行处理。
  - `service`的ip和port成对出现，仅单独使用ip没有意义。
  - `kube-proxy`如何使用`iptables`
    1. 当一个`service`被创建，会立即被分配一个`virtual IP`。
    2. `api server`立即通知所有的node上的`kube-proxy`，新的`service`被创建了。
    3. `kube-proxy`确保其运行的`node`对`新service`是可达的。实际的做法是新增若干条`iptables`记录，将指向`service`的请求，重定向到其关联的任意一个`pod`上。
    4. `kube-proxy`不仅需要时刻监控`service`的状态，还要时刻监控`Endpoints`的状态。

## Running highly available clusters

- making app highly available
  - 同时运行多个实例，降低宕机的可能性
  - 对无法同时部署多个实例的`app`使用[leader-election](https://en.wikipedia.org/wiki/Leader_election)

- making kubenetes control plane highly available
  - 同时运行多个`master node`
  - 同时运行多个`ectd`实例
  - 同时运行多个`api server`实例，每个`api server`仅与相同node上的`ectd`通信
  - `controllers`和`scheduler`的高可用
    
    由于`controllers`和`scheduler`会对各种资源做操作，可能存在竞争关系。

    可以同时存在多个`controllers`和`scheduler`实例，但在任何给定时刻仅能有一个处于活跃状态。详细概念为`leader-election`。当`leader`不可访问时，再从非活跃的实例中，选举一个`新leader`。当`leader`活跃时，其他实例处于`stand-by`状态

## inter-pod networking
- pod之间通信时，必须使用实际pod的ip地址。不能使用`NAT(network address translation)`。
- 同一node上的pod，使用`虚拟网管接口（virtual Ethernet interface）`连接到同一个`bridge`上进行通讯。
- 集群内部所有pod的ip必须唯一。
  - 每个node上`bridges`（ip范围）必须不重叠。
- 不同`node`上的`pod`之间的通讯
  pod -> veth -> bridge -> phycial adapter -> brider -> veth -> pod
- Software Defined Network(SDN)
