# About gunicorn

https://docs.gunicorn.org/en/latest/index.html

TODO: `gunicorn`的相关内容需要单独新建一个文件记录，现在放在这里只是方便。
    - 先这样吧，gunicorn相关的内容就这些。暂时先不动了。

画了一个uml图放在upload/gunicorn.mdj。（可能用得上）

## running gunicorn

```sh
$ gunicorn [OPTIONS] [WSGI_APP]
```

`WSGI_APP`是形如`${MODULE_NAME}:{VARIABLE_NAME}`的形式。`MODULE_NAME`是模块的路径，`VARIABLE_NAME`是模块中的一个可调用变量。

一些示例
```
$ gunicorn --workers=2 test:app

$ gunicorn --workers=2 'test:create_app()'
```

## 有用的一些记录

命令行启动入口: `gunicorn.app.wsgiapp.run`

没明白的地方
- gunicorn为什么仅仅导入了`wsgi application`而没有存储它的引用。这样做的目的是在作用域中添加`wsgi applicaiton`的实例吗？

对于worker的猜想
- 每个worker都有一个flask applicaiton？[ok]