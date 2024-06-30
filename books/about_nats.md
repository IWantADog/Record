# about nats

## 主要概念

### subject

两种通配符。

`*`

- time.*.east可以匹配time.us.east和time.eu.east
- *可以在subject中出现多次。例如`*.*.east`

`>`

- `>`能够同时匹配一个和多个字符，且只能放在subject的末尾。例如time.us.>能够匹配time.us.east和time.us.east.atlanta。
- `>.`可以匹配所有信息

### pub & sub

*message的构成*
1. subject
2. 携带的信息
3. 任意数量的header信息
4. 一个可选的reply地址字段

> message存在一个容量上限，可以通过配置中的`max_payload`进行调整。默认是1MB，可以最大提升到64MB。官方建议保持message的上限不超过8M

### request-reply

请求响应模式。双向的pub/sub。

类似于pub/sub，而且底层也是使用pub/sub进行实现。

定义一个subject。replay/request都即是publisher，也是subscriber。replay接受到request之后会向request发消息。

思考？
- 有什么可用的场景吗？

### queue

- 广播。订阅同一个subject的所有subscriber都会收到消息。
- 消费者组。一条信息仅会发给，同一个queue的一个消费者。
  - queue能否保证数据的有序性（无法保证）

queue的name也支持和subject相同的通配符概念，这个如何理解？有什么使用场景？TODO:

### jetStream

jetStream是nats中的一个持久化引擎。

stream：发布者和订阅者之间的时间解耦

#### Replay policies (响应策略)

- instant: 尽可能快的发送消息
- original: 发送消息的频率和接受到消息的频率一样。
- 回复消息从给定的序列号开始
- 回复消息从给定的时间点开始

#### 保留策略和限制

stream相关的限制方式，避免消息无限增加。

- 消息存储的时间
- 消息的总容量（bytes)
- 消息的总数量
- 单个消息的最大字节
- 限制消费者的数量

废弃策略：指当任意一种以上的限制达到之后，stream改如何处理新接受的消息。有以下2种方式。
1. 删除旧消息
2. 删除新消息，并报错

信息保留策略
1. limits策略。
2. 额外限制策略。额外策略对于消息处理的优先级低于limit策略，简单讲就是，如果满足了limit策略，即使额外策略没有满足，消息也会被删除。
  - interest: 当前所有存活的consumer都ack消息之后，stream中的消息会被立即删除。
  - work queue: 一个消息只会被消费一次，消息被ack之后立即被删除。对于一个subject 一个queue中最多只能有一个consumer。创建第二个consumer会报错。

消息去重
- 在消息的header中增加*Nats-Msg-Id*.
- 并且设置*dupe-window*配置


source & mirrors

信息内部分发

#### 不太关注的feature

- key/value store: k-v存储。底层使用stream存储数据。jetstream额外的功能
- object存储

### consumer

消费stream的数据子集，并记录发送了那些消息，那些消息被ack了，那些消息没有被ack（处于pending状态）

#### 接受message的方式 push/pull

push: nats server主动向client发送数据。官方更推荐push + ephemeral搭配进行使用（对数据的丢失容忍度高的场景）。对于数据丢失容忍度低的场景，还是优先使用pull模式

#### consumer持久化策略

- ephemeral: 数据存储在内存中，当consumer长时间没有被订阅，数据会被删除。
- durable: 数据会保存在集群中。

#### consumer配置项

*消费者ack策略*
> 如果ack是必须的，但是一条消息在给定的AckWait没有被ack，这条消息会被重发（且可能发送给不同的消费者）。

- explicit: 每条消息分别被ack。
- none: 消息不需要被ack
- all: 如果接受到批量的信息，只需要ack最后一条信息，这个消息之前的所有信息会在同一时间被自动ack。

*消息发送策略*

- DeliverAll: 发送现有的所有数据
- DeliverLast: 发送订阅的subject中的最后一条数据
- DeliverLastPerSubject: 发送订阅的每个subject的最后一条数据
- DeliverNew: 仅仅发送新数据
- DeliverByStartSequence:
- DeliverByStartTime: 

*最大Ack等待数量*

定义消息未被完成的最大数量。如果数量达到限制，消息发送会被阻塞。

- MaxAckPending同时对push/pull consumer生效。
- 对于消息的吞吐量比较高。可以适当提升MaxAckPending的值。
- 如果消息处理的比较慢，可以适当降低MaxAckPending的值，并且AckWait从而避免消息重发。


### subject mapping和分片

支持对subject进行分离，并提取子字符串，或调整token的位置。

```sh
// bar.a.b -> baz.b.a
nats server mapping "bar.*.*"  "baz.{{wildcard(2)}}.{{wildcard(1)}}"
```

####  Deterministic Subject token Partitioning

NOTE: nats提供了queue的概念，不过需要注意的是，在同一个queue中所有的client消息的分配是随机的，例如对应同一个用户的信息，可能会发送给不同的消费者进行处理。在对事件顺序有要求的场景就不适应了。

nats提供了根据subject token进行hash。之后再进行分片的处理。是否支持根据给定的信息进行处理？例如用户id，不过这个通过业务处理也是可以，直接对需要分区的维度进行hash然后取模就可以了。

感觉这个地方没有kafka灵活。TODO: 深入了解下kafka。


#### 权重映射(weight mapping)

可以作用于a/b test或者蓝绿发布。将事件按权重分配到不同的subject

### ~~nats service Infrastructure（nats基础服务）~~


## docker compose

```yaml
version: '2'

services:
  nats:
    image: 'bitnami/nats:latest'
    ports:
      - 4222:4222
      - 6222:6222
      - 8222:8222
    environment:
      NATS_EXTRA_ARGS: "-js"
```