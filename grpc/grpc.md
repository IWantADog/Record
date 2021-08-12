# how to use grpc correctly

## 定义一个service

```pb
service ServiceName{
    // something methods
}
```

service method type:
- simple RPC: `rpc GetFeature(Point) returns (Feature) {}`
- response-streaming RPC: `rpc ListFeatures(Rectangle) returns (stream Feature) {}`
    > 关键是`strem`
- request-streaming RPC: `rpc RecordRoute(stream Point) returns (RouteSummary) {}`
- bidirectionally-streaming RPC: `rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}`

## install

根据proto生成`*_pb2.py`和`*_pb2_grpc.py`文件
```sh
pip install grpcio-tools

python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/route_guide.proto
```

`*_pb2.py`: 包含根据proto生成的数据类型的class。

`*_pb2_grpc.py`: 包含生成的`client`和`server` class。
- `*Stub`: 客户端连接到gPRC服务
- `*Servicer`: 定义远程服务的接口，实现功能时需要继承该接口
- `add_*Service_to_server`: 将定义的服务注册到`server`的方法

## 更新生成的client和server

### 更新server

```py
class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	add_GreeterServicer_to_server(Greeter(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	server.wait_for_termination()
```

需要注意的点：
- 在服务端实现功能时需要继承`server class`
- 继承的子类中定义同名的方法，并且方法的第一个位置参数是一个定义好的`protocol buffer class`对象。
- 对于一个`response-streaming`的RPC method，它需要通过一个**生成器**实现。
- 对于一个`request-streaming`的RPC method，传入的`request`是一个**可迭代对象**。
- 对于一个`Bidirectional-streaming`的RPC method，就是以上两者的综合。传入的request是一个的可迭代对象，并且将方法实现为一个`生成器`。
- 调用`server.start()`不会阻塞当前线程，一个新线程会被创建用来处理请求。也就是说，调用`server.start()`方法的线程不会处理请求。如果遇到需要阻塞当前线程的情况，可以调用`server.wait_for_termination()`阻塞主线程，直到server终止。

### 更新clinet

```py
def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)
    response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)
```

需要注意的点：
- 调用一个`request-stream method`时，需要传入一个`iterator`
- 调用一个`response-stream method`时，可以直接迭代返回值
- 调用一个异步method时，(很奇怪)
    ```py
    feature_future = stub.GetFeature.future(point)
    feature = feature_future.result()
    ```

## 问题
- grpc如何设置基于某种协议运行？
- 原生grpc与rock是如何组合运行的？

