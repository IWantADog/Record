# About Volumes

## Basic

`volumes`可以使数据在不同的pod之间共享。__`volumes`并不像pod一样是k8s的资源，它是pod的一部分，并且与pod拥有相同的生命周期。也就说，当pod被删除是volume也会被删除，当pod重启时，还可以拿到之前pod操作的数据。__

一个pod中的任意容器都可以使用`volumes`，不过使用之前需要先将`volumes`挂载到指定的`container`。

## volumes的种类

- emptyDir: 空文件
    > `medium: Memory`将文件存储在内存而不是文件系统中。
- hostPath: 挂载`work node`的文件系统到`pod`上。
- gitRepo: git仓库。本质上是在`emptyDir`上的扩展，首先clone一个git repo，再切换到指定的分支上。
    > volume中的git repo不会主动更新。每次新建pod，才会拉取新数据。
- nfs: 共享nfs挂载到pod
- gcePersistentDisk: google提供的持久化硬盘
- awsElasticBlockStore: aws提供的持久化硬盘
- azureDisk: azure提供的持久化硬盘
- 一些没听过的网络资源挂载
    - cinder
    - cephfs
    - iscsi
    - flocker
    - glusterfs
    - quobyte
    - rbd
    - flexVolume
    - vsphere-Volume
    - photonPersistentDisk
- 一些可挂载的k8s集群信息
    - configMap
    - secret
    - downwardAPI
- persistentVolumeClaim: a way to use a pre- or dynamically provisioned persistent storage.


## hostPath

将`work node`的文件系统挂载到该node上的pod上。

`hostPath`是一种**持久化**的存储方式。它不同于`emptyDir` & `gitRepo`，即使pod被删除数据仍然存在。新建的pod如果被 __分配到相同的node且挂载在相同的volumes__，可以访问之前pod留下的数据。

虽然是一种持久化的数据存储方式，但这种方式是对node敏感的，即新的pod必须分配到指定的node上才能拿到指定的数据，数据与node是紧密绑定的。

> hostPath只应该在读取系统文件的时候被使用。不应该用来在不同的pod之间共享数据。

## google、aws、azure
云服务商提供的持久化数据存储方式，的确好用。不过也造成了pod与特定的k8s集群绑定，因为使用不同持久化存储技术的pod在不同的云平台上是不兼容的。

## sidecar container

对于想要保证git仓库实时更新的需求，可以通过使用`sidecar container`来实现。

由于保证git仓库实时更新的逻辑与业务逻辑无关，所以它不应该放在运行业务逻辑的container，可以单独使用一个`sidecar`容器来保证数据是最新的。
