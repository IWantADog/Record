# 数据库系统概论笔记

通过简明、准确的语言记录数据库知识中的关键点。

## 基本sql

理解一条查询的方法：先from，在where，最后select。可以这样理解，但sql底层并不这样实现。

### 自然连接

- 两个关系 __相同的属性__ __取值相同__ 的元组对。
- 自然连接默认校验所有相同的属性。可使用`using`指定属性。

### 集合运算

- 并集: union
- 交集: intersect
- 差集: except

> 集合运算`默认去重`

### 空值

空值也可做逻辑运算

- and: true and unknown -> unknown; false and unknown -> false; unknown and unknown -> unknown
- or: true or unknown -> true; false or unknown -> unknown; unknown or unknown -> unknown;
- not: not unknown -> unknown;

如果元组在所有属性中取值相同，那么它们就被当作相同元组，__即使某些值为空__。

### 聚合函数

- 没有group by时认为所有的元组为一个分组
- 使用group by时将元组分为不同的分组
- 聚合函数作用于分组上
- 使用 __having__ 过滤分组
- __聚合函数除`count`外默认忽略空值。由于忽略空值导致可能出现空集。规定对于空集的`count`计算为0，其他所有的聚合运算在输入为空集的情况下返回一个空值__

### 如何理解`group by`和`having`的使用

1. form算出一个关系
2. where过滤
3. group by 分组
4. having过滤
5. select选择需要的字段

### `in` and `not in`

__多属性的成员资格测试__。

```sql
select count(distinct id)
from tasks
where (c, s, se, y) in (
    select c, s, se,y
    from t
    where t.a=1000
);
```

### some && all

`some`代表

`all`代表

### exist && no exist

检测一个子查询的结果中是否存在元组

### where子查询、from子查询、标量子查询

- `where`子查询：可以使用外层查询的相关的名称（这称为 __相关子查询__ ）。
- `from`子查询：不能使用外层的查询的相关名称。(有个 *lateral* 关键字不过许多数据库都未支持)
- 标量子查询：标量子查询的结果必须为 __单一属性__ 的 __单一元组__。标量子查询可用在返回单个表达式能够出现的任何地方，例如`select` & `where` & `having`。

### with

用于定义临时关系，十分有用。

```sql
with emp1(arg1, arg2) as (
    select arg1, arg2
    from table1
    where conditions1
), emp2(arg3, arg4) as (
    select arg3, arg4
    from table2
    where condition2
);
```

## 中级sql

### 外连接

__外连接通过创建空值元组的方式，保留在连接中丢失的元组。__

为了与外连接进行区分。不保留空值元组的连接运算被成为`内连接`

左外连接的操作过程：

1. 首先进行内连接
2. 对于内连接左侧中任意一个与右侧元组都不匹配的元组t，向连接结果中加入一个元组r，r的结构如下：元组r从左侧获取t的值；r的其他属性被赋为空值。

`on`与`where`的区别

`on`是外连接的一部分，外连接会为那些对相应内连接结果没有贡献的元组补上空值并加入结果。而`where`会过滤所有不符合表达式的元组。

### 视图

- 视图返回的数据是调用时计算的，视图并不存储数据。
- 通过视图可以隐藏实际的表结构。对于控制某些数据不可见，可以通过提供视图来实现。

```sql
create view test_view as 
select arg1, arg2
from table1

-- 显式指定视图属性名

create view test_view_2(arg1, arg2) as
select arg1, arg2
from table2
```

#### 物化视图

物化视图是 __指将视图的实际结果存储在数据库中，同时保证当用于定义视图的关系改变时，视图同步被更新。__

__不要尝试通过视图想数据库插入数据。__

### 事务

实现多个更新语句的原子性。所有的语句要么全部执行成功，要么全部影响彻底被取消。

### 完整性约束

- NOT NULL - 指示某列不能存储 NULL 值。
- UNIQUE - 保证某列的每行必须有唯一的值。也可同时对多个属性增加唯一性约束。
- PRIMARY KEY - NOT NULL 和 UNIQUE 的结合。确保某列（或两个列多个列的结合）有唯一标识，有助于更容易更快速地找到表中的一个特定的记录。
- FOREIGN KEY - 保证一个表中的数据匹配另一个表中的值的参照完整性。子表中的外键一定对应主表的主键，并且外键的值一定在主表中存在。
- CHECK - 保证列中的值符合指定的条件。
- DEFAULT - 规定没有给列赋值时的默认值。

#### 事务中对完整性约束的违反

在事务的中间步骤可能存在对完整性约束的违反，不过事务结束后完整性约束又会被满足。

为了处理这样的情况，sql标准允许将`initially deferred`加入约束声明。这样完整性约束不是在事务的中间步骤上检查，而是在事务结束后被检查。

__一个约束可以被指定为`可延迟的`，这意味着默认情况下它会被立即检查，但是在需要的时候可以延迟检查。__

### 索引

在关系上创建的索引是一种数据结构，__它允许数据库高效地找到关系中那些在索引属性中取得定值的元组，而不用扫描关系中的所有元组。__

```sql
create index studentID_index on student(ID);
```

### 大数据对象

`clob` & `blob`

### 用户定义的类型

__现实中将一个以美元表示的货币与一个以英镑表示的货币进行比较几乎可以肯定是错误的。__ 一个好的类型系统应该能检查这类赋值和比较。为了支持这种检测，sql提供了 __独特类型(distinct type)__。

```sql
-- 创建
create type Dollars as numeric(12, 2) final;
create type Pounds as numeric(12,2) final;

-- 删除
drop type

-- 修改
alter type
```

