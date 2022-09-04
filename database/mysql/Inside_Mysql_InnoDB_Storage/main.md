# about InnoDB

- [x] 1
- [x] 2
- [x] 3
- [x] 4
- [x] 5
- [x] 6
- [x] 7
- [] 8(略读)


## 1 mysql体系结构和存储引擎

没什么值得记录

## 2 InnoDB

InnoDB的体系架构进程、内存、文件

进程
- master thread：负责将缓冲池中的数据异步刷新到磁盘
- io thread: 处理io请求的回调
- purge thread: 用于清理处理事务提交后清理不用的undo页
- page cleaner thread: 处理之前版本的脏页的刷新操作
  - 脏页: 缓冲池中的页与磁盘上的页的数据不一致

内存
- 缓冲池: 
  InnoDB存储引擎基于磁盘存储数据，并将其中的记录按照页的方式进行管理。

  缓冲池简单讲是一块内存区域，目的是通过内存的速度来弥补磁盘数据较慢对数据库的影响。在数据库进行读页操作时，首先将从磁盘上读取的页放入缓冲池中。在下一次读区相同的页时，首先判断该页是否在缓冲池中。如果在缓冲池中，称该页在缓冲池中被命中，直接读区页。否则，从磁盘上读取页。

  对于数据库上的页的修改操作，则首先修改缓冲池中的页，然后在按照一定的频率刷新到磁盘上。需要注意的是，页从缓冲池刷行如磁盘的操作并不是在每次页发生更新是触发，而是通过一种称为*checkpoint*的机制刷新回磁盘。

  内存数据对象
  - 数据页
  - 索引页
  - 插入缓冲
  - 锁信息
  - 自适应哈希索引
  - 数据字典信息

-  LRU list、Free list、Flush list
  缓冲池通过LRU(Latest Recent Used，最近最少使用)算法进行管理。即讲最频繁使用的页在LRU的最前端，而最少使用的页在LRU的最后端。当缓冲池中不能存放新读到的页时，将首先释放LRU列表中尾端的页。

  TODO: LRU的算法问题不是很理解
  TODO: 为什么free列表上来存放了数据，按照描述free列表好像仅相当于存储的LRN的长度？Free list的功能是什么

  - LRU list用来管理已经读取的页。
  - Flush list用来管理脏页，将脏页数据刷新回磁盘。需要注意LRU和Flush中都存在脏页数据，但用途不同，不冲突。
- redo日志缓冲
  InnoDB存储引擎首先会将redo日志文件放入缓冲区，然后按一定的频率将其刷新到redo日志文件。

  redo日志缓冲一般不必很大，因为一般情况下每一秒钟会将日志缓冲刷新到日志文件，因此用户只需保证每秒产生的事务量在缓冲大小之内即可。

  redo日志写入磁盘的触发条件
  - master thread 每一秒讲redo日志缓冲刷新到日志文件
  - 每个事务提交时会讲redo日志缓冲刷新到日志文件
  - 当redo日志缓冲池剩余大小小于1/2时，redo日志缓冲池会被刷新到日志文件。

checkpoint
- 

master thread
- 将redo日志写入磁盘（即使事务还未被提交）
- 合并插入缓冲
- 刷新缓冲池脏页到磁盘
- 删除无用的undo页

