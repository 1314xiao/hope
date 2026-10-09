from errors import InterpreterError

# 初始化turtle画布，全局只初始化一次
_turtle_screen = None
_turtle_pen = None
_turtle_module = None

def _init_turtle():
    global _turtle_screen, _turtle_pen, _turtle_module
    if _turtle_screen is None:
        import turtle as _turtle_module
        _turtle_screen = _turtle_module.Screen()
        _turtle_screen.title("Hope Turtle 绘图")
        _turtle_pen = _turtle_module.Turtle()
        _turtle_pen.speed(6)

# turtle_forward(distance)：画笔前进指定距离
def turtle_forward_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_forward函数需要1个参数：turtle_forward(距离)")
    distance = args[0]
    if not isinstance(distance, (int, float)):
        raise InterpreterError("turtle_forward函数的参数必须是数字")
    _init_turtle()
    _turtle_pen.forward(distance)
    return "画笔前进完成"

# turtle_turn(angle)：画笔左转指定角度
def turtle_turn_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_turn函数需要1个参数：turtle_turn(角度)")
    angle = args[0]
    if not isinstance(angle, (int, float)):
        raise InterpreterError("turtle_turn函数的参数必须是数字")
    _init_turtle()
    _turtle_pen.left(angle)
    return "画笔转向完成"

# turtle_title(title_text)：设置绘图窗口标题
def turtle_title_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_title函数需要1个参数：turtle_title(窗口标题)")
    title_text = args[0]
    if not isinstance(title_text, str):
        raise InterpreterError("turtle_title函数的参数必须是字符串")
    _init_turtle()
    try:
        _turtle_screen.title(title_text)
        return f"窗口标题已设置为：{title_text}"
    except Exception as e:
        raise InterpreterError(f"设置标题失败：{str(e)}")

#turtle_bgcolor(color): 设置背景颜色
def turtle_bgcolor_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_bgcolor函数需要1个参数：turtle_bgcolor(颜色名)")
    color = args[0]
    if not isinstance(color, str):
        raise InterpreterError("turtle_bgcolor函数的参数必须是字符串")
    _init_turtle()
    try:
        _turtle_screen.bgcolor(color)
        return f"背景颜色已设置为{color}"
    except Exception as e:
        raise InterpreterError(f"颜色设置失败：{str(e)}")

# turtle_speed(speed)：设置画笔速度 0-10
def turtle_speed_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_speed函数需要1个参数：turtle_speed(速度0-10)")
    speed = args[0]
    if not isinstance(speed, (int, float)):
        raise InterpreterError("速度必须是数字")
    _init_turtle()
    _turtle_pen.speed(int(speed))
    return f"画笔速度已设置为{int(speed)}"

# turtle_clear()：清空画布，不重置画笔位置
def turtle_clear_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_clear函数不需要参数")
    _init_turtle()
    _turtle_pen.clear()
    return "画布已清空"

# turtle_reset()：重置画笔和画布到初始状态
def turtle_reset_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_reset函数不需要参数")
    _init_turtle()
    _turtle_pen.reset()
    return "画布已重置"

# turtle_hide()：隐藏画笔（只留图形，不显示箭头）
def turtle_hide_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_hide函数不需要参数")
    _init_turtle()
    _turtle_pen.hideturtle()
    return "画笔已隐藏"

# turtle_show()：显示画笔箭头
def turtle_show_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_show函数不需要参数")
    _init_turtle()
    _turtle_pen.showturtle()
    return "画笔已显示"

# turtle_pensize(size)：设置画笔粗细
def turtle_pensize_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_pensize函数需要1个参数：turtle_pensize(粗细)")
    size = args[0]
    if not isinstance(size, (int, float)):
        raise InterpreterError("粗细必须是数字")
    _init_turtle()
    _turtle_pen.pensize(int(size))
    return f"画笔粗细已设置为{int(size)}"

# turtle_undo()：撤销上一步绘图
def turtle_undo_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_undo函数不需要参数")
    _init_turtle()
    _turtle_pen.undo()
    return "已撤销上一步"

# turtle_dot(size, color)：在当前位置画一个点
def turtle_dot_func(args):
    if len(args) != 2:
        raise InterpreterError("turtle_dot函数需要2个参数：turtle_dot(直径, 颜色)")
    size, color = args[0], args[1]
    if not isinstance(size, (int, float)):
        raise InterpreterError("直径必须是数字")
    if not isinstance(color, str):
        raise InterpreterError("颜色必须是字符串")
    _init_turtle()
    _turtle_pen.dot(int(size), color)
    return "已画点"

# turtle_write(text, size)：在画笔位置写文字
def turtle_write_func(args):
    if len(args) != 2:
        raise InterpreterError("turtle_write函数需要2个参数：turtle_write(文字, 字号)")
    text, size = args[0], args[1]
    if not isinstance(text, str):
        raise InterpreterError("文字必须是字符串")
    if not isinstance(size, (int, float)):
        raise InterpreterError("字号必须是数字")
    _init_turtle()
    _turtle_pen.write(text, font=("微软雅黑", int(size), "normal"))
    return f"已写入文字：{text}"

