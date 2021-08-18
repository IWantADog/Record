# python cookbook section 2

文本与字符串

## 使用多种界定符分割字符串

`re.split`

## 字符串开头和结尾匹配

`str.startswith()` & `str.endswith()`

## 字符串的搜索和替换

- `str.replace()`
- `re.sub()`

    用来处理较为复杂的替换逻辑。

    sub() 函数中的第一个参数是被匹配的模式，第二个参数是替换模式。反斜杠数字比如 \3 指向前面模式的捕获组号。

    ```sh
    >>> text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
    >>> import re
    >>> re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
    'Today is 2012-11-27. PyCon starts 2013-3-13.'

    >>> re.sub(r'(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)', r'\g<year>-\g<month>-\g<day>', text)
    'Today is 2012-11-27. PyCon starts 2013-3-13.'
    ```

- re.IGNORECASE: 忽略大小写的文件匹配
- `sub`可以接受一个回调函数。
    ```sh
    >>> import re
    >>> datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
    >>> from calendar import month_abbr
    >>> def change_date(m):
    ... mon_name = month_abbr[int(m.group(1))]
    ... return '{} {} {}'.format(m.group(2), mon_name, m.group(3))
    ...
    >>> datepat.sub(change_date, text)
    'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'
    ```
- re.DOTALL: 让正则表达式中的`.`匹配包括换行符在内的所有字符。

## 将unicode文本标准化

在需要比较字符串的程序中使用字符的多种表示会产生问题。 为了修正这个问题，你可以使用`unicodedata`模块先将文本标准化。

## 删除字符串中不需要的字符

- str.strip()
- str.lstrip()
- str.rstrip()

## 合并拼接字符串

- str.join: 可接受一个`生成器`

## 以指定列宽格式化字符串

`textwrap`