# Contextual/Thread-local Sessions

[offical document](https://docs.sqlalchemy.org/en/14/orm/contextual.html)

## basic

1. A `scoped_session` is constructed by calling it, passing it a factory which can create new `Session` objects.
    ```py
    from sqlalchemy.orm import scoped_session
    from sqlalchemy.orm import sessionmaker

    session_factory = sessionmaker(bind=some_engine)
    Session = scoped_session(session_factory)
    ```
    > 将 `sesssion_factory` 传入 `scoped_session` 中，获取 `scoped session object`

2. The `scoped_session object` we’ve created will now call upon the `sessionmaker` when we “call” the registry:
    ```py
    some_session = Session()
    ```
    > 直接调用 `scopted session object` 会返回一个 `session` instance

3. 多次调用 `scoped session object` 返回的是相同的 `session instance`

4. The `scoped_session.remove()` method first calls `Session.close()` on the `current Session`, which has the effect of releasing any connection/transactional resources owned by the Session first, then discarding the Session itself. __“Releasing” here means that connections are returned to their connection pool and any transactional state is rolled back, ultimately using the rollback() method of the underlying DBAPI connection__.
    > 通过 `scopted_session.remove()` 释放当前使用的 `session`。释放意味着所有数据库连接归还连接池并且所有事务回滚。

## Thread-Local Scope

We call this notion `thread local storage`, which means, a special object is used that will maintain a distinct object per each application thread. Python provides this via the `threading.local()` construct. The `scoped_session` object by default uses this object as storage, so that a single `Session` is maintained for all who call upon the `scoped_session` registry, but only within the scope of a single thread. Callers who call upon the registry in a different thread get a Session instance that is local to that other thread.

> 对于多线程的应用，sqlalchemy会为每个线程分配一个 `Session`，通过 `threading.local()` 存储。

The `scoped_session.remove()` method, as always, removes the current Session associated with the thread, if any. __However, one advantage of the `threading.local()` object is that if the application thread itself ends, the “storage” for that thread is also garbage collected.__ So it is in fact “safe” to use thread local scope with an application that spawns and tears down threads, without the need to call `scoped_session.remove()`.

> `threading.local()` 当线程结束时会被垃圾回收机制回收，

## Using Thread-Local Scope with Web Applications

[Using Thread-local Scope with Web Applications](https://docs.sqlalchemy.org/en/14/orm/contextual.html#using-thread-local-scope-with-web-applications)





