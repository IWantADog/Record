# automatic scaling pod and nodes

## 横向扩展pod

HorizontalPodAutoscaler(HPA)
  
周期性监控所辖的pod的各种指标；与设置的指标进行比对；修改pod数量

- 周期性监控所辖的pod的各种指标
  - 数据采集流程: pods -> cAdvisor(s) -> Heapster -> HPA(S)  
  - autoscaler的输入输出：接受多种数据，计算之后得出一个int（pod的数量）。
  - 对于多个指标，Autoscaler会分别计算各自的指标。计算出满足各种指标所需的pod的数量。之后取最大的那个。

### 基于cpu指标的扩张

- autoscaler基于cpu的扩张需要使用request(计算实际使用的cpu和request的比例)
- “kubectl autoscale deployment kubia --cpu-percent=30 --min=1 --max=5”
- 