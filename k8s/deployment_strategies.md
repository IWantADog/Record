# Deployment Strategies

- recreate
  - 立即删除`所有旧pod`，之后再创建`新pod`。

- rolling up
  - 滚动更新。当`新pod`能够处理请求之后再删除`旧pod`。

- blue/green
  - 主要目的：同时并存新旧两个版本，但仅有一个版本接受真实流量。发布的新版本再未测试完全时，仅接受测试请求，不处理真实请求。当新版本测试完成之后，将所有的流量切换到新版本，并且废弃旧版本。

- canary
  - 主要目的：对于有风险的功能，采用`canary`。当突然出现问题时，可以及时回滚版本。

- A/B testing
  - 主要目的：通过对比 `A/B变量` 相应的统计数据，从`A/B`中找出最优解。
  - 确保单一变量
  - 应用的范畴更广

## reference

https://blog.container-solutions.com/kubernetes-deployment-strategies

https://en.wikipedia.org/wiki/Blue-green_deployment

https://en.wikipedia.org/wiki/Feature_toggle

https://en.wikipedia.org/wiki/A/B_testing