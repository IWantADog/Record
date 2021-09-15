# python datemodel

[offical document](https://docs.python.org/3/reference/datamodel.html)

TODO: 感觉需要再读几遍

## Objects, values and types
- 每个对象都有`identity`、`type`、`value`。一个对象被创建之后`identity`不会被改变，可以认为`identity`是对象在内存中的位置。
- 当使用`is`时比较的就是两个对象的`identity`。可以使用`id()`获取一个对象的`identity`。
- 对于`immutable`如果`value`相同则可能是同一对象。而对于`mutable`即使`value`相同也不可能是同一对象。

## The standard type hierarchy

- `function`和`instance methods`都是可调用对象。
- 区分清楚`function`和`instance methods`

	```py
	class A:
		def func(self):
			pass

	a = A()
	```
	- 区分清楚`A.func`和`a.func`。`A.func`是一个`function`，`a.func`是一个`methods`
	- `methods`中包含了`class`、`class instance`和一个`callable object`(通常是一个user-defined function)。
		- `__self__`存储`class instance`。对于`class methods`，`__self__`存储的是`class`。
		- `__func__`存储实际的`function`
	- 理解`A.func(a)`等价与`a.func()`。
- classes instance
	- 类属性存储在`__dict__`中。在当前类找不到相应的属性时会向父类寻找。
	- 实例属性的搜索路径
		1. instance的`__dict__`
		2. class的`__dict__`
			- 如果搜索的属性是`user-defined function`，则返回一个`instance methods`
			- `static method`和`class method`会通过`Descriptors`实现
		3. class的`__getattr__`
	- 对实例属性的修改仅会修改实例的`__dict__`，不会修改类的`__dict__`。如果类中定义了`__setattr`和`__delattr__`，当修改属性是会先调用这两个方法。

## Special method names

### basic customization
- `__new__`创建对象，`__init__`初始化对象
- `__new__`返回一个对象，`__init__`不需要显示返回值（返回空值）
- 当在一个类上定义了`__new__`后，如果调用`super().__new__(cls)`，不会向上搜索调用`type().__new__()`。

	```py
	class A:
		def __new__(cls):
			return super).__new__(cls)
	```

	需要注意：
	- A.__new__用来创建类A的实例
	- type.__new__用来创建A的实例

- 使用`__hash__`时，可以采用将对象的不同属性组合成一个`tuple`之后使用`hash()`处理。

### customizing attribute access

- `__getattribute__`: 获取属性的默认方式。使用`__getattribute__`可以完全控制对象属性的获取
- `__getattr__`: 如果通过`__getattribute__`无法获取属性，则会调用`__getattr__`
- `__setattr__`: 设置属性时触发
- `__delattr__`: 删除属性时出发

#### Implementing Descriptors

- `__get__`
- `__set__`
- `__delete__`
- `__set_name__`

#### Invoking Descriptors

```py
class Descriptor:
    def __init__(self, name):
        self._name = name
    def __get__(self, instance, owner_class):
        if instance:
            return instance.__dict__.get(self._name, "is empty")
        raise ValueError("you need a instance")
    def __set__(self, instance, value):
        if not instance:
            raise ValueError("you need a instance")
        print(f"set new value {value}")
        instance.__dict__[self._name] = value

class Base:
    c1 = Descriptor("c1")
```

- 直接调用: `x.__get__(a)`
- 通过instance调用: `x.a`相当于`type(x).__dict__["a"].__get__(x, type(x))`
- 通过class调用: `X.a`相当于`X.__dict__["a"].__get__(None, x)`
- 通过super调用: 假设`super()`的返回值为`X`，则实际的调用相当于`X.__dict__["a"].__get__(x, x.__class__)`
- `data descriptor`: 定义`__set__`或`__delete__`中的一个，或全部。
- `not-data descriptor`: 仅定义`__get__`。
- `staticmethod`和`classmethod`都是`not-data descriptor`。`property`是一个`data descriptor`。

#### \_\_slots__
`__slots__`能够显式地决定那些属性可以被创建，并且可以阻止`__dict__`和`__weakref__`被创建（除非通过`__slots__`显式的声明）

`__slots__`的主要用途是`节省内存（当某个类的实例数量十分庞大时）`和`加速属性获取`。


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

当`class`定义被执行时，以下步骤依次执行:
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


## about type

当使用`type(object)`时返回`object`的类型信息。类似于`object.__class__`。

当使用`tyep(name, bases: tuple, dict, **kwds)`时，创建一个新的`type object`。这是一种动态创建`class`的声明方式。
- `name`作为`__name__`。
- `bases`作为`__bases__`。如果bases为空tuple，则`object`被加入。
- `dict`作为`__dict__`。
- `kwds`

## reference

https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
> this is very important

https://docs.python.org/3/reference/datamodel.html#customizing-class-creation