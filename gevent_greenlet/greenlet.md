# about greenlet

## 比较greenlet和threads

thread:
- 多个threads能够同时运行
- 多个threads的执行顺序由操作系统控制，无法通过代码控制
- 可能出现*竞争*、*死锁*等问题

greenlet:
- 有序执行。当一个greenlet运行时，其他的greenlet被阻塞。
- 能通过代码控制不同greenlet的执行顺序

> thread相较与greenlet需要更多的资源，相同资源下可以存在更多数量的greenlet

[一些有助于理解的例子](./practice_code/greenlet_example.py)

## greenlet中的概念

- ~~一个`greenlet`是一个独立的`伪Thread`~~
- 使用greenlet时一般会同时创建多个greenlet实例，并在多个greenlet之间切换。**切换是显式的，并且必须确定切换的目标**
	> Remember, switches are not calls, but transfer of execution between parallel “stack containers”, and the “parent” defines which stack logically comes “below” the current one.

- 通过`greenlet.switch()`切换greenlet时可以传递参数
- 通过`getcurrent()`获取当前正执行的greenlent
- main greenlet
	- 不需要创建就存在
	- 唯一一个`parent=None`的greenlet
	- 永远不会`dead`
- greenlet parents
	- 除了main greenlet其他的greenlet都有parent
	- 一个greenlet默认的parent是该greenlet被创建时所在的那个greenlet。
	- 当一个greenlet中止后，会返回到它的parent继续执行。这里的中止具体指函数显示return、函数执行完毕或者函数报错。
	- greenelt中未被捕获的异常会在它的parent中被报出。

## switch between greenlets

切换出现的情况
1. 调用`greenlet.switch`，切换到调用者继续执行
2. 调用`greenlet.throw`，切换到调用者继续执行
3. 当一个`greenlet`结束执行时，切换到该greenlet的parent继续执行

切换时可以传递一个`object`或是`exception`给目标greenlet。

### start from here
https://greenlet.readthedocs.io/en/latest/switching.html#switching-between-greenlets-passing-objects-and-control