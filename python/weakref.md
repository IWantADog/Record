# about weakref

[weakref document](https://docs.python.org/3/library/weakref.html)

## 特点
- 软连接不会阻碍object被`garbage collection`回收；如果实际对象被回收，软连接则会返回`None`
- 可以注册`callback`函数，当实际对象`garbage collection`删除时，该回调函数会被调用。被调用时，该软连接将作为唯一的参数，被传入回调函数。
- 主要用途是`创建缓存`或`通过映射缓存大数据文件`
- `list` & `dict`不能直接作为软连接的对象。不过可以通过继承他们实现子类的方式。
- `tuple` & `int`不能作为软连接的对象，即使子类也不行。
  ```py
  class d_dict(dict):
      pass
  ```
- 如果使用了`__slots__`，同时想要使用`weakref`，`__slots__`中必须存在`__weakref__`。
