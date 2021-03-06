# Python的垃圾回收

 python的垃圾回收机制以引用计数为主，标记清除和分代回收为辅。

### 引用计数

引用计数法的原理：所有的python对象维护一个ob_ref字段，用来记录该对象当前被引用的次数，每当新的引用指向该对象时，它的引用计数ob_ref加1，每当该对象的引用失效时计数ob_ref减1，一旦对象的引用计数为0，该对象立即被回收，对象占用的内存空间将被释放。

它的缺点是需要额外的空间维护引用计数，这个问题是其次的，主要的问题是它不能解决对象的“循环引用”，因此，也有很多语言比如Java并没有采用该算法做来垃圾的收集机制。

什么是循环引用？A和B相互引用而再没有外部引用A与B中的任何一个，它们的引用计数虽然都为1，但显然应该被回收，例子

```python
    a = { } #对象A的引用计数为 1
    b = { } #对象B的引用计数为 1
    a['b'] = b  #B的引用计数增1
    b['a'] = a  #A的引用计数增1
    del a #A的引用减 1，最后A对象的引用为 1
    del b #B的引用减 1, 最后B对象的引用为 1
```

del之后，已经没有引用指向a、b，意味着a，b已经无用，内存需要释放。可是a，b的引用都还是1，此时引用计数算法无法处理。所以python又添加了标记清除和分代回收算法，处理循环引用。

### 标记清除

『标记清除（Mark—Sweep）』算法是一种基于追踪回收（tracing GC）技术实现的垃圾回收算法。它分为两个阶段：第一阶段是标记阶段，GC会把所有的『活动对象』打上标记，第二阶段是把那些没有标记的对象『非活动对象』进行回收。那么GC又是如何判断哪些是活动对象哪些是非活动对象的呢？

对象之间通过引用（指针）连在一起，构成一个有向图，对象构成这个有向图的节点，而引用关系构成这个有向图的边。从根对象（root object）出发，沿着有向边遍历对象，可达的（reachable）对象标记为活动对象，不可达的对象就是要被清除的非活动对象。根对象就是全局变量、调用栈、寄存器。

![mark-sweep](/images/python-gc-mark-sweep.jpeg)

在上图中，我们把小黑圈视为全局变量，也就是把它作为root object，从小黑圈出发，对象1可直达，那么它将被标记，对象2、3可间接到达也会被标记，而4和5不可达，那么1、2、3就是活动对象，4和5是非活动对象会被GC回收。

标记清除算法作为Python的辅助垃圾收集技术主要处理的是一些容器对象，比如list、dict、tuple，instance等，因为对于字符串、数值对象是不可能造成循环引用问题。Python使用一个双向链表将这些容器对象组织起来。不过，这种简单粗暴的标记清除算法也有明显的缺点：清除非活动的对象前它必须顺序扫描整个堆内存，哪怕只剩下小部分活动对象也要扫描所有对象。

### 分代回收

Python将内存根据对象的存活时间划分为不同的集合，每个集合称为一个代，Python将内存分为了3“代”，分别为年轻代（第0代）、中年代（第1代）、老年代（第2代），他们对应的是3个链表，它们的垃圾收集频率随对象的存活时间的增大而减小。新创建的对象都会分配在年轻代，年轻代链表的总数达到上限时，Python垃圾收集机制就会被触发，把那些可以被回收的对象回收掉，而那些不会回收的对象就会被移到中年代去，依此类推，老年代中的对象是存活时间最久的对象，甚至是存活于整个系统的生命周期内。同时，分代回收是建立在标记清除技术基础之上。分代回收同样作为Python的辅助垃圾收集技术处理那些容器对象

## 参考
[FOOFISH-PYTHON之禅-Python中的垃圾回收机制](https://foofish.net/python-gc.html)

