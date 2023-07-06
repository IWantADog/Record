# 大数据平台基础架构指南

## 大数据平台的两种建设路径

1. 垂直业务领域一站到底的建设方式。针对具体的业务场景，有针对性地开发所需要的服务。
2. 通用组件建设，组合支撑业务的方式。针对抽象的通用功能需求，分别构建独立的系统或服务，并通过各个系统和服务的叠加配合，来完成各类业务场景的支撑。

第一种，为业务定制服务，会导致服务不通用，后续难以迭代和扩展。
第二种，考虑通用化，会有服务设计难度大，推进缓慢的问题，不过如果能够顺利开发完毕，并且设计合理的话，带来的收益会更高。

第一种和第二种各有优势，还是需要结合业务紧急程度、压力等问题进行抉择。并非第二种就绝对优于第一种，首要的是为用户解决问题。必要时候可以两者结合起来。

## 服务意识和产品意识的培养

用户需要的究竟是什么？
- 存储
- 计算
- 查询

没有目标的攻坚工作，坚决不做

简单点就是，带着具体的业务的痛点来做开发，在此基础上考虑如何构建通用的解决方案来适配其他业务。采用“通用+适度”定制的方式快速平台的构建，不怕做的不够通用，就怕通用到过于抽象，没有业务可以快速适配。

向上管理

真正站在用户的角度来设计产品，而不是站在开发者的角度来设计产品。

不仅仅在一件事情的内部思考权衡，还需要在外部进行横向比较。比如并不能仅仅思考`“是什么”，“能不能做”，“怎么做”`。而要去思考，`“为什么一定要怎么做”，“有没有其他的解决方案”`。更应该去思考，`“这样做值的吗”，“做点别的事是不是收益更高”`。


## 数据采集、传输、交换、同步服务

异构数据库，将数据在不同的数据库之间进行同步，充分发挥不同数据库的优势。

数据之间的同步不一定仅仅靠脚本，说不定有现成、优秀的工具。

## 方法论

注意方法论的培养，注重提升解决问题能力的普适性。