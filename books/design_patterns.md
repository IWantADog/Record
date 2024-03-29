# design patterns [设计模式]

## 创建型模式

### Factory Method

**将类的初始化延迟到子类。**

本质:
- 父类定义创建接口。
- 子类实现创建接口，返回需要的功能类实例。不同的子类返回各自需要的类实例。

实现:
- 父类是否提供缺省实现
- 参数化工厂方法。使用时通过显式输入参数选择需要生成的类。子类继承父类的实现并可扩展。
- 对于类可以作为对象的语言，这一直接将目标类作为类变量。
- 注意命名，显式指出是否使用了*工厂方法*

### Builder

**对象的构建和表现分离。**

变化点
- 一个由许多不同部件构成的整体，需要对不同的部件做多种不同的转化。

本质
- 定义一个抽象基类，每个部件使用相应的接口。

### Abstract Factory

对工厂函数进行抽象。

抽象工厂定义所有接口。

子类负责实现具体的功能。

- 变化点
**许多类需要支持具有不同表现的相同功能。**

### Prototype

对于python来说，就是将类作为一个类变量，之后根据类变量生产实例。

### Singleton

单例模式，某一个类只能拥有一个实例。

## 结构型模式

### Adapter

包装器，已有类的接口不符合需求。对旧有类做一层包装。
- 类的适配器，使用多重继承实现。
- 对象的适配器，使用对象组合实现。

### Bridge

桥接，**抽象与实现分离**。

变化点
- 同时有多个抽象和多种实现方式。并且抽象和实现可以灵活的切换。

实现
- 对于python还是直接将类对象，作为类变量;当有多个实现时，可以在抽象层中增加工厂方法获取指定的实现.

感觉类似这样：

Abstract A \                      / Implement_1
Abstract B -  Abstract - Implement - Implement_2
Abstract C /                      \ Implement_3

### Composite

组合模式。**对单个对象和组合对象的使用具有一致性。**

关键点
- 子部件与父部件拥有相同的接口

实现
- 子部件中需要保留父部件的引用
- 需要考虑父部件中子部件的存储方式
- 最大化容器的接口，并提供缺省功能。

### Decorator(装饰器)

动态的给一个对象增加一些功能。相较与类继承更加的灵活。

关键点:
- **装饰器对象与被装饰对象需要有完全相同的接口**。可以定义一个基类，装饰器和被装饰器都继承至基类。而对于数量较少的装饰，可以不定义基类，而仅仅将数据转发给被装饰对象。
- 实现时装饰器对象中需要维持一个被装饰对象。
- 当被装饰对象原本就十分庞大时，使用`decorator`的代价太大，可以使用`strategy`模式。

### Facade(外观)

定义一个高层接口，简化对子系统的调用。

### FlyWeight（共享对象）

使用共享对象，节省内存资源。

关键点：
- 对**种类有限**但**实际数量很大**的数据进行建模。
- 重点区分**内部状态**和**外部状态**。内部状态是可以共享的，而外部状态是不可共享的。
- 对共享池进行建模
- 创建获取flyweight对象的工厂方法。

### Proxy（代理模式）

对其他对象做一层封装，控制对该对象的访问。

## 行为模式

### Chain Of Responsibility(职责链)

将对象链接起来构成一条链，将请求延链条传递直到有一个对象将其处理。解耦**发送者**和**接受者**之间的关系。

变化点：请求的发送者不确定接受者。

TODO: 感觉想不到合适的使用场景，先这样吧。
- 请求链如何合理的构建？

### Command(命令模式)

**将一个请求封装为一个对象**

要点：
- `Invoker`接受`Command`实例，并在内部维持。`Invoker`仅仅调用`Command`暴露的公用接口。
- `Command`实例中维持`Receiver`实例。并且暴露公用的接口，供`Invoker`调用。
- 每个`Command`实例可能一次调用多个`Receiver`方法。

`command`模式的实现是建立在`Receiver`拥有合理的公共接口的基础上的，不然所有`Receiver`都需要对应一个`command`。

我之前对`command`模式的理解是：简单的将需要执行的命令和数据通过结构体的形式传递给`receiver`，`receiver`通过解析结构体获取`方法标识`和`数据`，通过方法标识寻找相应的方法，并将数据作为参数调用方法。

