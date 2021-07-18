# Basic k8s


## k8s大致的情况

在硬件层面，kubernetes集群由多个node组成，node可以分为两类。

- master node: 负责`kubernetes control plane`，其负责管理整个kubernetes系统。
- worker node: 运行实际的application

control plane（master node）的构成
- kubernetes Api Server: 
- Scheduler: 为applicaiton调度分配node
- Controller Manager: 负责cluster层面的逻辑，比如复制组件、跟踪worker node、处理异常等情况。
- etcd: 可靠的分布式数据存储，保存集群的配置信息

worker nodel的构成
- 容器: Docker，rkt，或者其他。
- kubelet: 负责与API server通信，控制本node中的容器。
- kubernetes service proxy: 控制各个application容器之间的网络通信

一旦application开始运行，k8s会始终保证application的状态符合配置文件中定义的。例如配置中指明某个application有5个实例，那么k8s会始终保持5个实例正在运行中。如果某个实例崩溃或是故障，k8s会自动重启它。
同样如果某个`worker node`无法使用，k8s会将该node上的容器全部转移到另一个可用的node上。

用户能够app运行时在修改app的数量，k8s会自动的增加或减少app的数量。这些也可完全由k8s来控制，比如根据cpu负载、内存、每秒的请求数量等。

使用容器而不将app部署在某个指定的node上，使用户在任何时候能够自由地移动app。部署在cluster中的app能够被k8s合理的组合使所有的资源被合理的使用。

## 关于容器

linux control groups & linux namespaces

## 关于pod

pod是一组相关容器的组合体。pod中的容器运行在`同一个node`上，并且拥有相同的`linux namespace`。

每一个pod像是一个独立的逻辑上的机器，拥有自己的IP、hostname、process。

一个pod中的所有container运行在同一个`logic machine`，而不同pod的container，即使运行在同一个node，也表现为运行在不同的logic machine。

每个pod都有各自的ip，即使不同的pod位于不同的node。他们依然可以相互通讯。

通常情况下每个pod只应该包含一个`container`。一个重要的原因是当多个`container`包含在一个`pod`中时，这些`container`只能运行在一个`worker`上。
> 虽然pod内部支持运行多个container，为了保持简单，应该尽量保证一个pod只包含一个container。

### 当使用kubelet run后发生了什么
输入`kubelet`后，
1. 向`kubernetes api server`发送`rest http request`创建了`ReplicationController`。
2. `ReplicationController`创建一个pod
3. `Scheduler`将pod分配到一个合适的node
4. node上的kubelet识别到被分配给自己，之后委托docker拉取指定的`image`。image下载完成之后，运行container。

__pod被分配的ip地址都属于内部ip，外部无法直接访问__。为了使pod能够被外部访问，需要一个`Service`。创建一个`LoadBalancer-Type service`，之后就可通过这个`load balancer`的`public ip`访问到内部的pod。

### 为什么使用pod

对比多个`applicaton`运行在同一个`container`和运行多个`container`的利弊。
- 多个`application`运行在一个container管理十分不便。
    - 例如其中的一个app需要升级、或是修改依赖项。必须重新部署镜像时，也可能对其他的app造成影响，并且也需要重启其他的app。
    - 某个app崩溃了，需要自己实现重启的逻辑。
    - 当所有的app输出日志到标准输出时，所有的日志都混在一起难以分辨。

由于多个app部署在同一个container中的管理问题。而当多个相关的容器需要统一管理时，就需要新的概念--pod。

### 理解pod内部container的部分隔离

k8s通过配置`Docker`使一个`pod`中的所有`container`共享一个linux namespace。

由于一个pod的所有container在相同的`Networks` & `UTS` namespace，所以他们共享相同的`hostname` & `network interfaces`。

