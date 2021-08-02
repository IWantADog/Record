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






