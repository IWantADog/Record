# About Service

由于pod的易变性、动态扩展通过ip直连pod十分麻烦。而`Service`的使用就是为了解决这个问题。

所有的`Service`都有固定的`ip`和`port`。当`client`需要连接pod时，直接访问`service`，再由`service`将请求转移到某个`pod`。

## related command

kubectl expose

kubectl get svc

kubectl exec



