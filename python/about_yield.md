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

That exhausts the current alternatives. Some other high-level languages provide pleasant solutions, notably iterators in Sather [4], which were inspired by iterators in CLU; and generators in Icon [5], a novel language where every expression is a generator. There are differences among these, but the basic idea is the same: provide a kind of function that can return an intermediate result ("the next value") to its caller, but maintaining the function's local state so that the function can be resumed again right where it left off. A very simple example:
