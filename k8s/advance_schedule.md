# Advance Schedule

## node taints/pod tolerations

- 通过`pod tolerations`和 `node taints`限制pod只能运行在指定的node上。一个pod只能被分配到能够`匹配node taints`的node上。
- pod的tolerations: `<key>=<value>:<effect>`
- taint effect的种类
  - `NoSchedule`: 如果pod的toleration不匹配node的taint，pod不会被分配到该node。
  - `PreferNoSchedule`: `NoSchedule`的宽松版。一般不合适的pod toleration不会分配到该node，除非该pod没有node接受。
  - `NoExecute`: 与`NoSchedule`和`PreferNoSchedule`仅影响为分配的pod不同。如果该node上运行有不匹配的pod，该pod会被驱逐出node。
- 添加自定义`taints`到node
 - kubectl taint node node1.k8s node-type=production:NoSchedule
- 添加tolerations到pod: 通过yaml设置
- node可以拥有多个`taint`
- pod可以拥有多个`toleration`

## 使用node affinity吸引pod到指定的node





