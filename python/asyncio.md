# about asyncio

## Coroutines and Tasks

### Coroutines

一个方法使用`async/await`定义，则被成为`coroutine function`。
一个`coroutine function`返回的对象是一个`coroutine object`。

```py
"""a simple example"""
import asyncio

async def main():
	print("hello")
	await asyncio.sleep(1)
	print("world")

asyncio.run(main())
```

### Awaitables

当一个`object`能够被`await`使用，则它就能被称为是`awaitables`。
常见的`awaitables`的类型有`Coroutines`、`Tasks`、`Futures`。

- Corotines: 使用`async`定义的方法
- Task: 使用`asyncio.create_task()`包装一个`Corotines`
- Futures: 过于底层，不用深究

### 运行一个`asyncio`项目

- asyncio.run()
- asyncio.gather()
- asyncio.sleep()
- asyncio.wait_for()


## Streams


## Running a asyncio program

https://docs.python.org/3/library/asyncio.html

## How asyncio work

https://stackoverflow.com/questions/49005651/how-does-asyncio-actually-work


## async in flask
- async在flask原理
- async在flask中的实现与完全使用``
- 算了，先搞清楚如何使用greenlet&gevent


### greenlet
- thread由系统调度。greenlet由用户调度？
- greenlet的调度可以完全由用户来控制。