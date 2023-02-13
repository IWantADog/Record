# django overview

## app.py

- django中每个app都是独立的，功能完全独立。
- 如果需要配置一个app，可以在一个app下创建一个app.py文件，并且定义一个 `AppConfig` 子类。
  - app.py的名字并不一定是固定的。使用`app.py`
  - 每个AppConfig的子类都可以指定一个name，不过必须全局唯一

## middleware

- [x] how to write a middleware
  - middleware必须是一个可调用类型
  - middleware必须接受一个request对象，并且返回一个response对象。
- [x] how to install a middleware to app
  - setting.MIDDLEWARE


## signal

django中使用Signal了进行功能解耦。用户可以定义一个Signal，之后可以向Signal发送数据，并注册一个回调函数。

注册回调函数有两种方式
- signal.connent(my_callback)
- 通过receiver装饰器
  ```py
  from django.dispatch import receiver

  @receiver
  def my_callback(sender, **kwargs):
    pass
  ```

signal callback的注册时机及方式: 对应于回调函数的注册方式
- 如果使用`connent`，官方推荐放在AppConfig.ready中
- 如果使用`receiver`, 需要在AppConfig.ready中import所有的回调函数。
