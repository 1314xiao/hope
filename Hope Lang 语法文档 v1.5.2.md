# Hope Lang 语法文档 v1\.5\.2

# \[syntax\.md\]\(syntax\.md\) — Hope Lang 语法文档

> Hope Lang v1\.5\.2
> 纯 Python 手写解释器，轻量动态脚本语言。
> 
> 

## 目录

1. 基础词法规则

2. 注释

3. 变量与赋值

4. 基础数据类型

5. 运算符

6. 分支语句 `if`

7. 循环语句 `loop`

8. 函数定义与调用

9. 内置库导入（`LIB_MAP` 扩展库）

10. 数组（列表）

11. 内置函数

12. 语法示例

13. 打包

---

## 1\. 基础词法规则

- 标识符（变量名、函数名）：字母、下划线、数字，**不能以数字开头**

- 区分大小写：`a` 和 `A` 是不同变量

- 源码编码：UTF\-8

- 语句分隔：一行多条语句可用空格隔开（可选）

- 缩进**不强制**（区别 Python），块使用 `{ }` 包裹

关键字列表（保留词，不能用作变量名）

```Plain Text
show if else loop func return set import 
show、input、str、int、float、len、max、min、
sum、range、round_two、round_custom、enumerate、
zip、type、id、str_get、str_slice、str_find、
str_split、list_append、list_pop、file_read、
file_write、file_append 
```

## 2\. 注释

```hope
// 单行注释，从//到行尾
/*
多行注释
可以跨多行
*/
```

## 3\. 变量与赋值

使用 `set` 关键字定义 / 更新变量

```hope
set a = 10
set b = "hello hope"
set c = 3.14

// 一行多个赋值，空格分隔
set x=1 set y=2
```

> 变量作用域：
> 
> - 全局：顶层定义
> 
> - 函数内：局部变量，优先使用局部；未定义则向上查找全局
> 
> 

## 4\. 基础数据类型

1. **数字 number**：整数、浮点数

```hope
set n1 = 100
set n2 = 3.14
```

2. **字符串 string**：双引号 `"` 包裹，暂不支持转义（可后续扩展）

```hope
set s = "Hope Lang"
```

3. **null**：空值

> ⚠️ 当前版本**没有布尔类型，不存在 true /false 字面量**。
> 比较运算结果仅用于 `if` / `loop` 的条件判断，**不能赋值保存到变量**。
> 
> 

## 5\. 运算符

### 算术运算符

`+` `-` `*` `/` `%`
> ⚠️ 语法约束：**不支持直接负变量 ****`-a`**。
> 负变量使用乘法表达：`-1 * 变量`，或者如`变量+(-2)`表达。
> 
> 

```hope
set res = 1 + 2 * 3
set mod = 10 % 3
```

### 比较运算符

`==` `!=` `>` `<` `>=` `<=`
✅合法：直接写在 if/loop 条件括号内

```hope
if(10 > 5){
    show("成立")
}
```

❌非法：不能把比较结果赋值变量

```hope
set ok = 10 > 5
```

### 逻辑运算符

> ⚠️ 当前版本**未实现逻辑运算**：
> 不支持 `and` / `or` / `not` 关键字；同时不支持符号 `&&`、`||`。
> 多条件判断只能通过嵌套 `if` 实现。
> 
> 

✅模拟逻辑与（and）

```hope
if( a > 0 ){
    if( b < 10 ){
        show("全部条件满足")
    }
}
```

✅模拟逻辑或（or）

```hope
if( a > 0 ){
    show("条件满足")
}else{
    if( b < 10 ){
        show("条件满足")
    }
}
```

✅模拟逻辑非（not）

```hope
// 模拟 not (a > 5) 等价于 `a <=5`
if( a > 5 ){
    // 条件为真，not就不执行
}else{
    show("not(a>5) 成立，a小于等于5")
}

```

#德摩根定律在这里完全生效：
`!(A && B)` = `!A || !B`
`!(A || B)` = `!A && !B`，
全部只用 if‑else 嵌套实现，不需要额外布尔运算符。

✅模拟组合演示：not + and

```hope
// not( a>0 && b<10 )
if( a > 0 ){
    if( b < 10 ){
        // a>0并且b<10，not不执行
    }else{
        show("not(a>0 && b<10) 成立")
    }
}else{
    show("not(a>0 && b<10) 成立")
}
```

