# pod resource request and limit

## 理解cpu/memory request对pod分配的影响
- request仅表明一个pod需要使用cpu/memory的最小值
- 实际pod对cpu/memory资源的使用可以小于或大于request的值
- 当向一个node上分配pod时，scheduler会计算node上剩余未被使用的资源，计算的方式是：`node总资源 - 该node上所有pod request的资源总和`。如果未被分配的资源小于request的资源，则pod不会被分配到该node上。（scheduler并不关心，node上所有pod实际使用的资源情况）
- pod被scheduler分配时可以设置的属性
  - LeastRequestedPriority: 优先选择空闲资源较多的node
  - MostRequestedPriority: 优先选择空闲资源较少的node，使node上的pod更紧凑，减少node数量
- pod cpu request不仅影响pod被分配，也同时影响所有pod在cpu时间上的共享
  - 当node上的cpu时间**有剩余时（即all > request）**，剩余cpu时间会按照每个pod的request等比例分配。但如果其他container都处于空闲状态，某个container可以用满所有的cpu。
  > 需要注意这些情况发生在cpu有剩余时间时，如果cpu已被用满，则新pod会一直处于pending状态。

## 限制container对资源的使用

- 一个node上的所有pod的cpu/memory limit可以超过该node实际拥有的资源(和require不同)。当node上的实际使用的资源，超过了拥有的资源，某些container会被kill。

- 需要注意cpu/memory在limit上差异
  - 当一个pod的cpu limit设置后，pod的cpu使用不会超过limit
  - 当一个pod的memory limit设置后，当pod实际使用的memory超过limit，pod会报`Out Of Memory（OOM）`异常，并被kill。

limit/request对于cpu和memory
- 当一个container的cpu被限制，实际限制的是该container在运行的node上的整个cpu时间。

  例如：一个container的cpu limit为1cpu，运行在一个16core的node上。则该container实际的cpu运行时间为整个cpu时间的十六份之一。并且该container并不一直运行在单一cpu，而是可能在不同的cpu之间切换运行。

- 当一个container的memory被限制，并不是该container只能访问到这些memory。如果在该container内部使用top命令，实际获取的是当前node的整个memeory使用情况。

  这也意味着，如果应用基于内存或cpu核数触发一些行为。结果可能和预想的有差别。

## Quality of Service(QoS)
- BestEffort(the lowest priority)
- Burstable
- Guaranteed(the highest)

QoS是pod的一种属性，表明当node资源不足pod被清除的优先级。

`BestEffort`:一个pod的所有container都没有设置request和limit
`Guaranteed`: 一个pod的所有container都设置了limit和request，并且limit和request相等。
`Burstable`: 不属于BestEffort和Guaranteed的其他所有。

当资源不足时被kill的顺序，BestEffort先于Burst·able，Burstable先于Guaranteed。

对于相同优先级的pod，k8s会计算一个`OOM score`。`OOM score`越高优先被删除。(这里OOM score的计算逻辑不详述）

## LimitRange

`LimitRange`是k8s的一种资源，用于为pod/container/PVC设置资源的min/max/default。需要注意`LimitRange`作用于一个namespace下的所有的单个pod/container/pvc。

## ResourceQuota

作用于一个namespace，
- 限制cpu/memory/disk资源的使用量
- 限制pod/service等其他资源的数量

当定义`ResourceQuota`资源之后，无法再创建未显示声明limit和request的pod

## 监控pod资源使用情况

cAdvisor & Heapster

cAdvisor搜集单个node上所有pod的资源使用情况，Heapster向集群中的每个node上的cAdvisor搜集数据并聚合。

可以通过`InfluxDB and Grafana`收集并可视化数据。