InnoDB的关键特性
- change buffer
  [about change buffer in official document](https://dev.mysql.com/doc/refman/5.7/en/innodb-change-buffer.html)
  
  change buffer是一种数据结构。当对*secondary index*修改（insert/update/delete），而该索引还未被读入内存时，就会创建change buffer。

  change buffer的主要目的是解决*secondary index*写入磁盘的效率问题。由于*secondary index*的更新数据一般是随机无序的，会造成大量的随机io。所以当需要更新的索引不在内存中时，innodb会先创建*change buffer*；当需要更新的索引被读入内存，则会将*change buffer*和*secondary index*进行合并。

  change buffer在内存和磁盘上都有。  

  innodb对于对象的删除分为两个过程。1）将记录标记为已删除，2）真正将记录删除。*delete buffer*在过程1中被使用，*pure buffer*在过程2中被使用。

- doublewrite

  doublewirte是为了解决数据从内存写入磁盘可能发生的写入异常中断问题，保证数据页写入的可靠性。

  数据页从内存写入磁盘时，会先将数据写入*double write buffer*（内存中），再将*double write buffer*写入磁盘中，最后才通过内存中的*double write buffer*更新磁盘上的页数据。当写入失败时，innodb能够从磁盘上的*double write buffer*获取完整的数据。

  虽然写入了两次，当讲内存中的*double write buffer*写入磁盘中属于顺序写入，所以对性能的不大。

- 异步io
  - 可以将多个io合并为一个io，即将对于多次io对同一个页的访问，合并为一次。

  - 刷新邻接页

    InnoDB还提供了`Flush Neighbor Page`的特性。它的工作原理是：当刷新一个脏页时，InnoDB存储引擎会检测该页所在的区（extent）的所有页，如果是脏页，则一起刷新。这样可以使用AIO将多个io合并为一个io。

## 3 文件

慢查询日志
- 手动设置一个阈值*long_query_time*，如果sql的查询大于设置的值，则该sql会被记录到慢查询日志
- 对于没有启用索引的表，可能导致慢查询日志不断的增大，可以通过*log_throttle_queries_not_using_indexes*来限制每分钟允许记录到*slow log*中而且没有使用索引的sql
- 对于较大的*slow log*使用mysql提供的*mysqldumpslow*进行分析

表结构定义文件
- frm文件

## 4 表

- 索引组织表

  在innodb存储引擎中，表都是根据主键顺序存放的。如果一个表没有显示的声明主键，则innodb会自动确定一个主键。

  主键的确定规则如下：
  - 首先判断表中是否有*非空*的*唯一索引*，如果有，则该列即为主键
    - 而当表中存在多个符合条件的列时，选择*第一个非空的唯一索引列*
  - 如果没有符合的列，innodb会自动创建一个6字节大小的指针

  *_rowid*仅对于单个int类型的主键起作用，其他的情况无法使用。

- innodb逻辑存储结构

  层级关系: 表空间(tablespace) -> 段(segment) -> 区(extent) -> 页(page) 

  - 表空间

    表空间可以理解为InnoDB存储引擎逻辑结构的最高层，所有的数据存放在表空间内。
    
    可以启用*innodb_file_per_table*，则每张表内的数据可以单独放到一个表空间内。不过需要注意的是，即使启用了*innodb_file_per_table*每张表的表空间内存放的只是*数据、索引和插入缓冲页*。*其他的数据，如undo信息，插入缓冲索引页、系统事物信息、二次写缓冲*等还是存放在共享表空间中。

  - 段
    常见的段有:
    - 数据段: b+树的叶子节点
    - 索引段: b+树的非叶子节点
    - 回滚段: 

  - 区
    区是由连续的页组成的空间，在任何情况下每个区的大小都是1MB。为了保证区中页的连续性，InnoDB存储引擎一次从磁盘申请4-5个区。在默认情况下，InnoDB存储引擎页的大小为16K，即一个区中一共有64个连续页。

  - 页

    页是InnoDB磁盘管理的最小单位，默认页的大小为16kb。也可以通过*innodb_page_size*进行调整。

    常见的页种类
    - 数据页
    - undo页
    - 系统页
    - 事务数据页
    - 插入缓冲位图页
    - 插入缓冲空闲列表页
    - 未压缩的二进制大对象页
    - 压缩的二进制大对象页
  
  - 行
    InnoDB存储引擎是面向列的，也就是说数据是按行进行存放的。（TODO: 了解一下）

- 约束
  对于*primary key*和*unique key*来说，创建索引就是创建约束。区别在于索引和约束的概念不同，约束是一个逻辑的概念，而索引是一个数据结构，既有逻辑上的概念，在数据库中还代表物理存储的方式。

  - 数据完整性
    InnoDB提供的约束: 
    - primary key
    - Unique key
    - Foreign key
    - Default
  
  - 外键约束
    一般来所，称被引用的表为父表，引用的表为子表。外键定义时*on delete*和*on update*表示在对父表进行*delete*和*update*操作时，对子表所做的操作，可定义的子表操作有：
    - cascade: 表示当父表发生delete和update操作时，对相应的子表中的数据也进行delete和update操作
    - set null: 表示当父表发生delete和update操作时，相应的子表中的数据被设置为NULL，但子表中的对应列必须允许为null值
    - no action: 表示当父表发生delete和update操作时，抛出错误，不允许这类操作
    - restrict: 表示当父表发生delete和update操作时，抛出错误，不允许这类操作

    > 如果为显示设置*on delete*和*on update*，则*restrict*为默认设置。

- 视图
  pass

- 分区表
  
  水平分区: 将同一表中不同行的记录分配到不同的物理文件中

  垂直分区: 讲同一表中不同列的记录分配到不同的物理文件中

  全局分区: 数据存放在各个分区中，但是所有数据的索引存放在一个对象中。

  局部分区: 一个分区中既存放了数据又存放了索引

  mysql属于*水平分区*和*局部分区*

  分区类型
  - range
  - list
  - hash
  - key
  - column

  null值的处理：
  - range/hash/key都是讲null值放入第一个分区
  - list需要显示的指定null值放在那个分区