✅模拟组合演示：not + or

```hope
//not( a>0 || b<10 )
if( a > 0 ){
    // a>0，or条件成立，not不执行
}else{
    if( b < 10 ){
        // b<10，or条件成立，not不执行
    }else{
        show("not(a>0 || b<10) 成立")
    }
}
```

### 优先级（从高到低）

括号 `()` \> 乘除取模 \> 加减 \> 比较

## 6\. 分支语句 if

```hope
if (条件) {
    // 条件成立执行
} else {
    // 可选else分支
}
```

示例：

```hope
set age = 18
if (age >= 18) {
    show("成年")
} else {
    show("未成年")
}
```

> 暂不支持 `else if`，如需多分支可以嵌套 if。
> 
> 

## 7\. loop 循环

```hope
loop (条件) {
    // 循环体
}
```

示例

```hope
set i = 0
loop (i < 5) {
    show(i)
    set i = i + 1
}
```

> 当前版本：暂不支持 `break / continue`，后续可扩展
> 
> 

## 8\. 函数定义与调用

使用 `func` 定义函数

```hope
func 函数名(参数1, 参数2) {
    return 返回值
}
```

示例

```hope
func add(a, b) {
    return a + b
}

set sum = add(12, 30)
show(sum)
```

- 无 return 的函数，返回 `null`

- 参数列表可以为空：`func hello() { ... }`

- 函数是一等对象（可存入变量，后续可扩展）

## 9\. 内置库导入（LIB\_MAP）

> 配置文件 `lib_config.hope` 预先映射库，使用 `import` 加载库
> 
> 

```hope
import math
print(math_sqrt(16))

import random
print(randint(1,100))
```

内置库清单：

- `math`：数学函数

- `random`：随机数

- `time`：时间相关

- `os`：操作系统接口

- `turtle`：绘图

- `urllib`：网络请求

- `fs`：文件系统

- `sys`：系统信息

- `eggs` / `hello`：示例扩展库

## 10\. 数组（列表）

```hope
// 创建数组
set arr = [10, 20, "text", 30]

// 下标读取
show(arr[0])

// ✅下标直接赋值（v1.5.2支持）
arr[1] = 99
arr[2] = "hello array"
show(arr)
```

> 注意：下标超出数组范围会产生运行错误。
> 
> 

## 11\. 内置全局函数

### 1.输出 show(值)

控制台输出，打印变量/表达式结果到标准输出，等价于打印展示内容。

```hope
show(123)
show("hello hope")
```
### 2.输入 input(prompt, type)

控制台输入函数。

- `prompt`：字符串，输入提示文本
- `type`：类型转换器，可选：`int` / `str` / `float`
等待用户在终端输入，读取输入内容并转换成指定类型后返回。
```hope
set a = input("a=", int)    //读取整数
set b = input("b=", str)    //读取字符串
set c = input("c=", float)  //读取浮点数
```

> 提示：SDK 长连接模式中调用`input()`可能会阻塞标准输入。
> 
> 

### 类型转换

- `str(val)`：任意值转为字符串

- `int(val)`：转为整数

- `float(val)`：转为浮点数

```hope
set s = str(123)
set n = int("66")
set f = float("3.14")
```

### 数学聚合函数

- `len(val)`：获取字符串 / 数组长度

- `max(*args)`：取多个参数最大值

- `min(*args)`：取多个参数最小值

- `sum(*args)`：对多个数字求和

- `range(*args)`：生成数字序列数组

- `round_two(val)`：保留 2 位小数

- `round_custom(num, decimals)`：自定义保留小数位数

```hope
show(len([10,20,30]))
show(max(1,9,3))
show(sum(1,2,3,4))
show(range(1,10))
show(round_custom(3.1415,2))
```

### 序列工具

- `enumerate(seq)`：遍历序列，返回下标 \+ 元素

- `zip(*args)`：多数组配对压缩

- `type(val)`：获取值的类型字符串

- `id(val)`：获取对象唯一标识

### 字符串函数

- `str_get(s, idx)`：按下标读取字符串单个字符

- `str_slice(s, start, end)`：字符串切片

