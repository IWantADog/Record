# python cookbook section 12

并发编程

## threading

- Thread
- Event
- Condition

## 线程之间通信

`Queue`多线程之间共享数据方式，其中已经实现了必要的锁，所以是线程安全的。

> 对于`Queue`中状态和大小的判断并不是线程安全的，所以最好不要在代码中使用相关的方法。

当使用队列时，协调生产者和消费者的关闭问题可能会遇到一些麻烦。一个通用的解决办法是在队列中放置一个特殊的值，当消费者读到这个值的时候就终止执行。

尽管`Queue`是线程安全的，但依然可以通过创建直接的数据结构并添加所需的锁和同步机制来实现线程之间的通信。最常见的方法是使用`Condition`变量来包装数据结构。


```py
import heapq
import threading

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()
    def put(self, item, priority):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait()
            return heapq.heappop(self._queue)[-1]
```

使用线程队列有一个要注意的问题是，向队列中添加数据项时并不会复制此数据项，线程间通信实际上是在线程间传递对象引用。如果你担心对象的共享状态，那你最好只传递不可修改的数据结构（如：整型、字符串或者元组）或者一个对象的深拷贝。

## 给关键部分加锁

- threading.Lock
- threading.Rlock
    > 不知道该如何合理使用？

## 防止死锁的加锁机制

解决死锁的一种方案是给每一个锁分配一个唯一的id，然后只允许按照升序规则使用每个锁。

```py
import threading
from contextlib import contextmanager

# Thread-local state to stored information on locks already acquired
_local = threading.local()

@contextmanager
def acquire(*locks):
    # Sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))

    # Make sure lock order of previously acquired locks is not violated
    acquired = getattr(_local,'acquired',[])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]
```

https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p06_storing_thread_specific_state.html