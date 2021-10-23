# core concepts

## RPC life cycle

### unary RPC

1. client调用stub的方法，server接受到client发送的metadata（其中包含`method name`、`deadline`）。
2. server可以执行一下动作（**可以通过配置信息修改**）：
    - 直接返回初始的metadata数据（并且必须在所有响应开始之前）
    - 等待request的请求信息
3. server执行业务逻辑，生成response。response和metadata（status code和message）一同返回给client
4. 如果status code是ok，则client接受返回的数据。

### server streaming RPC

`server streaming RPC`与`unary RPC`大致类似，除了返回的数据是`stream of message`，并且只有当所有的数据都发送完毕之后，才会发送metadata。

### client streaming RPC

`client streaming RPC`与`unary RPC`大致类似，除了请求的数据是`stream of message`，并且server的响应并不需要等到接受到所有的请求数据之后。

### bidirectional streaming RPC

`bidirectional streaming RPC`的调用的开始与client调用方法，并且server接受了client发送的metadata。而服务端可以选择先返回`初始的metadata`或在返回所有数据之后再返回。

client和server端的之间的流处理逻辑可以自定义。例如，server可以等待接受所有的数据之后再响应，或是server可以一边接受数据一边响应。

### Deadline/Timeout

- client可以设置timeout，如果超过给定的时间会抛出异常`DEADLINE_EXCEEDED`
- server可以查询一个特定的rpc是否超时，或者还剩多少时间超时。

### RPC termination

在rpc中，由于client和server对于方法是否调用成功的判断是相互独立的。例如，有可能server正确响应了请求，但在client端却超时了。也有可能server会在client发送完整数据之前响应。

### cancelling an RPC

在一个rpc的任何状态，client和server都可以任意终止rpc连接。并且终止之后，后续的逻辑就不会再被执行。

### Metadata
- grpc内部使用的字段
- 通过key-value的形式存储，可以是string或binary data

### channels

`channel`为client向server发送数据提供了一个connection(通过指定host和port)。

client通过channel连接server时可以提供额外的参数，以此控制grpc的行为（例如，信息压缩）。


TODO: 通读一遍，修改病句。