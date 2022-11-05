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

> 所有文档都会在发生给mongo之前被序列化胃BSON格式，之后再从BSON反序列化。驱动哭会处理底层的数据类型转换工作。

TODO: https://www.mongodb.com/docs/v6.0/core/index-ttl/?_ga=2.253478785.942358009.1667395083-1404305546.1667308134&_gac=1.25307727.1667482288.CjwKCAjwzY2bBhB6EiwAPpUpZsiJ_W5esy-00gWfd33FDlcOF80Jtk72M5JPuY06Q6eP7z-Borv0VxoCu6IQAvD_BwE

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






















