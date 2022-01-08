# how to use readiness and liveness prode

- 在开始探针验证之前，设置合适的等待时间，避免陷入`部署->重启`的死循环。
  > https://blog.colinbreck.com/kubernetes-liveness-and-readiness-probes-how-to-avoid-shooting-yourself-in-the-foot/#fnref1

- 并不是一定要同时使用`readiness` & `liveness` probe。需要根据实际的应用实现，进行判断。
- `livness probe`失败时容器会被重启
- `readiness probe`失败时pod会被移除`load balancer`，不再接受流量。
  > https://developers.redhat.com/blog/2020/11/10/you-probably-need-liveness-and-readiness-probes#what_are_liveness_probes_for_