实现：
1. 一个命令应该达到何种的智能程度。

    一种极端是一个`command`仅包含一个接受者和执行该请求的动作。另一种极端是没有接受者，所有的功能都由`command`自身实现。

    在这两个极端之间的情况是`command`有足够的信息可以找到`invoker`。

2. 支持实现`undo`和`redo`。内部存储`invoker`的状态，`command`可以被`reverse`。

### Interpreter(解释器)

给定一种语言，定义它的文法标识，并定义一个可以解释该语言的解释器。

### Iterator(迭代器)

提供一种方式顺序访问一个聚合对象的各个元素，同时不暴露该对象的内部标识。

要点：
1. 将对列表的访问和遍历从列表对象中分离出来并放入一个`迭代器对象`中。
2. 同一个数据结构可以设置不同的迭代算法。

### Mediator(中介者)

创建一个中介对象，将需要的功能类组合起来。使各个功能类不需要额外维持其他类的引用，确保类之间的松耦合。

### Memento(备忘录)

在不破坏类的封装的情况下，将类的部分内部信息保存到一个外部对象中。以便对类的状态进行回溯。

实现：
1. 维持Memento的数据既可存放在`Originator`内部也可存放在外部`Caretaker`。

需要注意的问题
1. 对于需要保存的数据量很大的情况，不适合使用`Memento`模式。（可以考虑使用增量式修改）
2. 即使是很小对象的数据记录，如果数量过多，也会造成大量存储开销。

### Observer(观察者)

> 感觉使用「发布订阅」更直观。

一个`target`对象被多个`observer`对象依赖。当`target`目标变化时，通知并自动更新其他`observer`。如果修改某个`observer`，其他`observer`也会被自动更新。

变化点：
1. 订阅者的种类和数量

实现：
1. 需要注意的是：发出请求的`observer`对象并不立即更新，而是将其推迟到它从`target`获取通知。
    > 避免对发起修改的`observer`做两次修改。

2. 由谁触发更新操作
    - 由`target`触发。不需要`observer`显示指定，不过每次微小修改都会通知所有`observer`。
    - 由`observer`触发。对若干修改累计后一起更新，不过需要显示调用，对于`observer`容易遗忘。

3. 避免特定于观察者的更新协议--推/拉模型
    - 推模型：`target`将若干数据推送给`observer`。不同的`observer`需要的数据可能不同，`target`推送的数据可能缺少或是冗余。
    - 拉模型： `target`不知道有那些`observer`。拉取所有的数据，需要`observer`识别那些做了修改。

4. 扩展`target`的注册接口，使`observer`仅注册对指定的事件感兴趣。

### State(状态)

动态修改对象的行为。

变化点：
1. 一个对象的不同状态，对应不同的行为。并且可以在运行时修改。

### Strategy(策略模式)

将功能的实现委托给对象，使功能逻辑可以被修改和替换。

变化点：
1. 同一数据需要支持多种处理逻辑。


### Template Method(模版方法)

基类定义算法的骨架，子类实现细节。

> 将重复逻辑提取到父类，子类仅实现差异的部分。

### Visitor（访问者模式）

对于不同的数据结构，在不改变其数据结构的基础上，定义作用于该数据结构的操作。

变化点：
1. 对于不同的数据结构需要支持共同的操作。

实现：
1. 将不同的功能定义为不同的类，每个功能类需要实现对所有数据结构的支持。
2. 使用访问者模式时，考虑的关键问题是系统的那一部分会经常修改。是作用于对象结构的算法还是对象结构本身。如果是对象结构本身，则并不适合使用`visitor`模式。

## 体会

使用设计模式的主要目的是为了**应对变化**。不同的功能有不同的表现，但他们的根本运行逻辑有一套通用的流程。将通用的逻辑抽象出来。每次实现不同的功能时，不必完全从头开发而仅需要关注功能的不同点即可。

判断自己是否应该使用设计模式？应该使用那种设计模式？这些问题的根本都在于需求中变化的点在哪里，有多少。

一句话，**对变化封装**。
