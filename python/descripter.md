# python descripter

https://docs.python.org/3/howto/descriptor.html

- `descripter`的实现动机是：当通过属性访问`class variables`时，可以自定义逻辑。
- 必须为`class variables`
- 必须实现`__get__` or `__set__` or `__delete__`方法
- TODO: 不要使用`descripter`存储数据，实际数据的存储还是应该存入`instance`
- 对于instance的属性搜索顺序
  1. `data descriptor`
  2. instance `__dict__`
  3. `non-data descriptor`
  4. class variables
  5. `__getattr__`


## `data descriptor`和`non-data descriptor`的区别

如果一个instance的`__dict__`中同时存在相同名字的`变量`和`data descriptor`，则`data descriptor`优先。

如果一个instance的`__dict__`中同时存在相同名字的`变量`和`non-data descriptor`，则优先使用`__dict__`

如果想要定义一个`只读 data-descriptor`，需同时定义`__get__` & `__set__`，但`__set__`可以仅抛出异常。

```py
class Descriptor_3:
    def __get__(self, instance, owner_class):
        return "get from non-data descriptor"

class Descriptor_4:
    def __get__(self, instance, owner_class):
        return instance._a
    def __set__(self, instance, value):
        instance._a = value

class Descriptor_5:
    def __get__(self, instance, owner_class):
        return "get from non-data descriptor"
    def __set__(self, instance, value):
        raise ValueError

class T1:
    t3 = Descriptor_3()
    t4 = Descriptor_4()
    t5 = Descriptor_5()
    def __init__(self) -> None:
        self._a = 1
```

## 关于`__set_name__`

- `__set_name__`的主要功能
  - **当在类中实例化一个`descriptor`时，获取分配给`descriptor`的变量名**。
- 传入参数`def __set_name__(self, owner, name)`
  - owner: `descriptor`位于的class
  - name: 实例化后分配的变量名
- 调用时机
  - 当一个类被创建时，`type` metaclass会扫描新class的dictionaey。如果存在`descripter`则会调用`__set_name__`。


## function and method

- `function`是一个`descripter`
- 每次通过`.`访问一个`function`，会触发`function.__get__`并则返回一个`method`，并将实例化的对象作为`function`的第一个参数返回。

```py
# 从官网上复制的例子，使用纯python实现的method和function。
# 对于理解method和function的功能有帮助
# 逻辑类似，但实际实现时，使用的是c
class MethodType:
    "Emulate PyMethod_Type in Objects/classobject.c"

    def __init__(self, func, obj):
        self.__func__ = func
        self.__self__ = obj

    def __call__(self, *args, **kwargs):
        func = self.__func__
        obj = self.__self__
        return func(obj, *args, **kwargs)

class Function:
    ...

    def __get__(self, obj, objtype=None):
        "Simulate func_descr_get() in Objects/funcobject.c"
        if obj is None:
            return self
        return MethodType(self, obj)
```