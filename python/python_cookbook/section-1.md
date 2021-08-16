# python cookbook section 1

## 数据的解包

```py
a, b, c = [1, 2,3 ]

# 对于数据较多的情况使用`*`
a, *array, c = [1,2,3,4,5,5,6]
```

## 双端列表`deque`

`from collections import deque`

- 可以设置队列的长度，当新元素压入并且队列已满时，旧的数据会被移除。
- 支持通过队列`头尾压入`和`弹出`操作。并且操作的时间复制都为`O(1)`

## heapq

`import heapq`堆排序算法(很有意思)
> 在底层实现中首先会将数据进行堆排序，之后再放入一个列表中。

TODO: sotred的底层实现是什么样的？

[通过heapq实现一个优先级队列](https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p05_implement_a_priority_queue.html)

> 可迭代对象是支持比较大小的，具体的比较逻辑是根据列表挨个比较。需要注意的是，尽量下表相同的两个数据的数据类型可以比较。

## 自动创建字典映射

`collections.defaultdict`。当一个key对应的value需要初始化的十分有用。

## 有序字典

`collections.OrderedDict`。有序字典，保持字典数据的插入顺序。

> 需要注意的是`OrderedDict`使用的内存是`dict`的两倍（因为`OrderedDict`内部使用了一个链表维持数据的顺序）。所以如果数据量很大时，需要仔细权衡一下。

## zip

dict.key()和dict.values()返回的数据好像是一一对应的。(带测试)


https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p08_calculating_with_dict.html