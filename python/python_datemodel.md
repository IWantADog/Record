# python datemodel

[offical document](https://docs.python.org/3/reference/datamodel.html)

## __new__ and __init__

> `__new__()` to create it, and `__init__()` to customize it.

> So in our example, `x.f` is a valid method reference, since `MyClass.f` is a function, but `x.i` is not, since `MyClass.i` is not. But `x.f` is not the same thing as `MyClass.f` — it is a `method object`, not a `function object`.

> the special thing about methods is that the instance object is passed as the first argument of the function. In our example, the call `x.f()` is exactly equivalent to `MyClass.f(x)`. In general, calling a method with a list of n arguments is equivalent to calling the corresponding function with an argument list that is created by inserting the method’s instance object before the first argument.

[进度](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access)

## __slots__
TODO: 记录一下

## Customizing class creation

### object.__init_subclass__(cls)

1. 当存在`__init__subclass__`方法的`class`被继承是，`__init__subclass__`就会被调用。
2. 传入的`cls`是新定义的子类。
3. 需要是`classmethod`。如果定义时没有显式指定为`classmethod`，会将其隐式的转换为`classmethod`。
4. 默认的`object.__init_subclass__`什么都不做。但如果传入了若干参数并被调用会抛出异常。

> TODO: 想不出什么时候应该调用这个方法？什么场景需要使用这个方法？

### metaclasses

```py
class Meta(type):
	pass

class MyClass(metaclass=Meta, first=1, second="this is second")
	pass
```

当使用`metaclass`时，所有其他的传入的`kwargs`参数会被直接向下传递。

When a class definition is executed, the following steps occur:

- MRO entries are resolved;(确定MRO)
- the appropriate metaclass is determined;(确定合适的`metaclass`)
- the class namespace is prepared;(TODO: class namespace是什么东西)
- the class body is executed;(执行class body)
- the class object is created.(`class`对象被创建)

#### resolving MRO entries

TODO: 什么意思

#### Determining the appropriate metaclass
确定合适的`metaclass`
- 如果`metaclass`没有显示指定，则使用`type()`
- 如果显式指定`metaclass`当它不是一个`type()`的`instance`，则直接将其作为`metaclass`。
- 如果一个`type()`的`instance`被显式指定为`metaclass`，或者基类被指定，则使用最近的`metaclass`。

TODO: `type instance`具体指什么？指的是class吗？

## about type

当使用`type(object)`时返回`object`的类型信息。类似于`object.__class__`。

当使用`tyep(name, bases: tuple, dict, **kwds)`时，创建一个新的`type object`。这是一种动态创建`class`的声明方式。
- `name`作为`__name__`。
- `bases`作为`__bases__`。如果bases为空tuple，则`object`被加入。
- `dict`作为`__dict__`。
- `kwds`

## reference

https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/

https://docs.python.org/3/reference/datamodel.html#customizing-class-creation