# python cookbook section 2

文本与字符串

## 使用多种界定符分割字符串

`re.split`

## 字符串开头和结尾匹配

`str.startswith()` & `str.endswith()`

## 字符串的搜索和替换

- `str.replace()`
- `re.sub()`

	sub() 函数中的第一个参数是被匹配的模式，第二个参数是替换模式。反斜杠数字比如 \3 指向前面模式的捕获组号。

	```sh
	>>> text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
	>>> import re
	>>> re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
	'Today is 2012-11-27. PyCon starts 2013-3-13.'

	>>> re.sub(r'(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)', r'\g<year>-\g<month>-\g<day>', text)
	'Today is 2012-11-27. PyCon starts 2013-3-13.'
	```

