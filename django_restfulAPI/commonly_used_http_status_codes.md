# 常用http状态码

[Http Status Code Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

## 请求成功

- 200 OK : 请求执行成功并返回相应数据，如 GET 成功
- 201 Created : 对象创建成功并返回相应资源数据，如 POST 成功；创建完成后响应头中应该携带头标 Location ，指向新建资源的地址
- 202 Accepted : 接受请求，但无法立即完成创建行为，比如其中涉及到一个需要花费若干小时才能完成的任务。返回的实体中应该包含当前状态的信息，以及指向处理状态监视器或状态预测的指针，以便客户端能够获取最新状态。
- 204 No Content : 请求执行成功，不返回相应资源数据，如 PATCH ， DELETE 成功

## 重定向

重定向的新地址都需要在响应头 Location 中返回

- 301 Moved Permanently : 被请求的资源已永久移动到新位置
- 302 Found : 请求的资源现在临时从不同的 URI 响应请求
- 303 See Other : 对应当前请求的响应可以在另一个 URI 上被找到，客户端应该使用 GET 方法进行请求。比如在创建已经被创建的资源时，可以返回 303
- 307 Temporary Redirect : 对应当前请求的响应可以在另一个 URI 上被找到，客户端应该保持原有的请求方法进行请求

## 条件请求

- 304 Not Modified : 资源自从上次请求后没有再次发生变化，主要使用场景在于实现数据缓存
- 409 Conflict : 请求操作和资源的当前状态存在冲突。主要使用场景在于实现并发控制
- 412 Precondition Failed : 服务器在验证在请求的头字段中给出先决条件时，没能满足其中的一个或多个。主要使用场景在于实现并发控制

## 客户端错误

- 400 Bad Request : 请求体包含语法错误
- 401 Unauthorized : 需要验证用户身份，如果服务器就算是身份验证后也不允许客户访问资源，应该响应 403 Forbidden 。如果请求里有 Authorization 头，那么必须返回一个 WWW-Authenticate 头
- 403 Forbidden : 服务器拒绝执行
- 404 Not Found : 找不到目标资源
- 405 Method Not Allowed : 不允许执行目标方法，响应中应该带有 Allow 头，内容为对该资源有效的 HTTP 方法
- 406 Not Acceptable : 服务器不支持客户端请求的内容格式，但响应里会包含服务端能够给出的格式的数据，并在 Content-Type 中声明格式名称
- 410 Gone : 被请求的资源已被删除，只有在确定了这种情况是永久性的时候才可以使用，否则建议使用 404 Not Found
- 413 Payload Too Large : POST 或者 PUT 请求的消息实体过大
- 415 Unsupported Media Type : 服务器不支持请求中提交的数据的格式
- 422 Unprocessable Entity : 请求格式正确，但是由于含有语义错误，无法响应
- 428 Precondition Required : 要求先决条件，如果想要请求能成功必须满足一些预设的条件

## 服务端错误

- 500 Internal Server Error : 服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。
- 501 Not Implemented : 服务器不支持当前请求所需要的某个功能。
- 502 Bad Gateway : 作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应。
- 503 Service Unavailable : 由于临时的服务器维护或者过载，服务器当前无法处理请求。这个状况是临时的，并且将在一段时间以后恢复。如果能够预计延迟时间，那么响应中可以包含一个 Retry-After 头用以标明这个延迟时间（内容可以为数字，单位为秒；或者是一个 HTTP 协议指定的时间格式）。如果没有给出这个 Retry-After 信息，那么客户端应当以处理 500 响应的方式处理它。
- 501 与 405 的区别是：405 是表示服务端不允许客户端这么做，501 是表示客户端或许可以这么做，但服务端还没有实现这个功能