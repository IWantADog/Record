# about explain

## join type

按照从好到坏的顺序排列

- system: 这个表仅有一行数据, 且表为系统表。system时const的一种类型
- const: 最多获取一行数据，并且该数据需要通过*完整主键*或*唯一索引*的获取。
- eq_ref: 获取一行数据，该表是个关联表，并且通过*完整主键*或*唯一且非空索引*获取数据。
- ref: 不论作为关联表还是作为主表，通过*不完整的索引*或*非主键*或*唯一索引*。一句还概括就是，通过给定的查找条件，能够获取到的数据有多行。
- fulltext: 全文索引
- ref_or_null: 类似于*ref*，不过额外增加了对null值列的查找
- index_merge: 表明*index merge optimization*被启用。表明查询中使用了多个独立的索引。*一般这种情况出现表明索引设计的有问题*
- unique_subquery: 
- index_subquery: 类似于*unique_subquery*，不过在子查询中使用的查询条件使用的不是唯一索引
- range: 通过*索引*进行范围查找。当使用`=, <>, >, >=, <, <=, is null, <=>, between, like, in`时都有可能使用range。当出现range时，ref为null。
- index: 扫描全表。有两种情况会出现
  - 查询中可以使用覆盖索引查询需要的数据
  - 扫描全表，需要使用索引进行排序。
- all: 没有索引的全表扫描，应当尽量避免

## extra information

较常见
- *using filesort*: 使用文件排序
- *using index*: 通过索引就能获取需要的数据，不用额外访问data page
- *using MRR*: 使用了MRR（Multi-Range Read）
- *using temporary*: 是否使用临时表
- *using where*: 是否使用where

不常见
- *backward index scan*: 优化器在Innodb表上使用index进行升序排序
- *child of table pushed join@1*: NDB相关（TODO:）
- *const row not found*: 搜索空表
- *deleting all rows*: 
- *distinct*: TODO: 无法触发
- *FirstMatch*: 启用[semigion](https://dev.mysql.com/doc/refman/5.6/en/semijoins.html)
- *Full scan on Null key*: TODO:
- *impossible having*: having的判断条件总是为false，无法获取数据
  - explain select * from table group by primary_key having primary_key is null\G;
- *impossible where*: where的判断条件总为false，无法获取数据
  - explain select * from table where primary_key is null\G;
- *impossible where noticed after reading const tables*: TODO:
- *LooseScan(m .. n)*: TODO:
- *no matching min/max row*: 无法根据where过滤后的数据进行min/max运算
- *no matching in const table*: 搜索的表为空或者根据where无法在索引上获取数据
- *no matching rows after partition pruning*: 通过分区后，没有找到数据可delete和update
- *no table used*:
- *no exist*:  
