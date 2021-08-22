# configMap and Secret

存储配置信息

## 配置app的方式

- 传递命令行参数给容器

    kubernetes支持定义pod时覆盖传递给container的命令行参数。

    在docker中，`ENTRYPOINT`定义当容器启动时，需要执行的命令。`CMD`定义传递给`ENTRYPOINT`的参数。

    定义pod时可以通过`command`覆盖`ENTRYPOINT`，`args`覆盖`CMD`。 
  
- 设置环境变量
- 挂载文件系统

## 通过ConfigMap解耦配置文件

通过configMap可以在pod中通过`name`绑定配置文件，可以在不修改pod定义文件的前提下，修改pod使用的配置。

`configMap`支持直接从读取文件，以文件名作为key，文件内容作为value。`configMap`同时也支持一次读取多个文件，仅需把`--from-file`指向一个文件路径。

可以通过`envFrom`一次性导入所有环境变量，`prefix`可以用来设置环境变量的前缀（也可以不设置）。

- 当修改ConfigMap时，所有相关的`volume`都会自动更新。
> k8s通过文件链接来实现配置文件的自动更新。当ConfigMap更新后，k8s会将新的配置写入一个新的路径下，之后在修改文件连接到新路径。

## Secret

`Secret`和`ConfigMap`类似，都通过`key-value`结构存储数据。

为了保证`Secret`的安全，`Secret`仅会分配给需要使用的`node`，并且secret仅存储在内存中不会写入磁盘中。
> 使用secret的volume通过`in-memory filesystem`存储数据。

不过`Secret`和`ConfigMap`有一个不同点。通过`secret`存储的数据会使用`Base64`加密，并且`Secret`也可以存储二进制文件，而`ConfigMap`使用的是明文。

### stringData

`stringData`是一个`write-only`的特殊字段。使用时只能向该字段赋值。当通过`get -o yaml`读取文件时，`stringData`对应的字段不会显示，相应的字段会在`data`下显示并通过`Base64`进行编码。

### 相关命令

kubectl get secrets
