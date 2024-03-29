# High Performance MySQl

- [x] 3. 服务器性能剖析
- [x] 4. schema于数据类型优化
- [x] 5. 索引
- [x] 6. 查询数据优化
- [x] 7. mysql高级特性
- [x] 10. 复制
- [x] 11. 可扩展的mysql
- [x] 12. 高可用性
- [x] 14. 应用程序缓存


## 逻辑架构

```puml

```

## 不同存储引擎的特性
- InnoDB
- MyISAM

95%的情况下都选择InnoDB

## mysql基准测试

sysbench

## 服务性能剖析

- 分析慢查询日志
  - `pt-query-digest`工具
- 剖析单条查询
  - 使用`show profile`
  - 使用`show status`
  - `Performance Schema`
    - 书上不是很推荐，应为写书的时候，该特性还不完善，不知道现在怎么样了
- 确认时单条查询问题还是服务器问题
  - `show global status`每秒获取服务器状态
  - `show processlist`获取线程状态

## 选择优化的数据结构


### 整数类型
- tinyint/smallint/mediumint/int/bigint，分别使用8, 16, 24, 32, 64位存储空间，可以存储的值的范围从`-2 ** (n-1)`到`2 ** (n-1) - 1`

### Blob和Text类型
- blob和text被作为单独的对象进行存储。当blob和text值太大时，InnoDB会使用专门的"外部"存储区域来进行存储，此时每个值在行内需要1-4个字节存储一个指针，然后在外部存储区域存储实际的值。
 
### 缓存表和汇总表

缓存表: 将主表的部分信息写入缓存表中，可以针对特殊查询，创建索引或者选择合适的存储引擎

汇总表: 保存从主表中聚合而来的结果数据

### 物化视图

物化视图实际上时预先计算并存储在磁盘上的表，可以通过各种各样的策略刷新和更新。

### 加快alter table操作的数据

mysql执行大部分修改表结构操作的方法是用新的结构创建一个空表，从旧表中查出所有数据插入新表，然后删除旧表。这种方式在数据量很大，而且存在很多索引的情况下需要花费很长时间。

而且`alter table`操作将导致mysql服务中断。

比较常用的办法有两个
1. 在一台不提供服务的机器上执行alter操作，之后于提供服务的主库进行切换
2. 新建一张和原表相同的表，在该表上进行操作。之后通过重命名和删表交换两张表

## 复制

### 复制概述

mysql支持两种复制：*基于行的复制*和*基于语句的复制*。两种方式都是通过在主库上记录二进制日志，在备库重放日志的方式实现异步的数据复制。

### 复制如何工作
复制的三个步骤
1. 在主库上把数据更改记录到二进制日志中（这些文件也被称为二进制日志事件）
2. 备库将主库上的日志复制到自己的中级日志中
3. 备库读取中继日志中的事件，将其重放到备库数据之上

### 复制的原理

基于语句的复制和基于行的复制各有其优缺点，mysql能够在这两种复制模式中动态切换。

#### 基于语句的复制

将主库上的sql在从库上执行一边

优点：简单
缺点：
- 对于sql中包含通过函数计算的值（例如current_user()，当前时间的时间戳），会造成主从数据库之间的不一致。
- 强串行（TODO:）

#### 基于行的复制

优点: 每一行数据都会被正确复制，适用于大量情况。
缺点：对于`update my_table set col1=0`这种全表更新，使用基于行的复制开销会很大。

### 复制拓扑
- 一主多备：适用于读多写少的场景
- 主主复制：
  - 主动-主动：
  - 主动-被动：两个库都是对方的主库，但其中一个库是只读的
- 环形复制: 不推荐
- 分发主库: 应对一个主库有多个备库的情况。当备库过多时，主库同步数据的负载会过高，可以单独起一个备库执行数据同步工作。不过存在一个缺点，无法使用一个备库替换主库。由于分发主库的存在，导致各个备库和原始主库的二进制日志坐标已不相同。
- 树状或金字塔

### 复制和容量规划

写操作是复制的瓶颈，并且很难使用复制来扩展写操作。写操作无法像读操作一样被同等地分发到多个服务器上，换句话说复制只能扩展读操作，无法扩展写操作。

## 可扩展的mysql

可扩展性: 当增加资源以处理负载和增加容量时系统能够获得的投入产出比。**增加资源能够带来合理的性能提升**，增加一倍的资源能够获得一倍的性能提升。

向外扩展
- 按功能拆分
- 数据分片
