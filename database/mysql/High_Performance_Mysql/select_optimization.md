# 查询性能优化

1. 仅获取需要的数据
2. 从扫描数据行数和返回的数据行数的角度思考问题

## mysql查询执行的基础

<img src='../statistic/mysql_sql_process.png'>

sql -> 查询缓存 -> 语法解析和预处理 -> 查询优化器 -> 生成执行计划 -> 存储引擎 -> 生成结果

- mysql客户端与服务器之间的通信协议是`半双工`的，这意味着，在任何一个时刻，要么是由服务器向客户端发送数据，要么是由客户端向服务器发送数据。

mysql缓存是否常用？TODO:

### MySQL如何执行关联查询

mysql对于任务`关联`都执行`嵌套循环关联`操作，即mysql先在一个表中循环取出单条数据，然后再嵌套循环到下一个表中寻找匹配的行，依次下去，直到找到所有表中匹配的行为为止。然后根据各个表匹配的行，返回查询中需要的各个列。mysql会尝试在最后一个关联表中找到所有匹配的行，如果最后一个联表无法找到更多的行以后，mysql返回到上一层次关联表，看是否能够找到更多的匹配记录，依此类推迭代执行。

> 关联的概念: 实际指所有的查询(从单表、从临时表、UNION不同结果之间、子查询)

```伪码
select tbl1.col1, tbl2.col2
from tbl2 inner join tbl2 using(col3)
where tbl1.col in (5,6)

<!-- 等价于 -->

outer_iter = iterator over tbl1 where col1 in (5,6)
outer_row = outer_iter.next
while outer_row
    inner_iter = iterator over tbl2 where col3=outer_row.col3
    inner_row = inner_iter.next

    while inner_now
        output [out_row.col1, inner_row.col2]
        inner_row = inner_iter.next
    end

    outer_row = outer_iter.next
end
```

```伪码
<!-- 外连接 -->
select tbl1.col1, tbl2.col2
from tbl1 left outer join tbl2 using(col3)
where tbl1.col1 in (5, 6)

<!-- 等价于 -->

outer_iter = iterator over tbl1 where col1 in (5,6)
outer_row = outer_iter.next
while outer_row
    inner_iter = iterator over tbl2 where col3=outer_row.col3
    inner_row = inner_iter.next

    if inner_row:
        while inner_now
            output [out_row.col1, inner_row.col2]
            inner_row = inner_iter.next
        end
    else:
        output [out_row.col1, NULL]
    end

    outer_row = outer_iter.next
end
```

### 排序优化

无论如何排序的成本都比较高，如果可以应当避免。

mysql排序（filesort）的内部实现逻辑:
- 如果需要排序的数据量小于`排序缓冲区`，mysql使用内存进行排序；如果内存不够排序，mysql会先将数据分块，对每个独立的块进行排序，并将每个块的排序结果存放在磁盘上，然后对每个排好序的块进行合并，最后返回排序结果。
- 单次传输排序: 先读取查询需要的列，然后再根据给定列进行排序，最后直接返回排序结果。不过需要注意，如果查询的列很多且很大时，排序过程中会使用大量的空间。

> 这也意味着：如果查询的列数量较多时且大多数列不参与排序时，可以考虑使用**延迟关联**的方式，较少排序使用过的内存

### 优化limit分页

- 尽可能地使用索引覆盖扫描，而不是查询所有的列。然后再做一次关联操作返回所需的列
- 记录上次查询的游标，翻页时传入该游标。不过这需要表中存在一列用于排序和比较（例如自增的主键）

> 感觉方法2的使用场景很有限，如果排序的字段有多个，将无法选取合适的游标列

### 优化UNION查询
- mysql总是通过创建并填充`临时表`的方式来执行UNION查询
- `UNION ALL`的执行效率优于`UNION`。因为`UNION`相比`UNION ALL`会额外对临时表做`唯一性检查`

