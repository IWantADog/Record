# about mongo

- [ ] mongo的索引
- [ ] mongo的可扩展性（水平扩展）
- [ ] mongo的持久化策略
- [ ] mongo的分片
- [ ] mongo的python驱动
  [PyMongo](https://pymongo.readthedocs.io/en/stable/tutorial.html)
- [ ] mongo schema设计的最佳时间
- [ ] mongo的查询技巧
- [ ] mongo的索引使用技巧
- [ ] mongo的原子性
- [ ] mongo中的事务

##  MongoDB基本概念

数据库/集合/文档

mongo中用文档用来记录数据。集合即为文档的集合。

### CRUD
- C: insert
- R: find
- U: update
- D: remove

### index & explain

- db.user.createIndex
- explain: 分析查询（类似于mysql）

## 编写代码操作mongo

### 驱动工作原理

驱动的主要职责
- 生成MongoDB对象ID。默认都存储在所有字段的_id字段里
- 将任意语言表示的文档转换为BSON或者从BSON转换为JSON
- 使用MongoDB自定义的协议，通过TCP socket与数据库进行通信

#### 关于主键

mongodb中文档都需要一个主键，这个键对于每个集合中的文档都必须是唯一的，存储在_id中，开发者也可以自己提供`_id`，如果不提供MongoDB会使用自己的默认值。

mongodb中的id由12个字节的十六进制字符组成。其中前4个字节包含标准的Unix时间戳，紧接着的3个字节是机器ID，之后的两个字节是进程id，最后的3个字节保存的是进城本地计数器。

使用这种格式的很重要的原因是*ID是在驱动中生成的，而不是在服务器上生成*。这与许多的RDBMS系统不同。关系型数据库在服务器上自增自动增长，因此导致服务器成为生成键的瓶颈。而如果多个驱动生成id并插入文档，它们就需要创建唯一表示而不会互相影响的方法。

## 4 面向文档的数据

### 核心概念

#### 数据库

数据库是集合和索引的命名空间和物理分组。

`db.stats()`获取数据库的相关信息

### 集合

**创建集合是隐式的，只有插入文档时才会创建。**不过mongo也提供了创建collection的方法，通过这些方法可以设置集合的大小和能容纳的文档数量。

*盖子集合*：一种特殊的集合，当文档的数量或体积达到上限（体积上限优先于数量上限）时，新数据会覆盖旧数据。

*TTL集合*：拥有过期时间的集合。具体使用时，需要在一个`time_field`字段上创建索引。之后该字段会定期检查时间戳，并与当前时间比较，如果time_field与当前时间的差值大于`expireAfterSeconds`，文档会被自动删除。

> 所有文档都会在发生给mongo之前被序列化为BSON格式，之后再从BSON反序列化。驱动会处理底层的数据类型转换工作。

TODO: https://www.mongodb.com/docs/v6.0/core/index-ttl/?_ga=2.253478785.942358009.1667395083-1404305546.1667308134&_gac=1.25307727.1667482288.CjwKCAjwzY2bBhB6EiwAPpUpZsiJ_W5esy-00gWfd33FDlcOF80Jtk72M5JPuY06Q6eP7z-Borv0VxoCu6IQAvD_BwE

### 文档

**mongo单个文档的大小限制为16MB**

## 构建查询


### 查询
- find和findOne的区别
  - pymongo中的find返回的是游标可迭代

mongodb支持通过正则进行匹配查询和范围查询
- 部分匹配查询：db.user.find({"last_name": /^Ba/})
- 范围查询: db.user.find({"addresses.zip": {"$gt": 100, "$lt": 200}})

范围查询运算符
- $lt
- $gt
- $lte
- $gte

集合操作运算符
- $in
- $all
- $nin
  - 无法使用索引

布尔运算符
- $ne
  - 无法使用索引
- $not
- $or
- $nor
- $and
- $exists

关键字查询
- $exists

匹配子文档
- find({"like.fruit": "apple"})
> mongo不仅仅可以匹配子文档，还可以匹配整个子文档。需要额外注意的是，如果匹配整个文档，将执行严格的逐字节比较，关键字的顺序非常重要。`find({"like": {"fruit": "apple", "food": "milk"}})`和`find({"like": {"food": "milk", "fruit": "apple"}})`是不同的查询，查询的结果也不同。

数组查询
- $elemMatch: 如果提供的所有词语在相同的文档中，则匹配
  - `find({"address" :{"$elemMatch": {"state":1, "zip": 1}}})`
  > 注意与find({"address.state": 1, "address.zip": 1})的区别
- $size: 如果子文档长度与提供的值相同，则匹配
  - `find({"address": {$size: 2}})`

javaScript查询运算符
- $where: 执行任意JavaScript来选择文档。在JavaScript内关键字this指向当前文档。

正则表达式

### 查询选择

- 映射
  - 可以在find中指定需要返回的字段
  - $slice: 用来限制返回结果中，每个元素中列表field的长度
- sort
- skip & limit
  - 注意使用skip跳过较大的范围时，效率会很低，查询会扫描与skip相同量的数据。

## 聚合

聚合管道: 将整个聚合过程拆分为若干部分，某一部分以上一部分的输出作为输入。每个聚合阶段执行独立的任务，并且聚合阶段没有数量上的限制。

sql和聚合框架的类比（仅便于理解，不可深究）
select - $project, $sum, $min, $avg
from   - db.collection.aggregate
join   - $unwind
where  - $match
group  - $group
having/where - $match

- $out: 可以自动将聚合管道的输出结果保存到集合里。如果集合不存在，则$out会创建一个集合；如果集合存在就会完全取代现有的集合。
  - 如果聚合失败，旧数据不会被删除。当聚合成功时，数据才会被删除。
- $unwind: 将文档中的列表属性逐项展开。
  - 例如：对于 `{"_id": 1, "tags": [1,2,3]}` 展开之后就会变为 `[{"_id": 1, "tags": 1}, {"_id": 1, "tags": 2}, {"_id": 1, "tags": 3}]`
- $group:
  - $addToSet: 将聚合的值放入一个集合，元素不重复
  - $push: 将聚合的值放入一个列表，元素可重复
  - $first
  - $last
  - $max
  - $min
  - $avg
  - $sum
- $match & $sort & $skip & $limit
- $project
  - 包含许多重塑文档操作符

### 理解聚合管道的性能

*explain*

- 尽早地在管道中尝试减少文档的数量和大小
- 索引只能用于$match和$sort操作，而且可以大大加速查询
- 在管道中使用$match和$sort之外的操作符之后不能使用索引
- 如果使用分片，则$match和$project会在单独的片上执行。一旦使用了其他操作符，其他的管道将会在主要片上执行。
  - TODO: 完全不理解是什么意思

### 聚合光标选项

在聚合结果中通过光标获取数据。*cursor*允许我们处理大规模数据流。允许我们在返回少量文档结果的时候处理大的结果集，因此可以减少一次性处理数据所需的内存。

### 其他聚合功能
- .count:
  - db.user.count()
- .distinct
  - db.user.distinct("name")

## 更新、原子操作和删除

mongo中更新数据的方式有两种: 替换 和 通过操作符更新
- 替换：在业务代码层面，首先获取数据，更新之后在写入数据库
- 通过操作符更新：直接通过mongo的命令，有mongo处理获取和更新操作

> 为保证操作的原子性，应该使用通过操作符更新的方式。

TODO: mongo对于列表的查询很奇怪
  - 例如对于tag是个列表的情况，find({"tag": 1})会寻找所有tag列表中包含1的document。

### 原子文档处理

- findAndModify
- upsert

更新操作符
- $inc
- $set
- $unset
- $rename
- $setOnInsert
  - 使用upsert时会用到。当插入数据时，该操作会被执行；而如果是更新数据，该操作就不会被执行。
- $push
  - $each: 如果要向列表中push多个值时，需要使用到 *$each*。如果直接push，会将一个列表push到一个列表中去。
  - $slice: 当使用push和each向列表中添加新值时，可以同时使用$slice，对列表进行截断，控制列表的长度。
- $pushAll
- $sort
- $addToSet
  - 一次添加多个值时同样需要使用 *$each*
- $pop
- $bit
- $pull
  - pull还支持通过范围删除数据
- $pullAll
- 位置操作符
  - $

### mongo更新的性能

理解mongo如何更新磁盘上的文档可以帮助我们优化性能。

更新文档有三种方式
- 仅更新文档中的单个值，且BSON文档大小不会被改变。这种方式最为高效。
  - 实际的场景中，$inc就是这样。
- 更新文档的大小和结构。
  - 实际的场景中，$push就是这样
- 完全重写一个文档。如果文档扩大，现有的空间不能满足，可能还需要移动到新的空间。

## 索引与查询优化

mongo的索引使用的也是b树。所以mysql中关于索引的一些知识可以在mongo中复用。

[about index in mongo](https://www.mongodb.com/docs/v6.0/indexes/?_ga=2.137501808.1557011951.1668005095-1404305546.1667308134&_gac=1.192687576.1667482288.CjwKCAjwzY2bBhB6EiwAPpUpZsiJ_W5esy-00gWfd33FDlcOF80Jtk72M5JPuY06Q6eP7z-Borv0VxoCu6IQAvD_BwE)

索引的类型
- 唯一索引: 被索引的值全局唯一
  - `db.user.createIndex({username: 1}, {unique: true})`
  - collection中`_id`上默认有一个唯一索引
- 稀疏索引(Sparse Index): 仅对集合中存在特定field的文档添加索引
- multikey index: 当给一个列表类型的字段添加索引时，mongo会分别为数组中的每一项创建多个索引。
- hash index: 通过hash函数确定索引的位置。
  - hash index存在的限制:
    - 不支持范围查询
    - 不支持多键hash
    - 浮点数会被转换为整数。即4.2和4.3有相同的哈希索引
  - hash index的优点
    - 索引是均匀分布的。更适合分片存储
- 空间索引

### explain

- explain(true): 输出查询分析
- hint(): 强制查询使用给定索引
