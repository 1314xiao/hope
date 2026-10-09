from errors import InterpreterError



# ========== Hope 的 tkinter GUI 库 ==========

_tk_root = None
_widgets = {}
_widget_count = 0

def _get_widget(widget_id):
    if widget_id not in _widgets:
        raise InterpreterError(f"控件 {widget_id} 不存在")
    return _widgets[widget_id]

def _next_widget_id(prefix):
    global _widget_count
    _widget_count += 1
    return f"{prefix}{_widget_count}"

# tk_window(title, width, height)：创建主窗口
def tk_window_func(args):
    global _tk_root
    if len(args) != 3:
        raise InterpreterError("tk_window函数需要3个参数：tk_window(标题, 宽度, 高度)")
    title, w, h = args[0], args[1], args[2]
    if not isinstance(title, str):
        raise InterpreterError("第一个参数必须是字符串（窗口标题）")
    if not (isinstance(w, (int, float)) and isinstance(h, (int, float))):
        raise InterpreterError("宽度和高度必须是数字")
    import tkinter as tk
    if _tk_root is None:
        _tk_root = tk.Tk()
    _tk_root.title(title)
    _tk_root.geometry(f"{int(w)}x{int(h)}")
    return f"窗口已创建：{title}（{int(w)}x{int(h)}）"

# tk_label(parent_id, text, x, y)：创建标签
def tk_label_func(args):
    if len(args) != 4:
        raise InterpreterError("tk_label函数需要4个参数：tk_label(父容器, 文字, x, y)")
    parent_id, text, x, y = args
    if not isinstance(text, str):
        raise InterpreterError("第二个参数必须是字符串（标签文字）")
    import tkinter as tk
    parent = _get_widget(parent_id) if parent_id != "root" else _tk_root
    if parent is None:
        raise InterpreterError("请先用 tk_window 创建窗口")
    label = tk.Label(parent, text=text, font=("微软雅黑", 12))
    label.place(x=x, y=y)
    wid = _next_widget_id("label")
    _widgets[wid] = label
    return wid

# tk_button(parent_id, text, x, y)：创建按钮
def tk_button_func(args):
    if len(args) != 4:
        raise InterpreterError("tk_button函数需要4个参数：tk_button(父容器, 文字, x, y)")
    parent_id, text, x, y = args
    if not isinstance(text, str):
        raise InterpreterError("第二个参数必须是字符串（按钮文字）")
    import tkinter as tk
    parent = _get_widget(parent_id) if parent_id != "root" else _tk_root
    if parent is None:
        raise InterpreterError("请先用 tk_window 创建窗口")
    btn = tk.Button(parent, text=text, font=("微软雅黑", 11), width=10)
    btn.place(x=x, y=y)
    wid = _next_widget_id("btn")
    _widgets[wid] = btn
    return wid

# tk_entry(parent_id, x, y, width)：创建输入框
def tk_entry_func(args):
    if len(args) != 4:
        raise InterpreterError("tk_entry函数需要4个参数：tk_entry(父容器, x, y, 宽度)")
    parent_id, x, y, w = args
    import tkinter as tk
    parent = _get_widget(parent_id) if parent_id != "root" else _tk_root
    if parent is None:
        raise InterpreterError("请先用 tk_window 创建窗口")
    entry = tk.Entry(parent, font=("微软雅黑", 11), width=int(w))
    entry.place(x=x, y=y)
    wid = _next_widget_id("entry")
    _widgets[wid] = entry
    return wid

# tk_text(parent_id, x, y, width, height)：创建多行文本框
def tk_text_func(args):
    if len(args) != 5:
        raise InterpreterError("tk_text函数需要5个参数：tk_text(父容器, x, y, 宽度, 高度)")
    parent_id, x, y, w, h = args
    import tkinter as tk
    parent = _get_widget(parent_id) if parent_id != "root" else _tk_root
    if parent is None:
        raise InterpreterError("请先用 tk_window 创建窗口")
    text = tk.Text(parent, font=("微软雅黑", 11), width=int(w), height=int(h))
    text.place(x=x, y=y)
    wid = _next_widget_id("text")
    _widgets[wid] = text
    return wid

# tk_get(widget_id)：获取输入框/文本框内容
def tk_get_func(args):
    if len(args) != 1:
        raise InterpreterError("tk_get函数需要1个参数：tk_get(控件ID)")
    wid = args[0]
    widget = _get_widget(wid)
    import tkinter
    if isinstance(widget, tkinter.Entry):
        return widget.get()
    elif isinstance(widget, tkinter.Text):
        return widget.get("1.0", "end-1c")
    else:
        raise InterpreterError(f"控件 {wid} 不支持 get 操作")

# tk_set(widget_id, text)：设置标签/按钮/文本框内容
def tk_set_func(args):
    if len(args) != 2:
        raise InterpreterError("tk_set函数需要2个参数：tk_set(控件ID, 内容)")
    wid, text = args
    if not isinstance(text, str):
        raise InterpreterError("第二个参数必须是字符串")
    widget = _get_widget(wid)
    import tkinter
    if isinstance(widget, (tkinter.Label, tkinter.Button)):
        widget.config(text=text)
    elif isinstance(widget, tkinter.Text):
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
    else:
        raise InterpreterError(f"控件 {wid} 不支持 set 操作")
    return "内容已设置"

# tk_command(button_id, hope_func_name)：给按钮绑定点击事件
def tk_command_func(args):
    if len(args) != 2:
        raise InterpreterError("tk_command函数需要2个参数：tk_command(按钮ID, 函数名)")
    wid, func_name = args
    button = _get_widget(wid)
    import tkinter
    if not isinstance(button, tkinter.Button):
        raise InterpreterError(f"控件 {wid} 不是按钮")
    # 按钮点击时调用 Hope 函数（通过 Hope 解释器的全局调用接口）
    # 这里用一个回调占位，实际由 Hope 解释器注入执行器
    button.config(command=lambda: _tk_callback(func_name))
    return f"按钮 {wid} 已绑定函数 {func_name}"

# 回调分发器（由 Hope 解释器在启动时注入 _tk_run_hope_func）
_tk_run_hope_func = None

def _tk_callback(func_name):
    if _tk_run_hope_func is not None:
        _tk_run_hope_func(func_name, [])

# tk_mainloop()：启动窗口消息循环
def tk_mainloop_func(args):
    if len(args) != 0:
        raise InterpreterError("tk_mainloop函数不需要参数")
    if _tk_root is None:
        raise InterpreterError("请先用 tk_window 创建窗口")
    _tk_root.mainloop()
    return "窗口已关闭"


# ========== 导出字典 ==========

TKINTER_FUNCTIONS = {
    "tk_window": (["title", "width", "height"], tk_window_func),
    "tk_label": (["parent", "text", "x", "y"], tk_label_func),
    "tk_button": (["parent", "text", "x", "y"], tk_button_func),
    "tk_entry": (["parent", "x", "y", "width"], tk_entry_func),
    "tk_text": (["parent", "x", "y", "width", "height"], tk_text_func),
    "tk_get": (["widget_id"], tk_get_func),
    "tk_set": (["widget_id", "text"], tk_set_func),
    "tk_command": (["button_id", "func_name"], tk_command_func),
    "tk_mainloop": ([], tk_mainloop_func)
}
