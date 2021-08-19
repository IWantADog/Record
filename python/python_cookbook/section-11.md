# python cookbook section 11

## http客户端
- request
- urllib

## 创建一个tcp/udp服务器
- socketserver

## 解析ip地址，子网掩码

- ipaddress

## 简单xml-rpc
- `from xmlrpc.server import SimpleXMLRPCServer`
> `SimpleXMLRPCServer`是单线程的，所以性能是他的缺点。如果需要快速构建一个简单的rpc服务，它是值得学习的。

## python多个解释器之间的通信

- multiprocessing.connection.Listtener
- multiprocessing.connection.Client

跟底层socket不同的是，每个消息会完整保存（每一个通过send()发送的对象能通过recv()来完整接受）。 另外，所有对象会通过pickle序列化。因此，任何兼容pickle的对象都能在此连接上面被发送和接受。

一个通用准则是，你不要使用 multiprocessing 来实现一个对外的公共服务。 Client() 和 Listener() 中的 authkey 参数用来认证发起连接的终端用户。 如果密钥不对会产生一个异常。此外，该模块最适合用来建立长连接（而不是大量的短连接），例如，两个解释器之间启动后就开始建立连接并在处理某个问题过程中会一直保持连接状态。

## 实现远程调用实现

客户端将调用的方法、数据序列化后通过网络协议发送，服务器端反序列化数据得到方法和参数。之后调用相应的方法，并将产生的数据通过序列化并通过网络协议发送给客户端。

## 简单的客户端认证

`hmac`认证的一个常见使用场景是内部消息通信系统和进程间通信。例如，如果你编写的系统涉及到一个集群中多个处理器之间的通信，你可以使用本节方案来确保只有被允许的进程之间才能彼此通信。事实上，基于`hmac`的认证被 `multiprocessing`模块使用来实现子进程直接的通信。

还有一点需要强调的是连接认证和加密是两码事。 认证成功之后的通信消息是以明文形式发送的，任何人只要想监听这个连接线路都能看到消息（尽管双方的密钥不会被传输）。

## 看不懂，直接跳过

11.11 进程间传递Socket文件描述符

11.12 立即事件驱动的IO

11.13 发送和接受大型数组