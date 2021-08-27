# Python Web Server Gateway Interface

## wsgi

[PEP-3333](https://www.python.org/dev/peps/pep-3333/)

https://wsgi.readthedocs.io/en/latest/

http://wsgi.tutorial.codepoint.net/application-interface

http://ivory.idyll.org/articles/wsgi-intro/what-is-wsgi.html

### 基本

牢记的几点

1. wsgi不是一个框架、一个python模块、一个服务器、一个API接口、或是软件应用。wsgi只是一种接口规范，关于server与application通讯的接口规范。如果application是按照wsgi编写的，该application就能在所有支持wsgi的server上运行。

2. wsgi分为server侧和application侧。server侧需要调用一个application侧提供的可调用对象。

3. wsgi application能够被叠放，在叠放的applicaion之间需要中间层(middleware)。中间层必须在两侧都实现wsgi规范。

4. wsgi server的工作仅是接受client的请求，再将其发送给application，最后将application的回应返回给client。其他的具体操作由application和middleware完成。

### wsgi application interface

1. wsgi application interface需要被实现为一个可调用对象，如一个方法、一个对象、或是一个含有`__call__()`的实例。

2. wsgi application interface的输入和输出
    - 输入：
        1. 存放[CGI](https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E7%BD%91%E5%85%B3%E6%8E%A5%E5%8F%A3)变量的dictionary
        2. 一个可调用方法，用于返回http状态码和状态头
            - 返回的状态头中`body length`必须是返回体中所有s字符串的总长度。

    - 输出：返回一个被包装在可迭代对象中的string作为响应体
        - 返回值的字符串需要使用`[]`包围。不然对于旧机器会迭代这个字符串，将整个字符串拆分为单个字节返回给客户端。

## Werkzeug

[Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)

Werkzeug不是一个框架。它是一个工具库，用途是帮助python web框架或web applicaiton作者实现wsgi。

## what middleware can do

- Handle web application errors
- Provide session support
- Profile your web application
- Deal with Login authentication
- and Gzip the output

## Reference

https://lucumr.pocoo.org/2007/5/21/getting-started-with-wsgi/
