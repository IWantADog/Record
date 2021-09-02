# About yield

## 生成器表达式
- 一个生成器表达式返回的是一个`生成器对象`
- 使用生成器表达式，返回值是在`__next__()`被调用时`lazily`计算。
- 为了避免干扰生成器表达式，在生成器表达式中应该避免使用`yield`和`yield from`

## yield表达式

- `yield from <expr>`中expr必须为`iterable`。

## gejerator-iterator methods

- generator.__next__()
- generator.send(value)
- generator.throw()
- generator.close()

```py
>>> def echo(value=None):
...     print("Execution starts when 'next()' is called for the first time.")
...     try:
...         while True:
...             try:
...                 value = (yield value)
...             except Exception as e:
...                 value = e
...     finally:
...         print("Don't forget to clean up when 'close()' is called.")
...
>>> generator = echo(1)
>>> print(next(generator))
Execution starts when 'next()' is called for the first time.
1
>>> print(next(generator))
None
>>> print(generator.send(2))
2
>>> generator.throw(TypeError, "spam")
TypeError('spam',)
>>> generator.close()
Don't forget to clean up when 'close()' is called.
```

## pep

### pep 255 -- simple generators
- yield不能在try/excep中(**不过在之后的pep中修改了这个特性**)

### pep 342 -- Coroutines via Enhanced Generators
- 在这个pep中增加了`yield`可以写在`try-finally`中的功能
- 生成器的本质是当调用一个函数时并不立即执行该方法，而是用返回一个对象来代替对函数返回的结果。
- 得到返回的生成器对象之后，用户需要在该对象上调用方法来驱动函数一步步执行。
    - 通常对生成器对象使用的`for`和`next`方法，其实都调用的是生成器的`__next__`方法。
    - `send`可以向生成器传递数据，不过只能传递一个参数。
    - `throw`是向生成器对象中传递一个异常。实现一个生成器函数时，可以对不同的异常做相应的处理逻辑。如果捕获异常之后重新`yield`新值，则新值会作为`throw`的返回值。
    - `close`是关闭一个生成器，`close`之后的`__next__`调用都会报`StopIteration`。可以在生成器内部执行资源回收的操作。
- `yield`是一个`expression`，返回值为`None`，除非通过`send`发送一个`非None值`。

```py
def test(_t=None):
    while True:
        try:
            _t = (yield _t)
        except Exception as e:
            print("catch exception: " + str(e))
        finally:
            print("in finally")
```

#### tips

关于`statement`&`expression`。可以简单理解为能放在`=`右边的是`expression`，反之则是`statement`。

### pep 380 -- Syntax for Delegating to a Subgenerator

A syntax is proposed for a generator to delegate part of its operations to another generator. This allows a section of code containing 'yield' to be factored out and placed in another generator. Additionally, the subgenerator is allowed to return with a value, and the value is made available to the delegating generator.

