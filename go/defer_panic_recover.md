# Defer & Panic & Recover

## Defer

defer的3条规则
1. 传入defer的是具体值的拷贝
2. defer的执行顺序是先进后出
3. 可以在defer中修改返回值
  - 这也证明defer是在函数体中的return确定返回值之后，返回到调用者之前执行的。

## Panic

- panic仅仅会终止当前的goroutine，不会影响其他goroutine。
- 当panic发生时会立即中止当前函数的执行，并开始执行defer，返回到函数的调用方。对于调用方，具体的行为也相当于发生了panic。panic一路向上，直到终止当前的goroutine。

## Recover

- recover用于捕获panic，并且能获取panic的入参。
- recover只能在defer中被调用