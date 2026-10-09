# Hope Lang SDK API 文档

# [SDK API 文档](sdk_api.md)

```markdown
# Hope Lang SDK API 文档
> 版本：v1.5.2
通信模式：**标准输入(stdin) / 标准输出(stdout) 基于JSON行协议**
启动方式：
- 源码运行：`python hope.py --sdk`
- 打包exe运行：`hope.exe --sdk`

## 概述
SDK 使用**按行JSON通信**：
1. 向子进程`stdin`写入一行JSON请求，末尾加换行符 `\n`。
2. 子进程处理完成，向`stdout`输出一行JSON响应，末尾加换行符 `\n`。
3. 每一条请求对应一条响应。
4. stderr保留给解释器原生日志、报错，不参与协议通信。

> ⚠️ 编码注意：Windows下注意编码，建议统一使用UTF‑8；客户端示例代码中当前使用gbk仅适配Windows控制台，正式推荐utf‑8。

## 请求通用格式
```json
{
  "action": "动作名",
  "其他参数键": "对应值"
}
```

## 响应通用格式

```json
{
  "ok": true,
  "data": null,
  "error": ""
}
```

|字段|说明|
|---|---|
|ok|布尔；`true`执行成功，`false`发生错误|
|data|返回结果数据；成功时存放返回值，出错一般为`null`|
|error|错误信息字符串；成功为空字符串，失败存放异常描述|

---

## Action 接口列表

### 1\. `run_code`

执行一段 Hope 脚本源码。

**请求参数**

```json
{
  "action":"run_code",
  "source":"set a=10\nshow(a)"
}
```

- `source`：字符串，完整 Hope 源代码，可以包含多行（`\n`换行）。

**响应示例（成功）**

```json
{"ok":true,"data":null,"error":""}
```

**响应示例（出错）**

```json
{"ok":false,"data":null,"error":"语法错误：xxx"}
```

> 说明：`run_code`会在同一个虚拟机实例执行，函数、全局变量会保留，状态持久。
> 
> 

---

### 2\. `call`

调用已经定义的 Hope 函数，传入参数，获取返回值。

**请求参数**

```json
{
  "action":"call",
  "func_name":"add",
  "args":[10,20]
}
```

- `func_name`：函数名字符串

- `args`：数组，传入的参数列表

**成功响应**

```json
{"ok":true,"data":30,"error":""}
```

**失败响应（函数不存在）**

```json
{"ok":false,"data":null,"error":"函数 add 未定义"}
```

---

### 3\. `set_global`

设置 Hope 虚拟机的全局变量。

**请求参数**

```json
{
  "action":"set_global",
  "var":"g_val",
  "value":1234
}
```

- `var`：变量名

- `value`：要设置的值（数字、字符串、数组等可序列化 JSON 类型）

**成功响应**

```json
{"ok":true,"data":null,"error":""}
```

---

### 4\. `get_global`

读取 Hope 虚拟机全局变量。

**请求参数**

```json
{
  "action":"get_global",
  "var":"g_val"
}
```

**成功响应**

```json
{"ok":true,"data":1234,"error":""}
```

> 如果变量不存在，返回`data:null`或者抛出错误，视解释器实现。
> 
> 

---

### 5\. `quit`

请求关闭 SDK 服务进程。

> ⚠️ 协议规则：收到`quit`会**先返回响应报文，再退出进程**，客户端必须读取返回 JSON，不能直接杀掉进程。
> 
> 

**请求**

```json
{"action":"quit"}
```

**成功响应**

```json
{"ok":true,"data":"exit","error":""}
```

收到该响应之后，子进程会结束。

---

## Python 客户端使用说明

> 参考源码：`examples/hope_sdk_client.py`，示例脚本：`examples/demo.py`
> 
> 

### 类：`HopeSdkClient`

```python
from hope_sdk_client import HopeSdkClient

# 传入exe路径
client = HopeSdkClient("hope.exe")

# 执行hope源码,自定义函数
client.run_code("""
func add(a,b){
    return a + b
}
""")

# 调用函数
res = client.call("add", 3,4)

print(res)

# 设置全局变量
client.set_global("x", 999)

# 读取全局变量
v = client.get_global("x")

print(v)

# 关闭
client.close()
```

### 异常说明

- `run_code` / `call` / `set_global` / `get_global` 在 `ok=false` 时抛出 `RuntimeError(resp["error"])`

- 调用`close()`发送`quit`，等待子进程正常结束。

## ⚠️ SDK 模式特殊限制（v1\.5\.2）

1. Hope 内置函数`input()`会阻塞 stdin；**SDK 模式不建议使用****`input()`**，会卡住整个 JSON 协议。

2. 虚拟机状态在 SDK 生命周期持续保存；函数、全局变量不会自动重置。如需重置，需要重新启动 SDK 子进程。

3. 文件 IO 函数 `file_read/file_write/file_append` 在 SDK 模式下正常工作，路径以子进程启动目录作为工作目录。

4. 不支持`and/or/not`布尔逻辑，不支持负数字面量 `-10`，遵循 Hope 语法文档`syntax.md`全部语法约束。

## 简单通信示例（原始 JSON，不使用客户端库）

```Plain Text
# 输入(stdin发送)
{"action":"run_code","source":"func add(a,b){return a+b}"}

# 输出(stdout收到)
{"ok":true,"data":null,"error":""}

# 输入(stdin发送)
{"action":"call","func_name":"add","args":[5,7]}

# 输出(stdout收到)
{"ok":true,"data":12,"error":""}

# 输入(stdin发送)
{"action":"quit"}

# 输出(stdout收到)
{"ok":true,"data":"exit","error":""}
```

## 故障排查

1. 客户端卡住收不到返回：确认每一条请求末尾带换行符`\n`；服务端必须执行`stdout.flush()`。

2. JSON 解析报错：每一行只能一条 JSON，不能多行合并；不要输出额外打印内容到 stdout。

3. Windows 乱码：优先使用 UTF‑8 编码打开管道。

```Plain Text
直接复制全部内容保存为 `docs/sdk_api.md`。

> 配套仓库文件放置：
> - `docs/sdk_api.md` 👉 SDK协议文档
> - `docs/syntax.md` 👉 Hope语法文档
> - `examples/hope_sdk_client.py` 👉 Python客户端源码
> - `examples/demo.py` 👉 简单演示示例

```
