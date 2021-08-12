# about protocal buffer 
https://developers.google.cn/protocol-buffers/docs/pythontutorial

## Basic

package: 避免命名冲突

date type:
- string
- int32
- float
- bool
- dobule
- enum

unique tag:
- 必须唯一
- 1-15比16-other少用一个二进制位，所以尽量使用15位也是种优化

filed annotation:
- optional: 可选字段。如果字段未设置，将会使用默认字段。对于简单的字段，可以手动设置默认值。
- repeated: 字段被重复多次，包括0次。可简单视为存储相同类型数据的数组字段。
- required: 必填字段。如果不填会报错。
	> 对于`required`的使用需要小心。当必填字段转换为可选字段时，旧的`reader`对于新的proto会出现不兼容的情况。在google内部也并不推荐使用`required`。`proto3`将不在支持`required`。

将proto文件转换为py:
`protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/addressbook.proto`

## The Protocol Buffer API

```py
import addressbook_pb2
person = addressbook_pb2.Person()
person.id = 1234
person.name = "John Doe"
person.email = "jdoe@example.com"
phone = person.phones.add()
phone.number = "555-4321"
phone.type = addressbook_pb2.Person.HOME
```

- 如果增加一个`.proto`中不存在的变量会导致`AttributeError`
- 如果为一个变量赋错误类型的值会导致`TypeError`

## Standard Message Methods
- IsInitialized(): checks if all the required fields have been set.
- __str__(): returns a human-readable representation of the message, particularly useful for debugging. (Usually invoked as str(message) or print message.)
- CopyFrom(other_msg): overwrites the message with the given message's values.
- Clear(): clears all the elements back to the empty state.
> https://googleapis.dev/python/protobuf/latest/google/protobuf/message.html#google.protobuf.message.Message

## Parsing and Serialization
- SerializeToString(): serializes the message and returns it as a string. Note that the bytes are binary, not text; we only use the str type as a convenient container.
- ParseFromString(data): parses a message from the given string.
> 如果想要在`proto buffer`上定制增加若干功能，可以考虑对`proto buffer`做一层额外的封装。但是应该注意不要使用继承`proto buffer`来增加功能(因为这样可能会破坏proto本身的逻辑)。


## 扩展proto buffer需要遵守的原则
- 不能修改已有的tag
- 不能增加和删除`required`字段
- 可以删除`optional`和`repeated`字段
- 可以增加新的`optional`和`repeated`字段，但是必须使用全新的tag（即使已经删除的字段的tag也不能用）

如果遵循以上的原则，新的proto和旧的reader可以兼容工作。

对于旧代码，删除的`optional`将被设置为默认值，删除的`repeated`将被设置为空数组。

对于新代码，新的`optional`字段可能不在数据中，需要显示的通过`has_`进行判断，或是在定义`.proto`时显式的定义默认值。string对应空字符串，numeric对应0，bool对应flase。**对于新的`repeated`字段，如果没有`has_`方法将无法判断该字段是被设置为空，还是从未被修改。**

https://googleapis.dev/python/protobuf/latest/