# turtle_home()：画笔回到原点(0,0)，方向朝右
def turtle_home_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_home函数不需要参数")
    _init_turtle()
    _turtle_pen.home()
    return "画笔已回到原点"

# turtle_width(w, h)：设置画布窗口大小
def turtle_size_func(args):
    if len(args) != 2:
        raise InterpreterError("turtle_size函数需要2个参数：turtle_size(宽度, 高度)")
    w, h = args[0], args[1]
    if not (isinstance(w, (int, float)) and isinstance(h, (int, float))):
        raise InterpreterError("宽高必须是数字")
    _init_turtle()
    _turtle_screen.setup(int(w), int(h))
    return f"窗口大小已设置为{int(w)}x{int(h)}"

# turtle_color(color)：设置画笔颜色
def turtle_color_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_color函数需要1个参数：turtle_color(颜色名)")
    color = args[0]
    if not isinstance(color, str):
        raise InterpreterError("turtle_color函数的参数必须是字符串")
    _init_turtle()
    try:
        _turtle_pen.color(color)
        return f"画笔颜色已设置为{color}"
    except Exception as e:
        raise InterpreterError(f"颜色设置失败：{str(e)}")

# turtle_circle(radius)：绘制指定半径的圆形
def turtle_circle_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_circle函数需要1个参数：turtle_circle(半径)")
    radius = args[0]
    if not isinstance(radius, (int, float)):
        raise InterpreterError("turtle_circle函数的参数必须是数字")
    _init_turtle()
    _turtle_pen.circle(radius)
    return "圆形绘制完成"

# turtle_done()：保持绘图窗口
def turtle_done_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_done函数不需要参数")
    _init_turtle()
    _turtle_module.done()
    return "绘图窗口已保持"

# turtle_up()：抬起画笔
def turtle_up_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_up函数不需要参数")
    _init_turtle()
    _turtle_pen.penup()
    return "画笔已抬起"

# turtle_down()：落下画笔
def turtle_down_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_down函数不需要参数")
    _init_turtle()
    _turtle_pen.pendown()
    return "画笔已落下"

# turtle_goto(x, y)：移动画笔到指定坐标
def turtle_goto_func(args):
    if len(args) != 2:
        raise InterpreterError("turtle_goto函数需要2个参数：turtle_goto(x坐标, y坐标)")
    x, y = args[0], args[1]
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
        raise InterpreterError("turtle_goto函数的参数必须是数字")
    _init_turtle()
    _turtle_pen.goto(x, y)
    return f"画笔已移动到({x}, {y})"

# turtle_fillstart()：开始填充图形
def turtle_fillstart_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_fillstart函数不需要参数")
    _init_turtle()
    _turtle_pen.begin_fill()
    return "已开始图形填充"

# turtle_fillend()：结束填充图形
def turtle_fillend_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_fillend函数不需要参数")
    _init_turtle()
    _turtle_pen.end_fill()
    return "已结束图形填充"

# tracer(n) 关闭/开启自动画布刷新
def tracer_func(args):
    if len(args) != 1:
        raise InterpreterError("turtle_tracer 需要1个参数 turtle_tracer(n)")
    n = args[0]
    if not isinstance(n, int):
        raise InterpreterError("参数必须是整数")
    _turtle_screen.tracer(n)
    return f"tracer 设置为{n}"

# update() 手动刷新画布
def update_func(args):
    if len(args) != 0:
        raise InterpreterError("turtle_update 不需要参数")
    _turtle_screen.update()
    return "画布已手动更新"

# 定义turtle库的函数列表，和其他扩展库格式统一
TURTLE_FUNCTIONS = {
    "turtle_forward": (["distance"], turtle_forward_func),
    "turtle_turn": (["angle"], turtle_turn_func),
    "turtle_color": (["color"], turtle_color_func),
    "turtle_bgcolor": (["color"], turtle_bgcolor_func),
    # ↓新增这一行
    "turtle_title": (["title_text"], turtle_title_func),
    "turtle_speed": (["speed"], turtle_speed_func),
    "turtle_clear": ([], turtle_clear_func),
    "turtle_reset": ([], turtle_reset_func),
    "turtle_hide": ([], turtle_hide_func),
    "turtle_show": ([], turtle_show_func),
    "turtle_pensize": (["size"], turtle_pensize_func),
    "turtle_undo": ([], turtle_undo_func),
    "turtle_dot": (["size", "color"], turtle_dot_func),
    "turtle_write": (["text", "size"], turtle_write_func),
    "turtle_home": ([], turtle_home_func),
    "turtle_size": (["w", "h"], turtle_size_func),
    "turtle_circle": (["radius"], turtle_circle_func),
    "turtle_done": ([], turtle_done_func),
    "turtle_up": ([], turtle_up_func),
    "turtle_down": ([], turtle_down_func),
    "turtle_goto": (["x", "y"], turtle_goto_func),
    "turtle_fillstart": ([], turtle_fillstart_func),
    "turtle_fillend": ([], turtle_fillend_func),
    # ...你原有所有turtle函数
    "turtle_tracer": (["n"], tracer_func),
    "turtle_update": ([], update_func)
}
