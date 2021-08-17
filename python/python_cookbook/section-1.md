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

## 字典的`键视图`和`元素视图`

`dict.keys()` & `dict.items()`的返回结果支持集合操作，比如集合并、交、差运算。

## 删除重复数据并保持数据的顺序

```py
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
```

## 切片对象

`slice()`。切片对象可以在任何使用切片的地方使用。

## 计算序列中出现次数最多的元素

`collections.Counter`

## operator模块

通过函数的调用，操作一些常用的运算符。

## 对排序后的存在重复数据的序列进行分组

`itertools.groupby()`

## 过滤序列对象

- filter: 需要注意的是返回的是一个迭代器，仅可迭代一次。
- `itertool.compress()`:  它以一个 `iterable` 对象和一个相对应的 `Boolean` 选择器序列作为输入参数。 然后输出 `iterable` 对象中对应选择器为 `True` 的元素。
	> 需要注意的是返回的结果也是一个迭代器。

https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p17_extract_subset_of_dict.html