# about gevent monkey patch

monkey patch

将`theading.local`替换为基于greenlet的local。每个`greenlet`可以存储仅自己可以访问的数据。