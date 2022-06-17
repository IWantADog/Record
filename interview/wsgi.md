# about wsgi

## wsgi

1. wsgi不是一个框架、一个python模块、一个服务器、一个API接口、或是软件应用。wsgi只是一种接口规范，关于server与application通讯的接口规范。如果application是按照wsgi编写的，该application就能在所有支持wsgi的server上运行。

2. wsgi分为server侧和application侧。server侧需要调用一个application侧提供的可调用对象。

3. wsgi application能够被叠放，在叠放的applicaion之间需要中间层(middleware)。中间层必须在两侧都实现wsgi规范。

4. wsgi server的工作仅是接受client的请求，再将其发送给application，最后将application的回应返回给client。其他的具体操作由application和middleware完成。

常用的uwsgi server

- uWSGI

    `uwsgi (all lowercase)` is the native binary protocol that `uWSGI` uses to communicate with other servers.

    `uWSGI` is often used for serving Python web applications in conjunction with web servers such as `Cherokee` and `Nginx`, which offer direct support for `uWSGI's` native uwsgi protocol.For example, data may flow like this: `HTTP client ↔ Nginx ↔ uWSGI ↔ Python app.`

- gunicorn
    pass

## 一个请求从进入http server到django经历了什么。django的请求的生命周期

客户端请求 - 》 http server（nginx）-》 wsgi server -》 middler -》 django路由选择 -》 http响应