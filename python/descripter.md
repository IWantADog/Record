# python descripter

https://docs.python.org/3/howto/descriptor.html

- `descripter`的实现动机是：当通过属性访问`class variables`时，可以自定义逻辑。
- 必须为`class variables`
- 必须实现`__get__` or `__set__` or `__delete__`方法
- 不要使用`descripter`存储数据，实际数据的存储还是应该存入`instance`


https://docs.python.org/3/howto/descriptor.html#id12

TODO: start from here
