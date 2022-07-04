# python interview

## python GIL

python全局解释器，可以理解为一个锁。python仅允许一个线程获取解释器。

GIL存在的目的是避免多个线程同时对python中的引用计数进行修改，造成对象被错误的清除。

[python GIL](https://realpython.com/python-gil/)

## python 多进程与多线程

python中的多线程由于有GIL的存在，对于`CPU密集型任务`完全实用，并且由于额外增加了获取锁和释放锁的开销，会是多线程任务的执行时间长于单线程任务的执行时间。

但是GIL对于多线程的`IO密集型任务`没有什么影响。因为当线程等待IO是，GIL会被释放，然后被别的线程获取。

为了突破GIL的瓶颈限制，可以使用多进程库`multiprocessing`。对于多进程，每个进程都会有一个自己的python解释器，就不存在GIL导致的瓶颈。

## *args, **kwargs

对于可变参数对于函数的输入参数的数量不确定时，可以使用`*args`，python会将所有的参数通过一个元组存储。

对于关键字参数，当输入的数量不确定时，使用`**kwargs`，python将它通过一个字典存储。

使用`*args`、`**kwargs`和默认参数的顺序需要注意。

默认参数必须在最前，之后是可变参数，关键字参数必须放在最后面。

`*` 和 `**` 代表解包操作。解包操作可以将任何可迭代对象中将元素解包出来。 其中`*`作用于可迭代对象，`**`作用于字典。

[Asterisks in Python: what they are and how to use them](https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/)

[pep-3102](https://www.python.org/dev/peps/pep-3102/)

[pep-448](https://www.python.org/dev/peps/pep-0448/)

## 装饰器

In mathematics and computer science, a `higher-order function` is a function that does at least one of the following:

- takes one or more functions as arguments (i.e. procedural parameters),
- returns a function as its result.

All other functions are `first-order functions`.

定义：装饰器是一个方法，可以接受其他方法作为参数传入并可以不用修改传入的方法就可以扩展它的功能，最终返回一个函数。

```py
from functools import wrap
def print_log(func):
    @warp(func)
    def wapper(*args, **kwargs):
        print('log info')
        return func(*args, *kwargs)
    return wapper
```

```py
def print_log(key=None, key2=None):
    def first_wrap(func):
        def wapper(*args, **kwargs):
            print('log info')
            return func(*args, **kwargs)
        return wapper
    return first_warp
```

## 迭代器、生成器、可迭代对象

生成器函数：函数中存在`yield`关键字的函数，就被称为生成器函数。生成器函数是迭代器，因为它实现了迭代器接口。

可迭代对象：实现`__iter__`，并且返回一个迭代器。

迭代器：实现`__iter__`，返回迭代器自身。实现`__next__`。

## python作用域

local、enclosing、global、builtin

## 闭包

出现在函数嵌套时。

```py
def f1():
    counter = 0
    def f2():
        nonlocal counter
        counter += 1
        return counter
    return f2
```

## 可变类型和不可变类型

可变类型： list， dict
不可变类型：string， int， flot， tuple

## __new__ 与 __init__

`__new__`创造对象

`__init__`初始化对象

## with

`__enter__` && `__exit__`。实现了这两个魔法方法，就能使用`with`。

## 匿名函数

lambda a: a+1

简单，直观使用与实现简单逻辑功能，对于负责的功能应该避免使用。

## 深拷贝与浅拷贝

引用传递

## 协程

pass

## python垃圾回收机制

引用计数

标记删除

分代回收
