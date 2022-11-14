# go读书笔记

## 基本

### 退化赋值

```go
func main(){
  x := 100
  fmt.Println(&x)

  // 这里的x为退化赋值
  x, y := 200, "abc"
}
```
而如果是这种情况
```go
func main() {
  x := 100
  fmt.Println(&x)

  x := 200  // 这里会报错
}
```

关于退化赋值的前提条件是：最少有一个新变量被定义，且必须是同一作用域

### make & new

new: `new(T)`为类型T分配内存，并返回指针，但是并不初始化T，T中所有的成员变量都是其类型的零值。

> `new(T)`等价于`&T{}`

make: 仅为`map & slice & channels`使用。`make(T)`返回一个实例化后的T（*注意不是指针*）。

由于new仅分配内存，且所有的内部变量都为零值。所以通过new声明的map、slice、channels无法直接使用，需要额外的初始化。*不过对于T，如果零值代表某种含义，则也可以使用new*

### 指针

不能把指针和内存地址混为一谈。

内存地址是内存中每个字节单元的唯一编号，而指针则是一个实体。指针会分配内存空间，相当于一个专门用来保存地址的整形变量。

### switch

switch & fallthrough

switch中每个case无需执行break语句，case执行完毕后自动中断。如须贯通后续的case，须执行fallthrough，但不再匹配后续条件表达式。
> *需要注意，fallthrough仅仅贯通后面紧邻的case*，而非贯通所有case，如需贯通所有case，则需要在每个case中都添加fallthrough

> break放在fallthrough之前，fallthrough会无法执行

## 函数

go中函数的限制
- 无需前置声明
- 不支持命名嵌套定义
- 不支持同名函数重载
- 不支持默认参数
- 支持变长参数
- 支持多返回值
- 支持命名返回值
- 支持匿名函数和闭包

> 第一类对象(first-class object): 在运行期创建，可以作为函数参数或返回值，可以存入变量的实体。 

go中从函数返回局部变量指针式安全的，编译器会通过逃逸分析（escape analysis）来决定是否在堆上分配内存。

```go
func test() *int {
  a := 1
  return &a
}

func main() {
  b := test()
  fmt.Println(*b)
}
```

不论是指针、引用类型，还是其他类型参数，都是值拷贝传递。区分无非是拷贝目标对象，还是拷贝指针而已。在函数调用之前，会为形参和返回值分配内存空间，并将实参拷贝到形参内存。

### 变参

本质上是一个slice。当将一个数组传递给一个变参时，需要将其先转换为一个切片。

当将一个切片传递给一个接受变参的函数时，需要先讲slice展开
```go
func test(a ...int) {
  for _, v := range a {
    fmt.Println(v)
  }
}

func main() {
  a := [3]int{1,2,3}
  test(a[:]...)
}
```
### 延迟调用

使用`defer`注册被**函数调用**，直到当前函数执行结束前才被**执行**。也就是说使用defer时，需要调用函数并提供参数，并非仅仅注册函数。

```go
func test(){
  a, b := 1, 2
  defer func(x, y int){
    fmt.Println(x, y)
  }(a, b)

  // other code
}
```

> 需要额外注意，defer有额外的性能开销，如果对性能的要求较高，使用时要做额外的压力测试工作。

### 错误处理

go将error定义为一个接口类型，以便实现自定义错误类型。
```go
struct error interface {
  Error() string
}
```

recover & panic

调用panic会立即中断当前函数流程，执行延迟调用。而在延迟调用中，recover可以捕获并返回panic提交的错误对象。

> 除非是不可恢复、导致系统无法正常工作的错误，否则不建议使用panic
