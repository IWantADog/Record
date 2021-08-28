# pod metadate and other resources

accessing pod metadate and other resources from applications

TODO: 感觉找不到这部分知识放在哪里合适，先这样吧，看完之后通篇了解之后在说吧。

## Downward API

`Downward API`主要解决的问题是，通过某种方式使容器内部可以获取k8s资源的属性。因为有些数据并不固定而是动态生成的例如pod的ip，label等属性--这些属性都在pod生成才有。

`Downward API`并不像`REST`请求之后返回数据的形式，而是通过`环境变量`和`文件（volume）`的形式获取数据。

可以获取的pod metadata
- pod name
- pod ip address
- namespace the pod belongs to
- the name of the node the pod is running on
- the name of the service account the pod is running under
- the CPU and memory request for each container
- the CPU and memory limits for each container
- the pod's lables
- the pod's annotations

**除了`pod labels`和`annotation`需要通过volumes获取，其他的都可以通过环境变量获取。** 并且在pod运行期间`label`和`annotation`是可以被随时修改的，而如果通过*环境变量*无法实现动态修改，通过*volume*则可以。

需要额外注意的一点是，如果需要暴露容器层级的资源，需要明确指定容器名，即使一个pod中仅有一个容器。

## 直接从kubernetes API server获取数据

虽然使用`Downward API`可以获取k8s资源信息，不过获取到的数据还是有限的。如果想要获取其他pod或是集群上的其他资源时，可以使用直接访问`Kubernetes APi server`。

直接获取api server: `kubectl cluster-info`

### kubectl proxy

访问`kubernetes api server`需要额外的用户认证，而使用`kubectl proxy`会在本地机器上启动一个代理服务，它来帮我们处理所有与api server的认证信息。并且启动一个代理服务十分简单`kubectl proxy`。

运行`kubectl proxy`启动本地代理服务后，可以直接通过`127.0.0.1:80001`访问`api server`。

### 在pod中访问api server

在pod中访问api server首先需要明确三件事：
- 找到api server的地址
    - 通过`kubectl get svc`
    - 通过pod中的service的环境变量
- 确定与api server直连，没有其他假冒的server
    - `curl --cacert /var/run/secrets/kubernetes.io/service account/ca.crt https://kubernetes`
- 连接api server需要用户认证，不然什么也看不到
    - 获取用户认证token
    - 指明获取数据的namespace

简化使用和使用`kubectl proxy`类似。在pod中单独起一个`ambassador container`用来专门处理用户认证，并且`main container`和`ambassador container`容器之间通过http通讯。

### 使用client libraries与api server通讯

pass
