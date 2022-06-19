# JavaScript

## 2019.03.02

1. 第一章
    1. number: 用于声明数字变量。
        - Number()： 用于强制类型转换。
    2. javascript 是动态类型语言( 弱类型)，一个变量可以在任意时刻变换类型。
    3. 在ES6中，声明常量的办法： __const__

2. 第二章
    1. typeof a;
        - typeof null: 返回的是是object

    2. Truthy & Falsy
        >重要的是要记住，一个非`boolean`值仅在实际上被强制转换为一个`boolean`时才遵循这个“truthy”/“falsy”强制转换。把你搞糊涂并不困难 —— 当一个场景看起来像是将一个值强制转换为`boolean`，可其实它不是。

        1. Truthy
            - 'hello' ，非空字符串
            - 42
            - true
            - [ ], [1, '2', 3] 。数组，注意空数组也是True
            - { }, { a: 42}。对象，注意空字典也是True
            - function foo( ) { }。函数
        2. falsy
            - "" 空字符
            - 0， -0， Nan 非法的Number
            - null, undefined
            - false

3. == & ===

    >`==`在允许强制转换的条件下检查值的等价性，而`===`是在不允许强制转换的条件下检查值的等价性；因此`===`常被称为“严格等价”。

    - 如果一个比较的两个值之一可能是`true`或`false`值，避免`==`而使用`===`。
    - 如果一个比较的两个值之一可能是这些具体的值（`0`，`""`，或`[]` —— 空数组），避免`==`而使用`===`。
    - 在 *所有* 其他情况下，你使用`==`是安全的。它不仅安全，而且在许多情况下它可以简化你的代码并改善可读性。

    >如果比较的两个非基本类型的值，如object（function，array）。使用==和 === 是比较的是引用的值而不是底层的值。

4. let 关键字

5. 三元操作符：` varb = (a > 3) ? 'hello': 'world'`

6. strict 模式: `use strict;`

7. 立即被调用的函数表达式 IIFE   ？？？？

8. 闭包：你可以认为闭包是这样一种方法， 即使函数已经完成了运行，它依然可以“记住”并持续访问函数的作用域。

9. this : 如果一个函数在它内部拥有一个`this`引用，那么这个`this`引用通常指向一个`object`。但是指向哪一个`object`要看这个函数是如何被调用的。

10. 原型： ？？？？

## 2019.03.04

1. 声明可以将变量绑定在本地的明确的块儿是一种强大的工具，你可以把它加入你的工具箱。
2. var 的使用真是奇怪

    ```javascript
    var foo = true;

    if (foo) {
        var bar = foo * 2;
        bar = something( bar );
        console.log( bar );
    }
    ```

    我们仅在 if 语句的上下文环境中使用变量 `bar`，所以我们将它声明在 if 块儿的内部是有些道理的。__然而，当使用 `var` 时，我们在何处声明变量是无关紧要的，因为它们将总是属于外围作用域__

3. let 使用

    ```javascript
    for (let i=0; i<10; i++) {
    console.log( i );
    }

    console.log( i ); // ReferenceError
    ```

4. 提升

    当你看到 `var a = 2;` 时，你可能认为这是一个语句。但是 JavaScript 实际上认为这是两个语句：`var a;` 和 `a = 2;`。第一个语句，声明，是在编译阶段被处理的。第二个语句，赋值，为了执行阶段而留在 **原处**。

    所以，关于这种处理的一个有些隐喻的考虑方式是，变量和函数声明被从它们在代码流中出现的位置“移动”到代码的顶端。这就产生了“提升”这个名字。

    换句话说，**先有蛋（声明），后有鸡（赋值）**。

    在提升中，__函数声明和变量声明都会被提升__。但一个微妙的细节（*可以* 在拥有多个“重复的”声明的代码中出现）是，__函数会首先被提升，然后才是变量。__

