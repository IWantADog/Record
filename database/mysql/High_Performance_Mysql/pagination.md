# mysql pagination

`PARTITION BY`

## 分区解决的问题

当数据量巨大时，不希望每次查询都扫描全表。而数据量巨大，也会导致索引在空间和维护上的消耗巨大。即使真的使用索引，如果使用非覆盖索引，返回大量的数据，也会产生大量的随机I/O，消耗大量时间。

分区提供了通过**少量的标识数据可以实现粒度更粗但消耗更少的方式来检索数据**。

## 分区的使用场景
- 表特别大，无法全部放入内存中。或者只在表的最后有热点数据，其他都为历史数据
- 避免特殊的瓶颈，例如InnoDB的单个索引的互斥访问
- 单独对分区进行删除、备份、修复、恢复和优化

## 分区的概念

分区表是一个独立的逻辑表，但是底层由多个物理子表组成。

实现分区的代码实际上是对一组底层表的句柄对象的封装。对分区表的请求，都会通过句柄对象转化为存储引擎的接口的调用。

分区表的索引也是也是按照分区的子表定义的，*没有全局索引*。

## mysql分区表的限制
- 一个表最多能有1024个分区
- 分区表达式的限制
- **如果分区字段中有主键或者唯一索引的列，那么所有的主键列和唯一索引都必须包含进来**
- 分区表中无法使用外键索引
- 所有分区必须使用相同的存储引擎

## 使用分区可能带来的问题
- NULL值会让分区过滤无效
  - 由于分区表达式可以为NULL，且为NULL的数据会写入第一个分区。当查找数据时由于分区表达式可能为NULL，所以也会查找第一个分区。而如果该分区中数据十分大时，查询的效率会很差。
  - 解决方案是创建一个存储NULL数据的分区，这样为null的数据不会出现在第一个分区中。即使每次都需要检查第一个分区，代价也很小。
- 分区列和索引列不匹配
  - 如果在a列定义了索引且在b列定义了分区。如果通过a列查找数据时，每一行数据都需要扫描所有分区上的索引。
- 选择分区的成本很高
  - 修改数据行的分区列，会将改行从旧分区中删除并插入新分区
- 打开并锁住所有的底层表的成本很高
  - 通过查询访问分区表时，mysql需要打开并锁住所有底层表，该操作在分区过滤之前发生，是使用分区表引入的额外开销。
- 维护分区的成本可能很高
  - 重新分区的代价较大。一般可以考虑将数据复制到临时分区，再删掉旧分区

## 查询优化

即便在创建分区时可以使用表达式，但在查询时却只能根据列来过滤分区。

## 分区的类型

### range partitioning

通过给定的范围条件进行分区
```
create table
partition by range (column)(
  partition p0 values less than (value_1),
  partition p1 values less than (value_2),
  partition p2 values less than (value_3),
  partition p3 values less than MAXVALUE,
)
```
> 可以通过*MAXVALUE*来兜底

### list partitioning
通过给定的列表进行分区
```
create table
partition by list (column/expr) (
  partition p0 values in (1,2,3,4),
  partition p1 values in (5,6,7,8),
  partition p2 values in (9,10,11,12),
  partition p3 values in (13,14)
)
```
> 没有像`range`的兜底功能，如果插入的数据无法确定分区，会报错

### columns partitioning

`range columns` & `list columns` 支持通过使用多个列作为分区的key。

`range columns`与`range`的区别:仅支持使用column，不支持使用表达式；支持多个列；并不仅限于int类型，string/date/datetime类型都支持

```
create table
partition by range columns(a, b, c) (
  partition p0 values less than (5,5,5),
  partition p0 values less than (10,10,10),
  partition p0 values less than (MAXVALUE, MAXVALUE, MAXVALUE)
)
```
> `range columns`判断数据行应该插入那个分区使用的是`tuple`之间比较，即依次比较不同的列，如果该列相同则比较下一列。

`list columns`与`list`的区别和`range columns`和`range`的区别相同

### hash partitioning

```
create table
partition by hash(expr)
partitions num
```
- `expr`的返回值必须为int，或者是mysql中整数类型列
- `num`指明分区的数量，必须为正整树
- hash分区的实质是`expr % num`

### key partitioning

key类似与hash，区别为
- hash使用用户提供的表达式，而hash使用mysql内部定义的
- key可以接受0个或多个列。如果表中存在`主键`，分区键必须包含部分主键或全部主键。如果不置顶列，则使用主键列或唯一约束列，否则会报错

`key partitioning`对于字符串类型不接受指定`prefix`

### subpagination

定义子分区

```
CREATE TABLE ts (id INT, purchased DATE)
PARTITION BY RANGE( YEAR(purchased) )
SUBPARTITION BY HASH( TO_DAYS(purchased) ) (
    PARTITION p0 VALUES LESS THAN (1990) (
        SUBPARTITION s0,
        SUBPARTITION s1
    ),
    PARTITION p1 VALUES LESS THAN (2000) (
        SUBPARTITION s2,
        SUBPARTITION s3
    ),
    PARTITION p2 VALUES LESS THAN MAXVALUE (
        SUBPARTITION s4,
        SUBPARTITION s5
    )
);
```

### 分区如何处理NULL

- range: 将null视为小于所有其他条件，所以插入第一个分区
- list: 如果定义分区时，某个分区的list中存在null，则插入该分区；如果不存在包含null的分区，则无法插入数据
- key & hash: 将null视为0处理
