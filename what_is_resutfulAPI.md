# how to develop restful api gracefully

[Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)

[Hypertext Transfer Protocol -- HTTP/1.1](https://www.w3.org/Protocols/rfc2616/rfc2616.html)

[What is the “N+1 selects problem” in ORM (Object-Relational Mapping)?](https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem-in-orm-object-relational-mapping)

[URIs, Addressability, and the use of HTTP GET and POST](https://www.w3.org/2001/tag/doc/whenToUseGet.html)

[Rest API CookBook](https://restcookbook.com/)

## Restful API 核心

1. http status codes、http action、http header。
2. 支持数据分页、排序、筛选、过滤。
3. 支持通过json完成POST、PUT、PATCH
4. 版本化应对模型、逻辑变化。
5. 使用名称复数描述资源，通过 http actions 操作资源。
6. https
7. OAuth2

## 幂等性

请注意，这里强调的是一次和N次具有相同的`副作用`，`而不是每次GET的结果相同`。

https://www.cnblogs.com/weidagang2046/archive/2011/06/04/2063696.html

## Data Design and Abstraction

有时候一个集合可以表达一个数据库表，而一个资源可以表达成里面的一行记录，但是这并不是常态。事实上，你的API应该尽可能 __通过抽象来分离数据与业务逻辑__。

## Verbs

- `GET` (SELECT): Retrieve a specific Resource from the Server, or a listing of Resources.
- `POST` (CREATE): Create a new Resource on the Server.
- `PUT` (UPDATE): Update a Resource on the Server, providing the entire Resource.
- `PATCH` (UPDATE): Update a Resource on the Server, providing only changed attributes.
- `DELETE` (DELETE): Remove a Resource from the Server.
- `HEAD` – Retrieve meta data about a Resource, such as a hash of the data or when it was last updated.
- `OPTIONS` – Retrieve information about what the Consumer is allowed to do with the Resource.

## Versioning - 版本化

应用和应用的数据关系终会发生变化，资源上的属性会被增加或删除。

__为了应对变化，一个好的RESTful API会在URL中包含版本信息。__ 另一种比较常见的方案是在请求头里面保持版本信息。但是跟很多不同的第三方开发者一起工作后，我可以很明确的告诉你，在请求头里面包含版本信息远没有放在URL里面来的容易。

## Analytics

对接口调用进行分析。为每一个接口分配一个uuid，通过`Request-Id`存储，便于对接口的使用进行调试、分析。

## API ROOT URL

这里有两个常见的URL根例子：

- https://example.org/api/v1/*
- https://api.example.com/v1/*

如果你的应用很庞大或者你预期它将会变的很庞大，那么`将API放到子域(e.g. api.)`下通常是一个好选择。这种做法可以保持某些规模化上的灵活性。

但如果你觉得你的API不会变的很庞大，或是你只是想让应用安装更简单些（如你想用相同的框架来支持站点和API），`将API放到根域名下(e.g. /api/)`也是可以的。

让API根拥有一些内容通常也是个好主意。Github的API根就是一个典型的例子。

同样也请注意HTTPS前缀，一个好的RESTful API总是基于HTTPS来发布的。

## Endpoints

1. 复数名称
2. http动词
3. 注意一对多和多对多关系，正确处理资源之间的关系。但同时防止路径嵌套过多。过深的导航容易导致url膨胀，不易维护，如 `GET /zoos/1/areas/3/animals/4`，尽量使用查询参数代替路径中的实体导航，如`GET /animals?zoo=1&area=3`


```
/orgs/{org_id}/apps/{app_id}/dynos/{dyno_id}
```

### 示例

- GET `/zoos/ZID/employees`: Retrieve a listing of Employees (ID and Name) who work at this Zoo
- POST `/employees`: Create a new Employee
- POST `/zoos/ZID/employees`: Hire an Employee at a specific Zoo
- DELETE `/zoos/ZID/employees/EID`: Fire an Employee from a specific Zoo

## Filtering

1. 提供合理的过滤字段
2. 不对过滤增加额外的限制
3. 对于复杂的查询可以设置简单、常用的别名

## Status Codes

`1xx`__范围的状态码是保留给底层HTTP功能使用的，并且估计在你的职业生涯里面也用不着手动发送这样一个状态码出来。__

`2xx`__范围的状态码是保留给成功消息使用的，你尽可能的确保服务器总发送这些状态码给用户。__

`3xx`__范围的状态码是保留给重定向用的。__ 大多数的API不会太常使用这类状态码，但是在新的超媒体样式的API中会使用更多一些。

`4xx`__范围的状态码是保留给客户端错误用的。__ 例如，客户端提供了一些错误的数据或请求了不存在的内容。这些请求应该是幂等的，不会改变任何服务器的状态。

`5xx`__范围的状态码是保留给服务器端错误用的。__ 这些错误常常是从底层的函数抛出来的，并且开发人员也通常没法处理。发送这类状态码的目的是确保客户端能得到一些响应。收到5xx响应后，客户端没办法知道服务器端的状态，所以这类状态码是要尽可能的避免

## Expected Return Documents

下面的列表是非常经典的RESTful API定义：

- GET /collection: 返回一系列资源对象
- GET /collection/resource: 返回单独的资源对象
- POST /collection: 返回新创建的资源对象
- PUT /collection/resource: 返回完整的资源对象
- PATCH /collection/resource: 返回完整的资源对象
- DELETE /collection/resource: 返回一个空文档

选择参数返回功能，仅返回用户指定的参数。

创建和更新后需返回一个资源描述。包含一个201状态码和一个`location headerr`指向新创建的资源。

## Authentication

[OAuth 2.0](https://tools.ietf.org/html/rfc6749)

1. 总是使用ssl
2. 使用`OAuth2.0`产生令牌并传递给第三方
3. 因为JSONP请求不能发送HTTP基本认证凭据(HTTP Basic Auth)或承载令牌(Bearer tokens)。这种情况下，可以使用一个特殊的查询参数`access_token`。注意，使用查询参数`token`存在着一个固有的安全问题，即大多数的web服务器都会把查询参数记录到服务日志中。

## Content Type

将响应类型放在响应头中

## 实践经验

虽然内部Model可以简单地映射到资源上，但那不一定是个一对一的映射。__这里的关键是不要泄漏与API不相关的实现细节。__

利用现有的 HTTP 方法在单个的 /tickets 接入点上实现了显著的功能。没有什么方法命名约定需要去遵循，URL 结构是整洁干净的

某种关系不依赖于资源，那么在资源的输出表示中只包含一个标识符是有意义的。API消费者然后除了请求资源所在的接入点外，还得再请求一次关系所在的接入点。但是如果一般情况关系和资源一起被请求，API可以提供自动嵌套关系表示到资源表示中，这样可以防止两次请求API

#### 如果Action不符合CRUD操作那该怎么办？

- 重新构造这个Action，使得它像一个资源的field（我理解为部分域或者部分字段）。这种方法在Action不包含参数的情况下可以奏效。例如一个有效的action可以映射成布尔类型field，并且可以通过PATCH更新资源。
- __利用RESTful原则像处理子资源一样处理它。__ 例如，Github的API让你通过PUT`/gists/:id/star` 来 star a gist ，而通过DELETE`/gists/:id/star`来进行 unstar 。
- 有时候你实在是没有办法将Action映射到任何有意义的RESTful结构。例如，__多资源搜索没办法真正地映射到任何一个资源接入点。__ 这种情况，`/search` 将非常有意义，虽然它不是一个名词。这样做没有问题 - 你只需要从API消费者的角度做正确的事，并确保所做的一切都用文档清晰记录下来了以避免（API消费者的）困惑。

### 只返回JSON

当不得不支持`xml`时，媒体类型是应该基于`Accept`头还是基于URL呢？。为确保浏览器的浏览性，应该基于URL。这里最明智的选择是在端点URL后面附加`.json`或`.xml`的扩展.

### 缺省情况下确保漂亮的打印和支持gzip

使用漂亮打印的json带来的开销是值得的。

可以通过url中的parameter或`Accept`请求头设置是否漂亮打印漂亮json

启用gzip后节省的带宽是可观的。

### 不要默认使用大括号封装，但要在需要的时候支持

不理解。

### 使用JSON 编码的 POST, PUT & PATCH 请求体

一个能接受JSON编码的`POST`,`PUT`和`PATCH`请求的API，应当也需要把`Content-Type`头信息设置为`application/json`，或者抛出一个`415`不支持的媒体类型（Unsupported Media Type）的HTTP状态码。

### 分页

[RFC 5988 中介绍的链接标头](https://tools.ietf.org/html/rfc5988#page-6)

### 重写/覆盖 HTTP 方法

一些HTTP客户端仅能处理简单的的`GET`和`POST`请求，为照顾这些功能有限的客户端，API需要一种方式来重写HTTP方法. 尽管没有一些硬性标准来做这事，但流行的惯例是接受一种叫`X-HTTP`的请求头，重写是用一个字符串值包含PUT，PATCH或DELETE中的一个。

__注意重写头应当仅接受POST请求，GET请求绝不应该 更改服务器上的数据!__

### 速率限制

为了防止滥用，标准的做法是给API增加某种类型的速率限制。`RFC 6585`中介绍了一个HTTP状态码`429`请求过多来实现这一点。

不论怎样，在用户实际受到限制之前告知他们限制的存在是很有用的。这是一个现在还缺乏标准的领域，但是已经有了一些流行的使用HTTP响应头信息的惯用方法。

最少时包含下列头信息(使用Twitter的命名约定 来作为头信息，通常没有中间词的大写):

- `X-Rate-Limit-Limit` - 当期允许请求的次数
- `X-Rate-Limit-Remaining` - 当期剩余的请求次数
- `X-Rate-Limit-Reset` - 当期剩余的秒数

### 缓存

HTTP 提供了一套内置的缓存框架!

有两种方式: [ETag](https://en.wikipedia.org/wiki/HTTP_ETag)和[Last-Modified](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.29)

### 错误

一个JSON格式的错误信息体应当为开发者提供几样东西 - 一个有用的错误信息，一个唯一的错误代码 (能够用来在文档中查询详细的错误信息) 和可能的详细描述。

```json
{
  "code" : 1234,
  "message" : "Something bad happened :(",
  "description" : "More details about the error here"
}
```

### 为每个资源提供uuid

全局唯一，对于所有资源唯一。

### 使用UTC时间和ISO8601时间格式

### 直接返回数据，不需要额外包装