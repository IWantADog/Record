# base

## 基本概念
- Producer: 生产者，发送消息的一方。
- Consumer: 消费者，消费消息的一方。
- Broker: 服务代理结点。对于kafka而言，Broker可以简单地看作一个独立的kafka服务节点或kafka服务实例。

  大多数情况下可以将Broker看作一个Kafka服务器，前提是这个服务器上只有一个kafka实例。一个或多个Broker组成一个Kafka集群。
- Topic: 

  kafka中消息以主题为单位进行归类，生产者负责将消息发送到特定的主题。消费者负责订阅主题并进行消费。
- Partition:

  topic是一个逻辑上的概念。一个主题还可以细分为多个分区，一个分区只属于一个topic。

  **kafka上的分区可以分布在不同的服务器(broker)上，也就是说，一个主题可以横跨多个broker，以此提供比单个broker更强大的性能。**
- offset:

  在存储层面上，一个分区可以被视为一个可追加的日志文件，消息在被追加到分区日子文件的时候都会分配一个特定的偏移量(offset)。

  offset是消息在分区中的唯一标识，kafka通过它来保证消息在分区中的顺序性。不过offset并不跨分区，也就是说，kafka保证offset在分区有序而不是在整个主题有序。

### kafka分区的多副本机制
- 同一个分区的不同副本保存的是相同的消息
- 副本之间是一主多从的关系，其中leader副本负责处理读写请求，follower副本只负责与leader副本的消息同步。
- 副本位于不同的broker中，当leader副本出现故障时，从follower副本中重新选举新的leader副本对外提供服务。
- 一些相关的概念
  - AR(assigned replicas): 所有的副本的统称，包括leader副本
  - ISP(In-Sync Replicas): 所有与leader副本保存一定程度同步的副本（包括leader副本在内）
  - OSP(Out-Of-Sync Replicas): 与leader副本同步滞后过多的副本（不包括leader副本）

  由此可见 AR=ISP + OSP。不过在正常情况下，所有副本都应该与leader副本保存一定程度的同步，即AP=ISP，OSP集合为空

  - HW(High Watermark): 描述一个分区特定的offset，消费者只能拉到这个offset之前的消息。
    - HW保证分区多副本情况下数据的一致性。多个follower副本与leader副本之间的数据同步可能并不一致，此时该分区的HW就是同步数据最少的follower的最大offset+1。

      例如一个分区有1个leader，2个follower。某一时刻，leader中有4份数据，follower_1完全同步了4分数据，follower仅仅同步了3分数据。 则此时的这个分区的HW为4。
  - LEO(Log End Offset): 表示当前日志文件中下一条待写入消息的offset。
