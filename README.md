# Hope‑Lang: 轻量级Python脚本语言

# Hope‑Lang

Hope 是一门基于 Python 开发的轻量动态解释型脚本语言，自带独立隔离虚拟机、REPL 交互式控制台，支持脚本文件运行与**基于标准输入输出的 JSON STDIO SDK**。

> 核心设计：**Python 底层函数映射**实现标准库，`HopeVM` 提供对外嵌入 API；配套 `HopeSdkClient`，可直接拉起 Hope 子进程做外部程序 / 编辑器集成。
> 
> 

> 项目版本：v1\.5\.2
> 项目状态：开发中
> License：MIT
> 
> 

## ✨ 核心特性

- 完整编译管线：词法分析 Lexer → AST 语法树 Parser → Interpreter 解释执行

- **隔离虚拟机实例**：每个 `HopeVM()` 实例拥有独立运行环境；多线程必须新建独立 VM 实例

- REPL 交互式终端，逐行调试代码；原生支持 `.hope` 脚本文件执行

- **STDIO‑JSON SDK**：`hope_sdk_server.py` 服务端基于标准输入输出传输单行 JSON 指令；`hope_sdk_client.py` 封装客户端，`subprocess`拉起进程，Windows 支持隐藏控制台窗口，适合编辑器、第三方程序集成

- **插件式标准库体系**：底层由 Python 实现，映射挂载到 Hope 运行时。新增库只需在 `libs/` 添加模块并注册，无需修改解释器核心

- 内置标准库：`math`、`random`、`time`、`os`、`fs`、`urllib`、`turtle`、`sys`

- 友好报错：错误附带源码行号，区分 `LexerError`、`ParserError`、`InterpreterError`

- 两种集成模式：①SDK 子进程模式；②Python 直接嵌入`HopeVM`，无需子进程

- 支持 PyInstaller 打包 Windows 独立 EXE；内置`_pyinstaller_embed_tk()`辅助函数处理 turtle/tkinter 图形库打包

- 可在 Termux（安卓）环境部署

## 📁 项目目录结构

```Plain Text
hope/
├── README.md                 # 项目文档
├── LICENSE                   # MIT开源协议
├── .gitignore                # Git忽略配置
├── requirements.txt          # Python依赖
├── hope.py                   # CLI主入口：REPL / 脚本执行 / --sdk SDK服务
├── hope_vm.py                # HopeVM虚拟机【对外嵌入API模块】
├── hope_sdk_server.py        # SDK服务端：stdin/stdout JSON协议
├── hope_sdk_client.py        # SDK客户端：HopeSdkClient类，subprocess拉起进程
├── hope_builtins.py          # 内置基础函数
├── hopeglue.py               # 胶水层
├── host.py
├── lexer.py                  # 词法分析器
├── parser.py                 # 语法分析器
├── interpreter.py            # AST解释执行核心
├── errors.py                 # 自定义异常类
├── lib_config.hope           # 标准库注册配置文件
├── loader.py                 # 库加载器：动态加载libs下模块，映射Python函数到VM
├── xide4.py
├── hope.spec                 # PyInstaller打包spec
├── hopeglue.spec
├── ho.ico                    # Windows打包图标
├── libs/                     # ✅ 所有标准库（Python实现，映射给Hope脚本调用）
│   ├── hope_random.py
│   ├── hope_math.py
│   ├── hope_time.py
│   ├── hope_os.py
│   ├── hope_turtle.py
│   ├── hope_urllib.py
│   ├── hope_fs.py
│   ├── hope_sys.py
│   └── hope_hello.py
├── examples/                 # Hope语言示例脚本
│   ├── hello.hope
│   ├── calc.hope
│   └── sdk_interactive_demo.py # Python SDK客户端使用示例
├── docs/
│   ├── syntax.md             # Hope语法参考文档
│   ├── sdk_api.md            # SDK长连接接口文档
│   └── build.md              # 打包与部署教程（Windows EXE / Termux）
└── build/
    └── build_spec.py         # PyInstaller打包脚本
```

## 🚀 快速上手

### 环境要求

Python \>= 3\.11\.9

```bash
# 克隆仓库
git clone https://github.com/1314xiao/hope.git
cd hope1.5.2

# 安装依赖
pip install -r requirements.txt
```

### 三种运行模式（\[hope\.py\]\(hope\.py\) 入口）

#### 1\. REPL 交互式（逐行写代码）

```bash
python hope.py
```

#### 2\. 运行 `.hope` 脚本文件

```bash
python hope.py examples/hello.hope
```

#### 3\. 启动 SDK STDIO‑JSON 服务

