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
- yield不能在try/excep中（待确认，感觉有点问题）

### pep 342 -- Coroutines via Enhanced Generators

Also, generators cannot yield control while other functions are executing, unless those functions are themselves expressed as generators, and the outer generator is written to yield in response to values yielded by the inner generator. This complicates the implementation of even relatively simple use cases like asynchronous communications, because calling any functions either requires the generator to block (i.e. be unable to yield control), or else a lot of boilerplate looping code must be added around every needed function call.

