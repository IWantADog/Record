# threaindg.local & contextVar

## threading.local

[_threading.local](https://github.com/python/cpython/blob/main/Lib/_threading_local.py
)

`threading.local`。不同的线程访问同一个实例化后`local`对象，只会得到属于该线程的数据。

```py
>>> from threading import Thread as T
>>> from threading.local import local


>>> l = local()
>>> l.val = 1

>>> def change():
    l.val = 2
    print(l.val)

>>> t = T(target=change)
>>> t.start()
2

>>> l.val
1
```

通过阅读`_threaidng.local`发现。每个`local`对象，内部都会维持一个`_localimpl`的变量。而`_localimpl`内部维持了一个`dict`，形如`{ id(Thread) -> (ref(Thread), thread-local dict) }`的结构。

每当一个线程访问`local`实例获取内部的数据时，其实就是通过当前线程的id，去`_localimpl.dicts`中获取value(获取时还通过线程锁来进行管理)。获取之后再将value写入到`local.__dict__`中。

> m.x is equivalent to m.__dict__["x"].

所以不同线程访只会得到属于该线程的值。


## contextvar

`contextvar`和`threading.local`很相似。不过`contextvar`能够正确的跟踪异步任务的变量。

### useing guideline

- 声明一个模块的全局变量作为句柄
- 每个异步任务通过 get() 获取句柄对应的变量
- 每个异步任务通过 set() 修改句柄对应的变量

### Context

当许多异步任务同时运行时，之前使用`threading.local`的做法是线程维持自己的`local`。不过使用`contextvars`后，每个线程维持的是一个包含`contextvars.Context`的`thread-local storage`。`Context`通过`key-value`存储`ContextVar`。

> Manipulation of the current context is the responsibility of the task framework, e.g. asyncio.

Context是一个`immutable dict`。只可读不可直接修改，并且支持所有`dict`的接口。

- 需要修改`context`时，需要使用`Context.run()`
- 使用`ContextVar.set()`修改 context 中的变量

ContextVar.get() 获取变量时，本质是以自己作为`key`从`context`中获取变量。

无法直接获取`context`的引用，但是可以通过`contextvars.copy_context()`获取一个当前系统线程的`context`拷贝。

### ContextVar & Token

```py
# ContextVar 和 Token 的使用
>>> c = ContextCar('t')
>>> c.set(1)
<Token var=<ContextVar name='a' at 0x7fa132089c20> at 0x7fa132523f80>
>>> c.get()
1

>>> t = c.set(2)
>>> c.get()
2

>>> c.reset(t)
>>> c.get()
1
```

### implement

[implement code](https://www.python.org/dev/peps/pep-0567/#implementation)

### Backwards Compatibility

__This proposal preserves 100% backwards compatibility.__

Libraries that use threading.local() to store context-related values, currently work correctly only for synchronous code. __Switching them to use the proposed API will keep their behavior for synchronous code unmodified, but will automatically enable support for asynchronous code.__


### reference

[pep-0567](https://www.python.org/dev/peps/pep-0567/)

[pep-0550](https://www.python.org/dev/peps/pep-0550)

[contextvars](https://docs.python.org/3/library/contextvars.html)





