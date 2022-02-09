# pod resource request and limit

## request/limit对pod被schedule的影响
- LeastRequestedPriority: 优先选择空闲资源较多的node
- MostRequestedPriority: 优先选择空闲资源较少的node，是node上的pod更紧凑，减少node数量
- scheduler向node分配pod时，主要关注的是所有pod`request`的cpu和memory总和，而不是实际使用的memory和cpu。
- 一个node上的所有pod的cpu/memory limit可以超过该node实际拥有的资源。

需要注意cpu/memory在limit上差异

- 当一个pod的cpu limit设置后，pod的cpu使用不会超过limit
- 当一个pod的memory limit设置后，当pod实际使用的memory超过limit，pod会报`Out Of Memory（OOM）`异常。

limit/request对于cpu和memory
- 当一个container的cpu被限制，实际限制的是该container在运行的node上的整个cpu时间。

  例如：一个container的cpu limit为1cpu，运行在一个16core的node上。则该container实际的cpu运行时间为整个cpu时间的十六份之一。并且该container并不一直运行在单一cpu，而是可能在不同的cpu之间切换运行。

- 当一个container的memory被限制，并不是该container只能访问到这些memory。如果使用top命令，实际获取的是当前node的整个memeory使用情况。

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

pass