域(domain)，它可以在类型上增加完整性约束。

```sql
create domain DDollars as numeric(12, 2) not null;
```

域的特点

1. 在域上可以声明约束，例如`not null`，也可以为域类型变量定义默认值。
2. 域不是强类型的。因此一个域的值可以被赋给另一个域，只要他们的基本类型是相同的。

```sql
create domain YearkSalary numeric(8,2)
    constraint salary_value_test check(value >= 2900000);
```

### create table扩展

`create table ... like ..` & `create table ... as ...`

根据现有的表创建一个完全相同的表。

```sql
create table temp_table1 like table1
```

将查询的结果存储为一张表。

```sql
create table t1 as(
    select *
    from table1
    where condition
) with data;
```

### 目录(catalog)、模式(schema)

[mysql and postgresql catalog and schema](https://stackoverflow.com/questions/7942520/relationship-between-catalog-schema-user-and-database-instance)

### 权限的授予

__一个创建了新关系的用户将自动被授予该关系上的所有权限。__

```sql
-- create privileges

grant <权限列表>
on <关系名或视图名>
to <用户/角色列表>

-- revoke privileges

revoke <权限列表>
on <关系名或视图名>
to <用户/角色列表>
```

SQL的授权机制，允许 __对整个关系授权__ 或 __一个关系的指定属性授权__。但是，它 __不允许__ __对一个关系的指定元组授权__。

### 角色

角色可以简单理解为权限的集合。

如果某类用户拥有的权限比较复杂，每次创建新用户时都需要执行重复的操作。__一种更好的方式是，将一些权限分配给角色(role)，并角色授予用户__。

```sql
-- create role
create role role1

-- grant privileges to role

grant select on table1 to role1;
```

关键点

1. 用户可以被授予角色
2. 角色也可被授予角色
3. 一个 __用户/角色__ 拥有的权限包含
    - 所有直接授予给 __用户/角色__ 的权限。
    - 所有授予给 __用户/角色__ 所拥有的角色的权限。

### 视图的授权

1. 创建视图不需要获得该视图对应关系上的所有权限。
2. __用户对于视图的权限取决于用户在关系上的权限__
3. 如果一个用户在某个视图上不能获得任何权限，系统会拒绝这样的视图创建请求。

### 权限的转移

__默认情况下，被授予权限的用户/角色无权把得到的权限授予给其他用户/角色。__

如果我们在授权时允许接受者把得到的权限再传递给其他用户，可以在相应的`grant`命令后面附件`with grant option`子句。

__理解授权图的概念__。用户为节点，权限的授予为边。例如u1授予u4权限，则表现为`u1 -> u4`，所有的节点和边构成了一个授权图。图的根结点为数据库管理员。

当判断一个用户是否具有权限的充分必要条件是：__当且仅当存在从授权图的根到用户的节点的路径。__

```sql
grant select on table1 to user1 with grant option;
```

### 权限的回收

1. 权限的回收默认是级联的，即用户授予他人的权限在该用户权限被回收时，也同时会被回收。

    级联回收是默认的，也可通过`cascade`显式指定。

    也可通过`restrict`来防止权限级联回收，当存在任何级联回收时，系统会返回一个错误，阻止级联回收。

    ```sql
        revoke select on table2 from user1 cascade

        revoke select on table1 from user1 restrict
    ```

2. 权限的级联回收在很多情况下是不合适的。

    假定`user1`具有`dean`角色，他将`instructor`授予`user2`，后来`dean`角色从`user1`处回收；`user2`继续被雇佣为教职员工，并且还应该保持`instructor`角色。

    在这种场景下级联回收就不适用。为处理以上这种情况，__SQL允许权限由一个角色授予，而不是通过用户授予__。SQL中有一个与会话关联的`当前角色`的概念。默认情况下，一个会话所关联的当前用户是空的。

    一个会话所关联的当前用户可以通过`set role role_name`来设置。指定的用户必须已经授予给用户，否则`set role`语句执行失败。

    如果做授予权限时将授权人设置为一个会话所关联的当前用户，并且当前用户不为空的话，可以通过在授权命令后加`granted by current_role`.

    通过将授权人设置为`角色`而非`用户`，可以解决上述问题。

## 查询处理

### 查询代价的度量

查询优化器通常努力去尽可能降低查询计划总的资源消耗（主要考虑的有两点：*数据块传输*和*磁盘扫描*），而不是尽可能缩减响应时间。

我们用于估计总的磁盘访问时间（包含寻道和数据传输）的模型，就是这样的基于资源消耗的查询代价模型的实例。

### 排序

对于不能完全放在内存中的关系的排序称为*外排序*。外排序中最常用的技术就是外部排序并归。

### 连接运算

*嵌套循环连接*
- 简单讲就是对于两个连接，使用双层的for循环读取数据。对于外层表中的每一行记录、内层表都需要做一次完整的扫描。
- 而对于其中一个关系的数据能够完全放在内存中，把这个关系放在内层关系中是有好处的。因为这样内层关系只需要读一次。

*块嵌套循环连接*

因缓冲区太小而内存不能完全容纳任何一个关系时，如果我们以块的方式而不是以元组的方式处理关系，仍然可以减少不少块的读写次数。

它是嵌套循环连接的一个变种，其中内层关系中的每一块与外层关系的每一块形成一对。在每个块对中，一个块中的每一个元组与另一块的每一元组形成元组对，得到全体元组对，再把满足连接条件的元组队加入结果中。

