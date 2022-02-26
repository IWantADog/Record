# python import

`import`实际的操作分为两步。1) 搜索给定的moduel，具体的搜索逻辑位于`__import__`. 2) 将搜索到的model绑定到变量名上。

如果一个module是被第一次搜索，则会实例化一个module object。如果无法发现，则报`ModuleNotFoundError`。

如果module已被import过，则会缓存在`sys.module`中。这会造成一旦import一个module，后续对该module的import获取的都是第一次生成的module实例。
  > `sys.module`实际是一个dict。（key为module名，value为module实例）

## 在代码中调用import

- importlib.import_module

## 关于packages

- python仅拥有一种`module type`，所有的modele都是同一种类型。
- 为了管理module引入了package的概念
- package也是一种module
  > 所有的package都是moduel，但module并不一定是package。

## 关于module搜索

当导入一个模块时，python的搜索逻辑
1. sys.module，存储所有已经被import过的module。
2. python standard library
  - python官方提供的模块
3. sys.path
  - 安装的依赖和本地的项目等
  - 通过`PYTHONPATH`可修改

## reference

[python import](https://docs.python.org/3.7/reference/import.htmls)

[python importlib](https://docs.python.org/3/library/importlib.html#module-importlib)