- `str_find(s, sub)`：查找子串，返回下标，找不到返回`-1`

- `str_split(s, sep)`：按分隔符切割字符串，返回数组

```hope
set text = "HelloHope"
show(str_get(text,0))
show(str_slice(text,0,3))
show(str_find(text,"Hope"))
show(str_split("a,b,c", ","))
```

### 数组工具函数（补充，除下标赋值之外）

- `list_append(lst, item)`：数组追加元素

- `list_pop(lst)`：弹出数组末尾元素，返回被弹出的值

```hope
set arr = [10,20]
list_append(arr, 30)
show(list_pop(arr))
```

### 文件操作函数

- `file_read(path)`：读取整个文件，返回文件内容字符串

- `file_write(path, content)`：覆盖写入文件

- `file_append(path, content)`：追加写入文件

```hope
file_write("test.txt","hello file")
show(file_read("test.txt"))
file_append("test.txt","\nnew line")
```

> 其余能力全部由各个扩展库提供。
> 
> 

## 12\. 完整示例合集

### 示例 1：Hello World

```hope
print("Hello Hope Lang!")
```

### 示例 2：求和函数

```hope
func sum(a,b) {
    return a + b
}
set s = sum(60,12)
show(s)
```

### 示例 3：循环计数

```hope
set i=1
loop(i<=10){
    show(i)
    set i = i+1
}
```

### 示例 4：使用 math 库

```hope
import math
set r = math_sqrt(25)
show(r)
```

### 示例 5：数组下标读写赋值

```hope
set arr = [1, 2, 3, 4]
arr[0] = 99
arr[3] = -1 * 10
show(arr)
list_append(arr, 50)
show(list_pop(arr))
```

### 示例 6：字符串分割处理

```hope
set s = "apple,orange,banana"
set parts = str_split(s, ",")
show(parts)
```

### 示例 7：简单文件读写

```hope
file_write("demo.txt","Hope Lang 文件测试")
set content = file_read("demo.txt")
show(content)
```

### 示例 8：嵌套 if 模拟多条件

```hope
set a = 5
set b = 3
if( a > 0 ){
    if( b < 10 ){
        show("a>0 并且 b<10")
    }
}
```

## 13\. 打包

### 使用 hopeglue 打包工具

用法: hopeglue\.exe loader\.exe 环境根目录 输入脚本\.hope 输出\.exe
示例: hopeglue\.exe loader\.exe D:\\hope 2\.hope 2\.exe

可以简化打包命令，需要配置 glue\.bat
用法:glue 输入脚本\.hope 输出\.exe
示例:glue 2\.hope 2\.exe

创建一个 glue\.bat 的文件，复制下面内容到 glue\.bat 中（有就不用创建，修改路径）
修改路径：

```bat
@echo off
chcp 65001 >nul
set "GLUE_DIR=D:\hope\hopeglue"
set "HOPE_ENV_ROOT=D:\hope"
del /q "_env_temp.zip" 2>nul
if "%~2"=="" (
    echo 用法：glue 脚本.hope 输出app.exe
    echo 示例：glue 2.hope app.exe
    pause
    exit /b
)
"%GLUE_DIR%\hopeglue.exe" "%GLUE_DIR%\loader.exe" "%HOPE_ENV_ROOT%" %1 %2
del /q "_env_temp.zip" 2>nul
```

---

# 附录：语法限制 \& 待开发功能

> 标注当前 v1\.5\.2 版本**尚不支持**，后续迭代计划
> 
> 

1. 不支持 `else if`

2. 不支持 `break` / `continue`

3. 字符串暂不支持转义字符 `\n` `'`

4. 没有对象 / 结构体，只有基础类型 \+ 数组

5. 没有 for 循环

6. **不支持直接负变量（****`-a`****非法），负数必须写 ****`-1 * a`**

7. **未实现 ****`and`**** / ****`or`**** / ****`not`****；不支持符号 ****`&&`****、****`||`****，复合条件依靠嵌套 if 实现**

8. **无布尔类型，不存在 true /false；比较表达式仅允许直接用于 if/loop 条件，不能赋值变量**

> 提示：SDK 模式下，可以通过 Python 侧调用 Hope 代码，也可以扩展双向回调。
> 
> 

---



