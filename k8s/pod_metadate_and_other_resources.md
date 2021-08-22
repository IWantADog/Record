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

**除了`pod labels`和`annotation`需要通过volumes获取，其他的都可以通过环境变量获取。**
