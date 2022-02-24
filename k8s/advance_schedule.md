# Advance Schedule

## node taints/pod tolerations

通过`pod tolerations`和 `node taints`限制pod只能运行在指定的node上。一个pod只能被分配到能够`匹配node taints`的node上。并可通过effect设置不同的响应策略。

- pod的tolerations: `<key>=<value>:<effect>`
- taint effect的种类
  - `NoSchedule`: 如果pod的toleration不匹配node的taint，pod不会被分配到该node。
  - `PreferNoSchedule`: `NoSchedule`的宽松版。一般不合适的pod toleration不会分配到该node，除非该pod没有node接受。
  - `NoExecute`: 与`NoSchedule`和`PreferNoSchedule`仅影响为分配的pod不同。如果该node上运行有不匹配的pod，该pod会被驱逐出node。
- 添加自定义`taints`到node
  - kubectl taint node node1.k8s node-type=production:NoSchedule
- 添加tolerations到pod: 通过yaml设置
- node可以拥有多个`taint`
- pod可以拥有多个`toleration`

## 使用node affinity控制pod被分配到指定node

通过`node affinity`设置pod只能被分配包含指定lable的node。提供更灵活，更强大的功能。

- requiredDuringSchedulingIgnoredDuringExecution
  - requiredDuringScheduling: pod必须被分配到包含该lable的node
  - IgnoredDuringExecution: 不影响该node上正在运行的任意pod
- preferredDuringSchedulingIgnoredDuringExecution
  - 设置多种情况

## 分配pod到node时，控制不同类型pod之间相互影响
- topologyKey: 控制pod直接的距离。可以设置为固定值或范围值
  - kubernetes.io/hostname
  - failure-domain.beta.kubernetes.io/region

使用`affinity`可以控制不同pod分配到同一个node上。
  - 使用`topologyKey`: 控制pod在同一个node，或是同一个区域

使用`anti-affinity`可以控制两种pod不同时出现在一个node上。
  - 使用`topologyKey`: 控制pod不会同时出现在一个node，或是同一个区域


## Reference

还是官方文档解释的详细

https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/

https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/
