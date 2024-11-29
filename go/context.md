# about context

## 派生上下文

context于派生context之间是一个树状结构。当一个context被关闭，由它派生而来的所有其他context也都会被关闭。

*Background*是一个context的根结点，永远不会被关闭。

*WithChannel*可以取消多余请求，在对副本的场景下（TODO: 不是很理解）

*WithTimeout*设置一个有deadline的请求。

*WithValue*写入key和value到ctx。后续可以使用*Value*读取写入的数据。