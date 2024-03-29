# 集成

集成: 将一些独立的软件组件组合为一个完整系统。

- 阶段性集成
- 增量集成

## 阶段性集成

阶段性集成可以简单描述: 所有的组件完全开发完成之后，才开始集成。这样在第一次集成时会不可避免的暴露大量问题。

阶段性集成仅适合小型项目。对于大型项目，一下子出现过多的问题，会导致编码者不能有条理的检测和纠正错误。

## 增量集成

增量集成可以简单描述为: 一块一块的编写并测试代码，然后一次一次地将它们拼接起来。

具体步骤如下:
1. 开发一个小功能模块，并进行彻底的测试和调试。并将该功能作为项目的骨架。
2. 设计、编码、测试、调试某个类。
3. 将新开发的类集成到系统骨架上。测试并调试”骨架和新类的结合体“。测试调试完成之后，继续步骤2。

增量测试的好处
1. 易于定位错误。当新引入一个类，调试是出现了错误，那问题大概率出现在新引入的类中。
2. 及早地在项目中取得系统级成果。并能改善对进度的把控。

## 增量集成的策略

- 自顶向下
- 直底向上
- 三明治集成
- 风险导向集成
- 功能导向集成
- T-型集成

> 需要注意，在使用这些策略时不应该生搬硬套，这些更多是启发而非准则。

