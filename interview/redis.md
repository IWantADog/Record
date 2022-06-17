# redis

## redis的优缺点

redis速度快

## redis的主要用途

作为缓存，消息队列

## redis常用数据类型

string

散列

列表

集合

有序集合

## redis的持久化，各自功能、特点及使用场景

快照持久化

根据配置文件，当满足条件时对数据库进行备份。快照持久化使用的子进程对数据进行备份，当数据量过大时会花费大量时间，可能会导致停顿。

快照持久化只适用于丢失一部分数据没有关系的应用。

AOF持久化

AOF持久化是将所有的被执行的写命令写入文件中。AOF不会造成数据的丢失。

不过AOF的备份文件可能会无限增大，当redis重新启动时可能花费大量时间。

不过redis提供了`BGREWRITEAOF`命令用来重写AOF文件，以此减少AOF文件的大小。

## Pipeline

## redis同步机制

## redis事务

## Redis Sentinal && Redis Cluster
