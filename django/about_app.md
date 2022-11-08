# about app

- django中每个app都是独立的，功能完全独立。
- 如果需要配置一个app，可以在一个app下创建一个app.py文件，并且定义一个 `AppConfig` 子类。
  - app.py的名字并不一定是固定的。使用`app.py`
  - 每个AppConfig的子类都可以指定一个name，不过必须全局唯一
