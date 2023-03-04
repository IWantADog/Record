# HTTP Introduction

## http verbs

GET (选择)：从服务器上获取一个具体的资源或者一个资源列表。

POST （创建）： 在服务器上创建一个新的资源。

PUT （更新）：以整体的方式更新服务器上的一个资源。

PATCH （更新）：只更新服务器上一个资源的一个属性。

DELETE （删除）：删除服务器上的一个资源。

还有两个不常用的HTTP动词：

HEAD ： 获取一个资源的元数据，如数据的哈希值或最后的更新时间。

OPTIONS：获取客户端能对资源做什么操作的信息。

## state code range

1xx范围的状态码是保留给底层HTTP功能使用的，并且估计在你的职业生涯里面也用不着手动发送这样一个状态码出来。

2xx范围的状态码是保留给成功消息使用的，你尽可能的确保服务器总发送这些状态码给用户。

3xx范围的状态码是保留给重定向用的。大多数的API不会太常使用这类状态码，但是在新的超媒体样式的API中会使用更多一些。

4xx范围的状态码是保留给客户端错误用的。例如，客户端提供了一些错误的数据或请求了不存在的内容。这些请求应该是幂等的，不会改变任何服务器的状态。

5xx范围的状态码是保留给服务器端错误用的。这些错误常常是从底层的函数抛出来的，并且开发人员也通常没法处理。发送这类状态码的目的是确保客户端能得到一些响应。收到5xx响应后，客户端没办法知道服务器端的状态，所以这类状态码是要尽可能的避免

### 常用状态码

#### 200 OK – [GET]

The Consumer requested data from the Server, and the Server found it for them (Idempotent)

客户端向服务器请求数据，服务器成功找到它们

#### 201 CREATED – [POST/PUT/PATCH]

The Consumer gave the Server data, and the Server created a resource

客户端向服务器提供数据，服务器根据要求创建了一个资源

#### 204 NO CONTENT – [DELETE]

The Consumer asked the Server to delete a Resource, and the Server deleted it

客户端要求服务器删除一个资源，服务器删除成功

#### 301 Move Permanently

The URL of the requested resource has been changed permanently. The new URL is given in the response.

#### 302 Found

This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests.

#### 304 Not Modified (未修改)

当使用HTTP缓存头信息时使用304

#### 400 INVALID REQUEST – [POST/PUT/PATCH]

The Consumer gave bad data to the Server, and the Server did nothing with it (Idempotent)

客户端向服务器提供了不正确的数据，服务器什么也没做

#### 401 Unauthorized

No authentication credentials provided or authentication failed

没有认证或认证失败

#### 403 Forbidden

Authenticated user does not have access

对于访问的资源没有权限

#### 404 NOT FOUND – [*]

The Consumer referenced an inexistant Resource or Collection, and the Server did nothing (Idempotent)

客户端引用了一个不存在的资源或集合，服务器什么也没做

#### 405 Method Not Allowed (方法被禁止)

当一个对认证用户禁止的HTTP方法被请求时

#### 410 Gone (已删除)

表示资源在终端不再可用。当访问老版本API时，作为一个通用响应很有用

#### 415 Unsupported Media Type (不支持的媒体类型)

如果请求中包含了不正确的内容类型

#### 422 Unprocessable Entity (无法处理的实体)

出现验证错误时使用

#### 429 Too Many Requests (请求过多)

当请求由于访问速率限制而被拒绝时

#### 500 INTERNAL SERVER ERROR – [*]

The Server encountered an error, and the Consumer has no knowledge if the request was successful

服务器发生内部错误，客户端无法得知结果，即便请求已经处理成功

[w3c http status codes](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

## headers

[X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)

## caches

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Caching_FAQ

## CORS

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS#

## negotiation

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Content_negotiation

## xss

https://stackoverflow.com/questions/239194/how-does-xss-work