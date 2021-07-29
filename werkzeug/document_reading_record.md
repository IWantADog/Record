# document reading reacord

## Serving WSGI Applications

如何创建一个简单的内置server。

```py
from werkzeug.serving import run_simple
from myproject import make_app

app = make_app(...)
run_simple('localhost', 8080, app, use_reloader=True)
```

### Reloader

`reloader`监控web application的相关文件，但文件被修改时重启整个服务。

`werkzeug`支持两种`reloader`:
- `stat`: 默认配置，固定间隔检查文件的`mtime`（修改时间）。
- `watchdag`: 使用`filesystem event`，比`stat`更快。但需要`watchdog`依赖，推荐的办法是在配置文件中增加`Werkzeug[watchdog]`。如果`watchdag`已被安装，会自动使用；如果没有被安装，则默认使用`stat`。


## Testing WSGI Applications

没什么值得记录的

## Request / Response Objects

`request`本质是对`CGI environment`的包装，便于数据的访问和获取。

`response`其实就是一个`WSGI applicaiton`。

`request`对象的特性
- **不可修改**。默认是不可修改的，不过可以将不可修改的对象替换为可修改的对象进行修改。（// todo 如何操作）
- **线程不安全**。`request`被多个线程访问是需要使用`同步锁`。
- **无法pickle**。 `request`对象无法pickle。

`response`对象的特性
- **可修改**
- **可被pickle**。调用`freeze()`之后能被pickle和copy。
- Since Werkzeug 0.6 it’s safe to use the same response object for multiple WSGI responses. // todo 什么意思
- **能使用`copy.deepcopy()`**
- response是一个`WSGI application callable`。当传入`environ` & `start_response`调用`__call__()`时，会将`status`和`headers`传入`start_response`并且返回响应体。


request的常用属性
- args: url paramenter
- data: bytes对象
- get_data(): 读取请求缓存的数据，并将其转换为一个`bytes`对象。__使用时需要先验证数据的大小，避免系统内存耗尽。__
- get_json(): 将`data`数据转换为json。如果请求头中没有`application/json`，则返回`None`。
- json: `get_json`的别名。
- files: 通过`multiDict`存储所有的上传文件，每个上传的文件是一个`FileStorage` object。
	> 只有request method为`post` & `put` & `patch`，并且`<form>`中存在`enctype="multipart/form-data"`时，file才不为空。其他情况下，file都为空值。
- form: form paramenter。
- headers: http请求头
- stream: 对于没有指定类型的数据，会被存储到`stream`，是一个`BinaryIO`。只会返回数据一次。
	> 大多时候优先使用`data`。
- values: `args` & `form`的组合体
- cookies: 类`dict`结构

`response`对象常用属性
- set_cookies(): 修改cookies










## URL Routing

MapAdapter

MapAdapter.bind_to_environ(environ)

MapAdapter.match()

### Rule Format
`<converter(arguments):name>`

### Built-in Converters

`werkzeug`内置的转换器，也可以覆盖或是扩展转换器。

- werkzeug.routing.UnicodeConverter: string，不可包含`/`
- werkzeug.routing.PathConverter: 和string类型相识，可以包含`/`

