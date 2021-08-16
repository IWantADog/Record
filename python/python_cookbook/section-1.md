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

https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p04_find_largest_or_smallest_n_items.html