并且所有在同一个`IPC`namespace下的所有`container`能够通过`IPC`相互通讯。
> [IPC: interprocessing communication](https://tldp.org/LDP/tlk/ipc/ipc.html)

### 如何合理地使用pod

为什么每个pod最好只包含一个container？

1. 不能合理使用node资源。一个pod只会运行在一个worker上，如果一个pod内部运行多个app，则只会使用一个node的资源。
2. 无法合理的横向扩展。一个pod中的多个app，对于横向扩展的需求不同。

何时应该在一个pod中使用多个`container`?

类似于存在一`main container`和多个`support container`的结构。support的功能可能类似于日志收集、文件下载和存储等。
> 书中这里提到了`sidecar`

## 关于`ReplicationController`

`ReplicationController`负责管理pod，当使用`kubelet run`时可以指定pod的数量，如果不指定pod的数量，默认只会创建一个pod。而且当pod由于意外挂起时，`rc`会自动创建一个新的pod代替旧的。

`ReplicationController`会始终监视`运行中的pod`数量，保证其数量等于配置的数量。如果pod的数量过少则新增pod，如果pod的数量过多则删除pod。

如果手动删除`rc`，会导致该rc所有的pod一并被删除。不过可以通过`--cascade=false`仅删除`rc`而不删除`pod`。

### ReplicationController的核心概念
- label selector: 确定`ReplicationController`所拥有的pod。
- replica count: pod的数量。
- pod template: pod的模版。

### tips
- 定义`ReplicationController`可以不指定`pod selector`。而在`pod template`中设置，这样可以保证定义`rc`的yaml更简洁。
- k8s不允许修改`rc`的label selector，当有这样需求时，可以修改`pod template`中的lable selector。

### common commands

修改pod template的 lable selector

`kubectl edit rc <rc_name>`

水平扩展pod的数量

`kubectl scale rc test --replicas=3`

> 用户无法也不能直接指定`kubernetes`该做些什么。用户只能告诉k8s一个期望的状态，k8s自己决定如何达到指定的状态。这是k8s的基本准则。

## About ReplicaSets

`replicaSets`是`replicationControllers`的增强版。（`ReplicationControllers`最终将会被完全移除）

相较于`ReplicationControllers`，`ReplicaSets`提供了更富有表现力的`lable selector`。`RC`只提供通过明确的`label`筛选`pod`。而`RS`可以匹配缺少`label`的`pod`，或仅通过`label key`筛选`pod`，而忽略`label value`。

`RS`还提供`IN` & `NotIN` & `Exists` & `DoesNotExist`。可以使用这些写出更具体的`label selector`。

## About DaemonSets

DaemonSets会在每一个`node`上部署一个执行特定任务的`pod`。当一个新的node被启动时，`DaemonSets`会自动部署一个新的实例到该`node`中。

`DaemonSets`也可以指明仅部署pod到特定的node上(通过`node-Selector`设置)。而如果一个node在部署了`DaemonSets`的pod之后，又被移除了`label`，部署的pod会被关闭。

**如果关闭`DaemonSet`，相关联的所有`pod`都会被删除。**

### 额外的情况

k8s中存在拒绝`pod`部署的`node`。对于这样的`node`，`DaemonSet`依然会部署在上面。其中的原理是，拒绝`pod`部署的`node`是通过阻止`schedule`向指定的`node`来实现的。而通过`DaemonSet`部署的`pod`会完全绕过`schedule`。

### how to use

// 查看指定的`DaemonSet`

kubectl get ds

## about Job

`Job`通过`pod`运行任务，`job`运行完成后pod就会被删除。

### 特性

- 当运行`job`的`node`故障时，`job`会被移动到其他的`node`运行。
- 当`job`由于自身的问题导致运行失败时，可以通过配置指定`job`是否重新运行。
- `job`可以指定 **`pod`运行多次** 和 **多个`pod`同时运行**。
    - spec.completions: 设置`pod`需要被运行的次数。
        > 需要注意的多次运行pod时，每次用的都是新的pod。也就是说任务需要运行N次，就会创建N个`pod`。并且如果`pod`运行失败，最后实际创建的`pod`数量可能大于需要执行的任务次数。
    - spec.parallelism: 设置需要同时运行的pod数量。
        > job支持运行中修改并行pod的数量。
- 指定运行时间限制`activeDeadlineSeconds`，如果实际运行时间超过了指定的时间，job会被标记为失败。

## About CronJob

定时运行的`job`。

### how to use

// 查看指定`Job`

kubectl get jobs

## how to use

// 删除pod
kubectl delete po <pod_name>

// 通过label删除pod
kubectl delete po -l <label_key>=<label_value>

// 通过删除namespace，删除pod
kubectl delete ns <namespace_name>


## 关于Service的功能

pod是易变的，可能随时挂起。当新的pod被创建时，pod会获得一个新的ip地址。如果直接通过pod的ip连接pod，会导致新建pod之后原有的ip完全不可用。

Service就提供了这样的功能。在Service的整个声明周期中它始终有一个静态ip。当需要连接一个pod时，间接通过Service访问pod。Service始终保证pod可以被访问，而无论pod具体在哪里。

Service还能为多个pod同时提供服务，当一个请求进来时会被转接到某一个pod上。


## labels

labels在k8s中用来分类管理不同的资源。一个资源可能有多个labels。

通常也可使用label来搜索不同的资源。

## liveness probes

k8s支持application的health check。当applicaiton崩溃后，k8s会自动`重启pod`。

k8s探测容器内部状态的几种原理:
- 通过`HTTP get`向容器中的用户事先定义的`endpoint`，如果请求失败，则将容器重启。
- 通过`TCP Socket`向容器的特定`port`建立连接。如果连接建立成功，则表明容器时正常的；反正，容器会被重启。
- 通过执行容器中某个`command`，判断命令的结束状态。如果命令执行失败，则容器会被重启。

`probe`还支持其他的而外参数:
- delay: 设置延迟时间。当container被启动时延迟若干时间等待container完全启动。
    > initialDelaySeconds: 设置延期时间。
- timeout: 超时时间。当container的相应时间超过设置的时间，则视为探测失败，容器会被重启。
- period: 检测间隔。
- failure: 设置失败可以接受的次数。只有失败的次数超过设置的值后才会重启`pod`。

### exit code
- 137: 128 + 9(SIGKILL)
- 143: 128 + 15(SIGTERM)

### 合理使用`porbe`的建议
- 对于生产环境必须使用`probe`
- `probe`的`endpoint`需要十分轻量，并且不需要认证。`probe`会被频繁触发，不能包含复杂的计算逻辑。
- 需要清楚的明白，`probe`的主要目的是检测`container`中`application`是否还在正常运行，不能引入无关的信息。
    > 书中例举一个例子。不能因为后端数据库的连接失败，而重启application。这没有用处，即使重启application，health请求依然会失败。


### 新增label、修改label
kubectl label po <pod_name> <label_name>=<lable_value>

kubectl label po <pod_name> <label_name>=<label_value> --overwrite

kubectl get po -l <label_name>=<label_value>

kubectl get po -l <label_name>

kubectl get po -l "!<lable_name>"

## annotating pods

类似与label也是`key-value`结构，不过不能用来对资源进行筛选，但是能够存储更详细的说明信息。

## namspaces

k8s的namespace并不是linux中namespace。linux中的namespace用来隔离进程。__而k8s中的namespace主要应用是避免资源名称的冲突。__

__需要注意的是k8s提供的namespace的隔离，不会影响不同namespace下的pod进行网络通讯。__

### how to use

// 获取所有的namespace
kubectl get ns

// 获取指定namespace下的资源
kubectl get po --namespace/-n <you_namespace>

// 创建一个namespace(不过我想一般还是会直接通过yaml文件创建吧)
kubectl create namesapce my-namespace


## k8s常规使用

kubectl cluster-info

kubectl get nodes/pods

kubectl describe pod/nodes/svc

kubectl expose rc

// 通过yaml创建k8s资源

kubectl create -f this_is_a_test.yaml

// 打开并编辑资源的yaml文件

kubectl edit <type> <resoure_name>

// 获取pod的yaml配置信息

kubectl get pod test_pod -o yaml

// 获取pod的日志

kubectl logs <name>

// 如果一个pod中包含多个container

kubectl logs <pod_name> -c <container_name>

// 获取上一个容器的log

kubectl logs <pod_name> --previous

// 将pod的端口绑定到本机指定端口

kubectl port-forward <pod_name> <local_port>:<pod_port>

// 查看资源的label

kubectl get po --show-labels
kubectl get po -L <label_name_1>,<label_name_2>

// 删除当前namespace下的所有资源(太危险了，不应该使用)

kubectl delete all --all

k run test --image=benjilee5453/test --port=5000 

k expose pod test --type NodePort --port 8080
> 这里的port指的是需要绑定的pod的端口。
minikube service hello-minikube --url

source <(kubectl completion zsh) # zsh kubuctl 命令自动补全