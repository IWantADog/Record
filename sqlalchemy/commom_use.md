# sqlalchemy common use

## Establishing Connectivity - the Engine

### create engine

```sh
>>> from sqlalchemy import create_engine
>>> engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
```

> `in-memory-only`数据库

## Working with Transactions and the DBAPI

### Getting a Connection

```py
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
```

__The default behavior of the Python DBAPI includes that a `transaction` is always in progress; when the scope of the connection is released, a `ROLLBACK` is emitted to end the transaction. The transaction is not committed automatically; when we want to commit data we normally need to call `Connection.commit()` as we’ll see in the next section.__

> 使用python DBAPI默认使用事务处理数据库请求。除非显示使用`commit`，否则事务接受后会`rollback`


`Engin.begin()`。和`Engin.connect()`类似，不过`begin`结束后会自动`commit`

### Basics of Statement Execution

`Result object` 

### how to use session

```py
with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y":11}, {"x": 13, "y": 15}]
    )
    session.commit()
```

> The Session doesn’t actually hold onto the `Connection` object after it ends the transaction. It gets a new `Connection` from the `Engine` when executing SQL against the database is next needed.

## Working with Database Metadata

### Metadata object

Having a single `MetaData` object for an entire application is the most common case, represented as a module-level variable in a single place in an application, often in a “models” or “dbschema” type of package. There can be multiple `MetaData` collections as well, however it’s typically most helpful if a series of `Table` objects that are related to each other belong to a single `MetaData` collection.

> `Metadata`似乎用来存储所有的`table`，通过 `Metadata` 创建表结构。

### Declaring Simple Constraints

```py
# 如何定义外键
Column('user_id', ForeignKey('user_account.id'), nullable=False),
```
> __When using the `ForeignKey` object within a Column definition, we can omit the datatype for that Column;__ it is automatically inferred from that of the related column, in the above example the Integer datatype of the user_account.id column.

### Emitting DDL to the Database

```sh
>>> metadata.create_all(engine)
```
> 通过`metadata`创建所有的表。

[Alembic: base sqlalchemy database migration tool](https://alembic.sqlalchemy.org/en/latest/)

### Defining Table Metadata with the ORM

#### setting up Registry

`registry` & `MetaData` & `ORM Mapped Table`

TODO: 如何理解`registry`。
```py
from sqlalchemy.orm import registry
mapper_registry = registry()
Base = mapper_registry.generate_base()
```

> 通过`registry`，获取`ORM Mapped Table`基类

- tip

    The steps of creating the registry and “declarative base” classes can be combined into one step using the historically familiar `declarative_base()` function:

    ```py
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()
    ```

### Table Reflection

[Reflecting DataBase Objects](https://docs.sqlalchemy.org/en/14/core/reflection.html)

> 通过数据库中已经存在的表，创建`ORM Mapped Table`。

## Working with Data

### Inserting Rows with Core

skip

### Selecting Rows with Core or ORM

`Connection.execute() in Core` and `Session.execute() in ORM`

`Select.join_from()` & `Select.join()`

> `Select.join_from()` method, __which allows us to indicate the left and right side of the JOIN explicitly__

> `Select.join()` method, __which indicates only the right side of the JOIN, the left hand-side is inferred__

Both the `Select.join()` and `Select.join_from()` methods accept keyword arguments `Select.join.isouter` and `Select.join.full` which will render `LEFT OUTER JOIN` and `FULL OUTER JOIN`。


### Aggregate functions with GROUP BY / HAVING

```py
from sqlalchemy import func
```

### use aliases

```py
from sqlalchemy.orm import aliased
```

## Data Manipulation with the ORM

### create a session

```py
session = Session(engine)
```

### Flushing

`Session.flush()` be used to manually push out pending changes to the current transaction,

### Identity Map

__The primary key identity of the objects are significant to the `Session`, as the objects are now linked to this identity in memory using a feature known as the identity map. The identity map is an in-memory store that links all objects currently loaded in memory to their primary key identity. We can observe this by retrieving one of the above objects using the `Session.get()` method, which will return an entry from the identity map if locally present, otherwise emitting a SELECT.__

> a flush occurs automatically before we emit any `SELECT`, using a behavior known as `autoflush`. And we are still in a `transaction` and __our changes have not been pushed to the database’s permanent storage__.

### closing a session

> Try to avoid using objects in their detached state, if possible. When the Session is closed, clean up references to all the previously attached objects as well. __For cases where detached objects are necessary, typically the immediate display of just-committed objects for a web application where the Session is closed before the view is rendered, set the `Session.expire_on_commit` flag to False.__

> `session`触发`commit`后，对象属性的访问是重新从数据库中查询的。可以通过`Session.expire_on_commit`修改这个行为，如果有需要的话。

## Working with Related Objects

### relationship

### Cascading Objects into the Session

> 当一个对象被添加进`session`， 和它相关的对象也会被加入`session`

### Loader Strategies

[loader strategies](https://docs.sqlalchemy.org/en/14/tutorial/orm_related_objects.html#loader-strategies)

[Relationship Loading Techniques](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html)

- selectin load

    [select in loading](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html#select-in-loading)

    > 发送两次查询，第一次获取主表数据，第二次通过返回的主表id，查询子表数据。

    > `selectin`对于 `复合主键` 和 `不支持IN的数据库` 无法使用。 

- join load

    __joinedload() is not a replacement for join()__

    The join created by `joinedload()` is anonymously aliased such that it does not affect the query results. An `Query.order_by()` or `Query.filter()` call cannot reference these aliased tables - so-called “user space” joins are constructed using `Query.join()`. The rationale for this is that `joinedload()` is only applied in order to affect how related objects or collections are loaded as an optimizing detail - it can be added or removed with no impact on actual results.

    > `joinload()` 不是 `join()` 的替代品。 `joinload()` 是对于查询 `many to one` 关系的优化处理。


- Raiseload

    > 对于懒查询，直接报错