5. 闭包 [link](https://github.com/getify/You-Dont-Know-JS/blob/1ed-zh-CN/scope%20%26%20closures/ch5.md) ***
    - 闭包的出现：实质上 *无论何时何地* 只要你将函数作为头等的值看待并将它们传来传去的话，你就可能看到这些函数行使闭包。

6. IIFE [link](https://github.com/getify/You-Dont-Know-JS/blob/1ed-zh-CN/scope%20%26%20closures/ch3.md#立即调用函数表达式) ***

7. 模块模式？ 没搞懂 [link](https://github.com/getify/You-Dont-Know-JS/blob/1ed-zh-CN/scope%20%26%20closures/ch5.md#现代的模块)

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/template_strings

## 2019.03.05

1. this

    `this` 不是编写时绑定，而是 __运行时绑定__ 它依赖于函数调用的上下文条件。`this` 绑定与函数声明的位置没有任何关系，而与 __函数被调用的方式紧密相连。__

2. this 绑定的是什么，*如何* 决定在函数执行期间 `this` 指向哪里

    - [页面详解](https://github.com/getify/You-Dont-Know-JS/blob/1ed-zh-CN/this%20%26%20object%20prototypes/ch2.md)

    - 默认绑定（Default Binding）
    - 隐含绑定（Implicit Binding）
    - 隐含丢失（Implicitly Lost）
    - 明确绑定（Explicit Binding）
    - 硬绑定（Hard Binding）
    - `new` 绑定（`new` Binding）

3. this 绑定的优先级 [参考](https://github.com/getify/You-Dont-Know-JS/blob/1ed-zh-CN/this%20%26%20object%20prototypes/ch2.md#判定-this)

4. this 他娘的真是复杂

## 2019.03.06

1. **注意：** `in` 操作符看起来像是要检查一个值在容器中的存在性，但是它实际上检查的是属性名的存在性。在使用数组时注意这个区别十分重要，因为我们会有很强的冲动来进行 `4 in [2, 4, 6]` 这样的检查，但是这总是不像我们想象的那样工作。

     >`4 in [1,2,3,4] return false`

2. **注意：** 将 `for..in` 循环实施在数组上可能会给出意外的结果，因为枚举一个数组将不仅包含所有的数字下标，还包含所有的可枚举属性。所以一个好主意是：将 `for..in` 循环 *仅* 用于对象，而为存储在数组中的值使用传统的 `for` 循环并用数字索引迭代。

3. 几个迭代的方法：
    - forEach(..)
    - every(..)
    - some(..)
    - for..of

### 2019.03.07

1. javascript中的类。不过我认为javascript添加类的特性没有必要。
    > 一般来讲，在 JS 中模拟类通常会比解决当前 *真正* 的问题埋下更多的坑。

2. prototype: 原型

3. 在 JavaScript 中，类不能（因为根本不存在）描述对象可以做什么。对象直接定义它自己的行为。**这里 仅有 对象**。

4. instanceof
    ```a instanceof Foo; // true```

    `instanceof` 操作符的左侧操作数接收一个普通对象，右侧操作数接收一个 **函数**。`instanceof` 回答的问题是：**在 a 的整个 [[Prototype]] 链中，有没有出现那个被 Foo.prototype 所随便指向的对象？**

5. 创建链接 Object.create( )

6. 委托 [link](https://github.com/getify/You-Dont-Know-JS/blob/1ed-zh-CN/this%20%26%20object%20prototypes/ch5.md)

书签[point](https://github.com/getify/You-Dont-Know-JS/blob/1ed-zh-CN/types%20&%20grammar/README.md#you-dont-know-js-types--grammar)

## 2019.08.31

1. var与let的区别:
    > let允许你声明一个作用域被限制在 块级中的变量、语句或者表达式。与 var 关键字不同的是， var声明的变量只能是全局或者整个函数块的。 var 和 let 其他不同之处在于后者是在编译时才初始化
