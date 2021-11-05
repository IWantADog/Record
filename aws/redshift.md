# redshift

## 基本概念

### 数据仓库系统架构

[origin reference](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c_high_level_system_architecture.html)

- redshift基于postgresql，不过并不完全相同
  - [Amazon Redshift 和 PostgreSQL
](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c_redshift-and-postgres-sql.html)。
- redshift的核心基础组件是**集群**。
  - 集群包含一个或多个*计算节点*。如果集群预置两个或多个计算节点，则一个额外的领导节点将协调计算节点并处理外部通信。
  - 客户端仅直接与领导节点交互。
- 领导节点
  - 领导节点管理所有外部通信以及与计算节点的所有通信。
  - 分析并制定计算计划，将计算任务分配个*计算节点*。
  - 计算节点在查询存储在其他计算节点上的表时，才将sql发送给计算节点。所有其他的查询都在*领导节点*上运行。
  - [在领导节点上支持的sql函数](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c_sql-functions-leader-node.html)
- 计算节点
  - *计算节点*接受从*领导节点*分配来的任务。执行任务并将中间结果返回给*领导节点*最终聚合。
  - 计算节点拥有自己的CPU、内存和磁盘。
- 节点切片
  - 一个计算节点还可以细分为多个切片。每个切片被分配*计算节点*内存和磁盘空间的一部分，从而处理分配给*计算节点*工作负载的一部分。
- 数据库
  - 一个集群包含一个或多个数据库。
  - 用户数据存储在计算节点上。（sql客户端与领导节点进行通信，进而通过计算节点协调查询执行）

### 性能

[original reference](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c_challenges_achieving_high_performance_queries.html)

- 大规模并行处理
  - 将表行分配给计算节点，以便并行处理数据。
- [列式存储](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html)
- 数据压缩
- 结果缓存
  - 对部分结果有选择的缓存。

## 最佳实践

### 设计表的最佳实践
- 选择最佳的排序键
  - 要让 Amazon Redshift 选择适当的排序顺序，请指定**AUTO**作为**排序键**。
  - 如果最近使用的数据查询频率最高，则指定**时间戳列**作为排序键的第一列。
    
    这样查询会更高效，因为可以跳过该时间范围之外的整个数据块。

  - 如果您经常对某列进行范围筛选或相等性筛选，则指定该列作为排序键。
    
    Amazon Redshift 可以不读取该列的整个数据块。之所以能这样做，是因为它会跟踪每个数据块中存储的最小和最大列值，并且可以跳过不适用于指定范围的数据块。

  - 如果您频繁联接表，则**指定联接列作为排序键(sort key)和分配键(distribution key)**。
    
    这样，查询优化程序可以选择排序合并联接而不是较慢的哈希联接。因为数据已按联接键排序，所以查询优化程序不用执行排序合并联接的排序阶段

- 选择最佳的分配方式
  - TODO: 不是很理解

  [original reference](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c_best-practices-best-dist-key.html)

- 定义主键和外键约束
  - 如果合适在表之间定义主键和外键约束。这样有助于优化查询。
  - 除非应用程序强制实施约束，否则不要定义主键和外键约束。**redshift不强制实施唯一约束、主键约束和外键约束**。

- 使用尽量可能小的列大小

- 在日期列中使用合适的类型
  - 日期列应该使用*date*/*time*，而不应该使用*char*/*vachar*，这可以改善性能。

### 加载数据的最佳实践
- copy。**适用于从aws的不同资源导入数据，例如S3、dynamodb等**
- 多行插入
  - `insert into TABLE (<fields>) values (),(),()`
- 使用批量插入。**适用于将数据或数据的子集从一个表移动到另一个表**

  ```sql
  insert into table_name (select * from table_name);

  create table table_name as select * from table_name;
  ```

### 使用自动表优化
- 预设情况下，未显示定义排序键和分配键时创建的表将设置为**AUTO**。
- 手动修改**排序键**和**分区键**。

  ```sql
  alter table table_name alter sortkey auto;
  alter table table_name alter diststyle auto;
  ```

  - 如果运行 ALTER 语句将表转换为自动表，则会保留现有的排序键和分配样式。
  - **排序键和分区键不能同时设置为AUTO**
