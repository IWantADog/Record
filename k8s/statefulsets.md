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
- 增加pod的数量时仅需要重新指定pod的数量即可
- 减少pod的数量按照pod的名字，从序号较高的pod开始删除。不同于`ReplicaSet`从任意一个pod开始删除。
- 删除pod时，每次仅删除一个pod。并且当pod中有不健康的pod时，`StatefulSets`不会执行删除pod的操作，因为如果这个时候删除pod会同时失去两个pod，有可能造成数据的丢失。

### 为每个pod提供各自的存储空间