```bash
python hope.py --sdk
```

> SDK 通信规则：每行一条 JSON 请求，输出单行 JSON 响应。
> 支持动作：`run_code` / `call` / `set_global` / `get_global` / `quit`
> 响应字段：`ok`\(bool\)、`data`\(返回值\)、`error`\(错误信息\)
> 
> 

### 使用 HopeSdkClient（子进程 SDK 模式）

```python
from hope_sdk_client import HopeSdkClient

# 传入exe路径
client = HopeSdkClient(r"hope.exe")

client.run_code("let a = 10; show(a)")
client.call("my_func", 1, 2, 3)
client.set_global("name", "hope")
val = client.get_global("name")

client.close()
```

## 🧩 HopeVM 嵌入 API（Python 直接嵌入，不启动子进程）

```python
from hope_vm import HopeVM

vm = HopeVM()
vm.run_code('set a = 10; show(a)')
vm.run_file("examples/hello.hope")

# 注册Python原生函数供Hope调用
vm.register_native(
    func_name="add",
    param_names=["x","y"],
    callback=lambda args: args[0] + args[1]
)

result = vm.call("my_hope_func", 1, 2, 3)
vm.set_global("val", 999)
print(vm.get_global("val"))
```

> ⚠️ 重要限制
> 
> 1. 不支持嵌套双向回调；不要在`register_native`回调内部调用 `vm.call()`
> 
> 2. 参数仅支持 `int/float/str/list`；禁止传递自定义 Python 对象
> 
> 3. 多线程：禁止多线程共享同一个 HopeVM 实例，每个线程新建实例
> 
> 4. 与 CLI REPL、SDK 子进程环境互相隔离
> 
> 

## 📜 Hope‑Lang v1\.5\.2 语法速览

> 不强制缩进，代码块使用 `{ }`，UTF‑8 编码；标识符区分大小写，不能以数字开头。
> 
> 

- **注释**：`//`单行，`/* */`多行

- **变量赋值**：`set a = 10`；支持全局、函数局部作用域

- **数据类型**：数字、双引号字符串（暂不支持转义）、`null`

    > ⚠️ **无布尔字面量 true/false**；比较表达式仅允许用于`if/loop`条件，**不能赋值给变量**
    > 
    > 

- **运算符**

    - 算术：`+ - * / %`，**不支持 ****`-a`****，负数写 ****`-1 * a`**

    - 比较：`== != > < >= <=`

    - 无 `and/or/not` / `&& ||`，多条件逻辑用嵌套`if‑else`实现

    - 优先级：`()` \> 乘除取模 \> 加减 \> 比较

- **控制流**

```hope
if(条件){ ... } else { ... }       // 不支持 else‑if，多分支需要嵌套
loop(条件){ ... }                 // 条件循环，无 break / continue
```

- **函数与数组**

```hope
func add(a,b) { return a+b }      // 无 return 返回 null
set arr = [10,20,"hi"]
arr[0] = 99                       // 支持下标读写赋值
```

- **库与内置函数**

    - `import math` / `import random`：加载预注册标准库，库配置位于`lib_config.hope`

    - IO：`show()`输出；`input(prompt, type)`终端输入

    - 类型转换：`str()` `int()` `float()`

    - 工具：`len`/`max`/`min`/`sum`/`range`；字符串、数组操作函数；`file_read/file_write/file_append`文件读写

- **v1\.5\.2 关键限制**

    - 没有`else if`、`break`、`continue`、`for`循环

    - 字符串不支持转义字符

    - 无对象 / 结构体，仅基础类型 \+ 数组

    - 不支持直接负变量；无逻辑运算符，复合条件依赖嵌套 if

    - 比较运算结果不可保存为变量

- **独立脚本打包**：使用`hopeglue`工具，可将`.hope`脚本打包为 Windows 独立 exe，可配置`glue.bat`简化命令。

## 📚 文档索引

- \[语法文档\]\(docs/syntax\.md\)：完整语法说明、示例、版本限制

- \[SDK API\]\(docs/sdk\_api\.md\)：STDIO JSON 协议、全部 action 指令、客户端类、错误样例

- \[打包部署\]\(docs/build\.md\)：Windows EXE 打包、Termux 安卓部署、图形库打包注意事项

## 📦 打包部署

项目自带 `hope.spec`，用于 PyInstaller 打包为独立 Windows EXE。

```bash
pyinstaller hope.spec
```

打包产物输出至 `dist/`。

## 📄 License

本项目使用 MIT 协议，详情见 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue、PR，参与语言开发、标准库扩充与文档完善。

> （注：部分内容由豆包工作 AI 生成）
