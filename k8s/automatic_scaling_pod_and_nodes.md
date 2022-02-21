# automatic scaling pod and nodes

## 横向扩展pod

HorizontalPodAutoscaler(HPA)
  
周期性监控所辖的pod的各种指标；与设置的指标进行比对；修改pod数量

- 周期性监控所辖的pod的各种指标
  - 数据采集流程: pods -> cAdvisor(s) -> Heapster -> HPA(S)  
  - autoscaler的输入输出：接受多种数据，计算之后得出一个int（pod的数量）。
  - 对于多个指标，Autoscaler会分别计算各自的指标。计算出满足各种指标所需的pod的数量。之后取最大的那个。

### 基于cpu指标的扩展

- autoscaler基于cpu的扩张需要使用request(计算实际使用的cpu和request的比例)
- “kubectl autoscale deployment kubia --cpu-percent=30 --min=1 --max=5”
- 保证扩展基于`Deployments`而不是`ReplicaSets`
  > NOTE: 这个后面确认一下具体的原因
- container的cpu使用情况计算方式是`实际cpu使用情况 / cpu require数量`。所以会出现cpu使用率超过100%的情况。
- 自动扩展存在限制
  - 数量限制
    - 如果当前副本的数量多于2个， 则一次扩展时副本数量最多翻倍
    - 如果当前副本的数量小于等于2个，则一次扩展时副本最多扩展到4个
  - 频率限制
    - 每个扩展操作的间隔时间至少为3分钟
    - 每个缩减操作的间隔时间为5分钟
 
### 基于内存的扩展

基于内存的扩展，当pod的内存使用到达阈值时，k8s所做的是杀掉并重启应用，并期望新的应用的内存使用超过阈值。

如果新pod的内存使用依然高于阈值，k8s会再次杀掉pod并重新启动。

> 书上仅提到了这些。

确定合适的扩展指标很重要。合理的指标应该是当pod数量增加时，该指标可以线性的减少。

autoscaling的最低pod数量不应该等于0

## 纵向扩展pod

不常用，直接跳过。

## 横向扩展集群node

### 扩展node的流程
1. 当一个pod被新建，但现有的所有node都无法接受该pod时，满足扩展node的条件。
2. 检查所有可拿到的node type中是否有适合该pod的node。如果存在则选择（如果存在多个合适的node type，则从其中选择最合适的node）。
> 这里的`最合适`需要通过配置文件设置（TODO: 如何设置）；最坏的情况是从中任选一个。
3. 新node被创建，kubectl将该node注册到集群中。
4. pod被分配到改node上。

### 手动设置node状态
- `kubectl cordon <node>`: 手动设置一个node不再接受新pod，但该node上正在运行的pod不会被驱逐。
- `kubectl drain <node>`: 手动设置一个node不在接受新pod，并驱逐改node上正运行的pod。
