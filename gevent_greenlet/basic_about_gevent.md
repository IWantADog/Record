# about gevent

[gevent For the Working Python Developer](https://sdiehl.github.io/gevent-tutorial/#introduction)

## Core

### Greenlets

The primary pattern used in gevent is the Greenlet, a lightweight coroutine provided to Python as a C extension module. Greenlets all run inside of the OS process for the main program but are scheduled cooperatively.

> Only one greenlet is ever running at any given time.

### Synchronous & Asynchronous Execution

The real power of gevent comes when we use it for network and IO bound functions which can be cooperatively scheduled. Gevent has taken care of all the details to ensure that your network libraries will implicitly yield their greenlet contexts whenever possible.

> 通过猴子补丁，gevent会隐式的自动处理阻塞网络和io请求。

### Determinism

As mentioned previously, greenlets are deterministic. Given the same configuration of greenlets and the same set of inputs, they always produce the same output.

> 对于相同的配置和相同的输入，greenlets的输出是相同的。

The perennial problem involved with concurrency is known as a race condition. Simply put, a race condition occurs when two concurrent threads / processes depend on some shared resource but also attempt to modify this value. This results in resources which values become time-dependent on the execution order. This is a problem, and in general one should very much try to avoid race conditions since they result in a globally non-deterministic program behavior.

The best approach to this is to simply avoid all global state at all times. Global state and import-time side effects will always come back to bite you!

> 虽然`greenlets`对于相同输入产生相同的输出。但是实际运行时，还是会出现不可预知的情况。

> 为了避免出现`race condition`。不应该在协程之间共享数据。

### Spawning Greenlets

```py
thread1 = Greenlet.spawn(foo, "Hello", 1)

# Wrapper for creating and running a new Greenlet from the named
# function foo, with the passed arguments
thread2 = gevent.spawn(foo, "I live!", 2)

# Lambda expressions
thread3 = gevent.spawn(lambda x: (x+1), 2)

threads = [thread1, thread2, thread3]

# Block until all threads complete.
gevent.joinall(threads)
```

### Greenlet State

- started -- Boolean, indicates whether the Greenlet has been started
- ready() -- Boolean, indicates whether the Greenlet has halted
- successful() -- Boolean, indicates whether the Greenlet has halted and not thrown an exception
- value -- arbitrary, the value returned by the Greenlet
- exception -- exception, uncaught exception instance thrown inside the greenlet

> 获取greenlet的状态

### Program Shutdown

A common pattern is to listen SIGQUIT events on the main program and to invoke gevent.shutdown before exit.

```py
import gevent
import signal

def run_forever():
    gevent.sleep(1000)

if __name__ == '__main__':
    gevent.signal(signal.SIGQUIT, gevent.kill)
    thread = gevent.spawn(run_forever)
    thread.join()
```

### Timeouts


### Monkeypatching

monkey.patch_socket()

This is a purely side-effectful command to modify the standard library's socket library.

This lets us integrate libraries that would not normally work with gevent without ever writing a single line of code. While monkey-patching is still evil, in this case it is a "useful evil".

> 使用gevent提供的猴子补丁，修改python中会被阻塞的相关库的相关操作（例如ssl、socket、select、threading）。

## Data Structures

### Events

Events are a form of asynchronous communication between Greenlets.

> 类似于threading.Event


### Queues

> 类似于theading.Queues

### Groups and Pools

> 类似于multiprocessing.Groups

### Locks and Semaphores

> 使用方法类似与threading.lock

### Thread Locals

Gevent also allows you to specify data which is local to the greenlet context. __Internally, this is implemented as a global lookup which addresses a private namespace keyed by the greenlet's getcurrent() value.__
