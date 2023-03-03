# about pubsub

## 概念简述

- redis提供两种订阅方式:
  - 订阅单个channel
  - 通过通配符同时订阅多个channel
- pubsub是一种广播机制。所有的订阅者都可以获取相同、全量的数据。
- pubsub不提供消息的持久化。当一个消息到达时，会向当前所有的订阅者发送消息。后续订阅的订阅者无法获取到历史数据。

  当一个消息到达时，如果一个channel没有订阅者，消息就永久丢失了。


TODO:
https://redis.com/ebook/part-2-core-concepts/chapter-6-application-components-in-redis/6-5-pull-messaging/

