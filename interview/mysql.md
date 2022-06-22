# mysql

## mysql base

## 读写分离

### 使用场景
- 读远多于写的使用场景

### 好处
- 分摊服务器压力
- 提升服务的可用性，当一个机器宕机之后可以快速调整一个从库快速恢复服务

## mysql索引类型
- 主键索引: 主用与主键, 字段必须唯一，非空
- 普通索引: 字段可以重复、可以为null
- 唯一索引: 字段必须全表唯一，但是允许NULL，并且运行存在多行NULL
- 组合索引: 组合多个字段构成索引
  - 组合索引使用时需要注意where中的`leftmost prefix`。如果创建了一个组合索引（col1, col2, col3），mysql查询时对于`(col1), (col1, col2), (col1,col2, col3)`也可使用索引进行查询。而对于`(col2, col3)`索引则不起作用。
- 全文索引:
- 空间索引:

```sql
create table test_index(
  id int,
  name varchar(10),
  unique index (name)
)

create table test_index_2(
  id int,
  name varchar(10),
  index (name)
)
```