# about Deployments



通常对镜像做了修改但不修改tag直接发布是不合适的。如果k8s的配置文件中使用的tag为`latest`，k8s拉取镜像去不会造成影响。但如果为其他tag，则可能出现问题。因为当一个镜像的特定tag版本被拉取后，会被存储到`node`上，k8s就不会在拉取相同版本的景象了。这就意味着k8s使用的可能是过时的镜像。

当使用特定的tag时需要手动设置合理的拉取策略`imagePullPolicy`。
> 当tag为latest时`imagePullPolicy`默认为`Always`，而tag为其他时`imagePullPolicy`默认为`ifNotPresent`

## update applications declaratively

`Deployments`属于高层级资源，主要用于通过声明式部署和更新application。与`Deployments`相比`ReplicationController`和`ReplicaSet`属于低层级资源。

当使用`Deployments`时，实际创建和管理pod还是通过`ReplicaSets`实现。
> 创建deployments时通过`--record`记录命令

## 更新Deployment

使用`Deployment`时，如果想要更新一个app，仅需要修改pod模版，kubernetes会处理好后续的其他事情。
> 使用`Deployment`时，更新容器版本结束后，原有的`ReplicaSet`不会被删除。

### understanding the available deployment strategies

- RollingUpdate

    默认策略。简单点讲，就是删除一个旧pod后增加一个新pod，直到新pod替换所有就pod，保证不会有请求被丢弃。

- Recreate

    删除所有的旧版本pod，之后创建新pod。

### about `minReadySeconds`

### about modify resources

- `kubectl edit`: 使用默认的编辑器打开manifest，保存后生效。
- `kubectl patch`: 修改单一属性时使用。
- `kubectl apply`: 使用yaml和json更新文件
- `kubectl replace`: 使用新文件替换旧文件
- `kubectl set image`: 更新定义的容器

### roll back a deployment

`kubectl rollout undo deployment kubia`

当一次发布完成之后，旧的`ReplicaSet`最终不会被删除，这就使得app可以被回滚到任意版本。版本历史可以通过`kubectl rollout history`查询。为了保证直观的发布历史，需要在使用`--record`命令。

回滚支持回滚到任意版本，`kubectl rollout undo deployment kubia --to-revision=1`。

可以通过在`Deployment`的定义中设置`revisionHistoryLimit`来限制保存的回滚版本数量。

### `maxSurge` & `maxUnavailable`

`maxSurge`和`maxUnavailable`是`rollingUpdate`的子属性。这两个属性可以用来设置当发布时一次有多少个pod被替换。

- maxSurge: 决定某一时刻最多有`desired + maxSurge`个pod存在
- maxUnavailable: 决定某一时刻必须有`desired - maxUnavailable`个容器可以访问。

### blocking rollout of bad version

- minReadySeconds: 决定当一个新创建的pod正常运行多久后才能被视为`available`。当一个pod被视为`available`之后，`rollout process`才能继续执行，创建下一个新pod。

使用`readiness probe`和`minReadySeconds`的组合可以有效的阻止有问题的版本被发布。

## tips

kubectl rollout status deployment kubia




