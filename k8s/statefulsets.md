# StatefulSets

## 简介

- `StatefulSets`同时管理多个pod。每个pod都有特定的`hostname`，`ip`。每个pod拥有各自的存储空间。当pod出现故障时，新pod与旧pod完全相同（hostname，name等）。
- `StatefulSets`也能通过修改`desired replica count`来控制pod的数量。
- 和`ReplicaSets`相同，根据`pod template`创建pod。
- 创建的pod的name、hostname有规律可循，由`StatefulSets`的名字和序号构成(从0开始递增)。

## 相关的一些使用

### 使用headless service
使用`StatefulSet`时需要访问制定某个pod。这是可以使用`headless service`，这样就能pod的hostname访问到特定的pod。

### 增加和减少pod的数量
- 增加pod的数量时仅需要重新指定pod的数量即可。
- 新增pod时`StatefulSet`每次仅会创建一个pod，等到该pod成功创建并且成功运行后才会开始创建下一个pod。这样做的原因是避免多个pod同时启动，造成竞争条件。
- 减少pod的数量按照pod的名字，从序号较高的pod开始删除。不同于`ReplicaSet`从任意一个pod开始删除。
- 删除pod时，每次仅删除一个pod。并且当pod中有不健康的pod时，`StatefulSets`不会执行删除pod的操作，因为如果这个时候删除pod会同时失去两个pod，有可能造成数据的丢失。

### 为每个pod提供各自的存储空间
- 删除`StatefulSet`pod时，pod上绑定的`PersistentVolumeClaim`并不会被删除。因为`StatefulSet`是有状态的，所以数据并不会随pod一起消失。如果确定需要删除，则需要手动删除`PV`。
- 使用`StatefulSet`时如果减少了pod的数量，被删除pod对应的`pvc`在pod被删除之后并不会被删除。而且该`pvc`可以被新pod重新使用。


## 发现`StatefulSet`下所有的pod

### 关于DNS中的`SRV`记录

SRV记录通过`hostname`和`port`指向一个服务。

kubernetes创建`headless service`时，会同时创建多个`SRV`记录指向`service`后面的pod。

## 更新`StatefulSet`

使用`kubectl edit statefulset <name>`打开默认的编辑器，对文件进行修改。

对`StatefulSet`的修改类似于对`ReplicaSets`的修改，只会影响之后创建的pod。如果想要更新旧pod只能手动删除旧pod。
> 从1.7开始，kubernetes支持像`Deployments`那样更新pod，需要配置`spec.updateStrategy`字段。

## StatefulSets处理node异常

当一个node(worker)无法访问时，获取这个node(worker)上所有pod的状态会显示为`Unknown`。如果pod为`Unknown`状态的时间超过了1分钟（可配置）。pod的资源会被`master node`回收。之后当`kubectl`看到pod被标记为`deletion`后，才会开始中止node上的运行的pod。当worker上的kubectl中止pod后，会通知api server，整个流程结束。

对于永久无法重新连接的`worker`，唯一的处理方法就是手动删除指定的pod。之后pod会被重新创建。

