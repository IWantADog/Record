# 锁

## Innodb中的锁

[innodb-locking](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html#)

锁的类型

两种标准的*行级锁*
- 共享锁(S Lock)，允许事务读一行数据
- 排他锁(X Lock)，允许事务删除或更新一行数据

xxx | x      | s
----|--------|----
x   | 不兼容  | 不兼容
s   | 不兼容  | 兼容

如果一个事务T1已经获得了行r的共享锁，那么另外的事务T2可以立即获取r的共享锁，因为读取并没有改变行r的数据，这种情况为*锁兼容*。若有其他的事务T3想要获取行r的排他锁，则必须等待事务T1、T2释放行r上的共享锁，这种情况称为*锁不兼容*。

InnoDB还支持一个额外的锁方式，称为*意向锁*。意向锁是将锁定的对象分为多个层次，意向锁意味着事务希望在更细粒度上进行上锁。如果将上锁的对象看为一颗树，那么对最下层的对象上锁，也就是对最细粒度的对象进行上锁，那么首先需要对粗粒度的对象上锁。如果意图对一个细粒度的行上锁，却发现该行所属的表或页已经被上锁，由于锁不兼容，该事务需要等待之前的事务完成。

两种意向锁（*表级别的锁*）
- 意向共享锁（IS lock），事务想要获取一张表中某几行的共享锁
- 意向排他锁（IX lock），事务想要获取一张表中某几行的排他锁

意向锁规定:
- 当一个事务需要对表的一行添加s锁时，该表必须先获取IS锁
- 当一个事务需要对表的一行添加x锁时，该表必须先获取IX锁

xxx | IS     | IX     | S      | X
----|--------|--------|--------|----
IS  | 兼容   | 兼容   | 兼容   | 不兼容
IX  | 兼容   | 兼容   | 不兼容 | 不兼容
S   | 兼容   | 不兼容 | 兼容   | 不兼容
X   | 不兼容 | 不兼容 | 不兼容 | 不兼容

> 需要注意: 意向锁之间是完全兼容

一致性非锁定读

一致性的非锁定读是指InnoDB通过*行多版本控制*的方式读取当前执行时间数据库中行的数据。*如果读取的行正在执行delete或update操作*，这时读取操作不会因此去等待行上锁的释放。相反地，InnoDB存储引擎会去*从undo log中读取行的快照数据*。

非锁定读机制极大的提高了数据库的并发行，InnoDB存储引擎默认使用这种方式，即读取不会占用和等待表上的锁。但是不同的事务隔离级别下，读取数据的方式不同。由此带来的并发控制，称为*MVCC（多版本并发控制）*
- 在*read committed*下，对于快照数据，非一致性读总是读取被锁定行的最新一份快照数据。
- 在*repeatable read*下，对于快照数据，非一致性读总是读取事务开始时的行数据版本。

一致性锁定读

InnoDB对与select语句支持两种一致性的锁定读操作
- select ... for update: 对需要读取的行加一个X锁，其他事务不能对已锁定的行加上任何锁。
- select ... for share: 对读取的行记录加一个S锁，其他事务可以向被锁定的行加S锁，但是如果加X锁，则会被阻塞。
  - 兼容`select ... lock in share mode`

NOWAIT and LOCKED

在使用for update和for share时可以同时使用nowait和skip locked

- nowait: 如果查询的数据行上出现锁不兼容，不等待锁释放，直接报错
- skip locked: 如果查询的数据行上出现锁不兼容，跳过冲突的行，立即返回数据

外键与锁

对于外键值的插入和更新，需要首先查询父表中的记录。但是对于父表的select操作，不是使用一致性非锁定读的方式，因为这样为发生数据不一致的问题，因此这时使用的是`select ... lock in share mode`方式，即*主动对父表加一个s锁*。如果这时父表中已经被加了X锁，子表上的操作会被阻塞。
> 一致性锁定读的使用场景

## 锁的算法

innodb存储引擎中有3中锁的算法：
- Record Lock: 锁定索引上的单行记录。
- Gap Lock: 间隙锁，锁定索引上的一个范围
  - 当一个index gap被添加gap lock，便会阻止其他事务向这个gap插入数据
  - Gap lock的共享锁和排他锁相互兼容
- Next-Key Lock: Gap Lock + Record Lock的组合，锁定索引上的一个范围，并且锁定记录本身

  示例：如果一个索引包含1，2，5，则可以将加锁的区间为 (-inf, 1], (1, 2], (2, 5], (5, +inf)。

- insert intention lock

  insert intention lock是一种gap lock，在插入数据之前被设置。使用这个锁当不同的事务向同一个gap插入不相同数据时，两个插入不会相互等待。

  例如已存在记录4，7，两个事务A，B分别想要插入5和6，此时两个事务不会相互冲突，应为它们插入的数据并不冲突。

InnoDB对于行的查询都采用Next-Key Lock这种方法。Next-key Lock这种加锁算法只要是用来应对[幻读问题](https://dev.mysql.com/doc/refman/8.0/en/innodb-next-key-locking.html)。

> 如果查询的索引含有*唯一属性*时，InnoDB存储引擎会对*Next-Key Lock*进行优化，将其降级为*Record Lock*。

唯一属性降级为Record Lock示例:
```sql
create table t (a int primary key);
insert into t values (1), (2), (5);

-- Session A
select * from t where a=5 for update;

-- session B
insert into t values (4); // ok
```

如果使用`select * from t where a=5 for update;`对a=5的行加锁，由于a是主键且是唯一的，所以锁定的仅是5这个值，而不是（2，5）这个区间。这是在插入a=4的数据是，不会导致阻塞。

非唯一属性使用Next-key Lock示例:
```sql
create table z (a int, b int, primary key (a), key(b));
insert into z values (1,1), (3,1), (5,3), (7,6), (10,8);

-- session A
select * from z where b=3 for update:


-- session B
insert into z values (4,2); // 会被阻塞
insert into z values (6,5); // 会被阻塞

insert into z values (8, 6); // 可以执行
insert into z values (2, 0); // 可以执行
```

如果使用`select * from z where b=3 for update`对b=3的行进行加锁。对于聚集索引会对a=5的索引加*Record Lock*，而对于辅助索引，会对范围(1,3)和(3,6)进行加锁，当向这两个区域插入数据时，sql会被阻塞。

> 如果对范围加锁，例如`select * from z where b>3 for update`则被被加锁的区间为(1,3)和(3, +inf)。

> 若唯一索引有多列组成，而查询仅查找组合索引中的某一列，这样的查询其实依然是range类型查询，而不是point查询。对于这种情况，InnoDB存储引擎依然使用Next-Key Lock进行锁定。

## 锁升级

锁升级是指讲当前锁的粒度降低。举例来说，数据库可以把一个表的1000个行锁升级为一个页锁，或者将页锁升级为表锁。如果在数据库的设计中认为锁是一种稀有资源，而且想要避免锁的开销，那数据库就会频繁出现锁升级现象。

InnoDB存储引擎不存在锁升级的问题，因为其不是根据每个记录来产生锁的，相反，其根据每个事务访问的每个页对锁进行管理，采用的是位图方式。因此不管一个事务锁住页中的一个还是多个记录，其开销通常是一样的。