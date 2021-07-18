# About Controller

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