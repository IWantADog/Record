# python cookbook section 3

## 数字的四舍五入

- round()
- decimal: 处理对数据精度十分严格的情况
	- 通过字符串存储数据，但支持所有的数据操作。

## 二、八、十六进制整数

- bin
- oct
- hex

## 随机数

`random`

## 处理时间和日期转换

- datetime
- dateutil

## 计算当前月份的时间范围
- calender

```py
# 很有意思的代码
from datetime import datetime, date, timedelta
import calendar

def get_month_range(start_date=None):
    if start_date is None:
        start_date = date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month)
    return (start_date, end_date)
```

```py
def date_range(start, stop, step):
    while start < stop:
        yield start
        start += step

for d in date_range(datetime(2012, 9, 1), datetime(2012,10,1),timedelta(hours=6)):
	print(d)
```

## 字符串转日期

`datetime.strptime()`

> `strptime`的性能很差，对于固定的日期格式，可以选择其他的方式，如通过字符串分割。

## 对于设计时区的时间操作

优先将时间转化为`UTC`时间之后再处理。