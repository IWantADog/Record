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

https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p03_communicating_between_threads.html#


