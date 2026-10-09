from errors import InterpreterError

# Hope语言介绍彩蛋
def hope_intro_egg(args):
    if len(args) != 0:
        raise InterpreterError("这个函数不需要参数哦")
    return """
========================================
    🎉 欢迎了解 Hope 编程语言 🎉
========================================
这是一个晓海亲手开发的轻量级解释型语言：
1.  📝 语 法简洁：接近Python，更易上手
2.  🛠️ 内 置功能：列表/工具函数/类型处理一应俱全
3.  🎨 可 扩展：能轻松新增内置函数和自定义功能
4.  🎮 小 彩蛋：还有隐藏的惊喜等你发现

你可以试试这些操作：
- set name = input("输入你的名字：")
- show(hello(name))
- show(range(1, 10))
========================================
(这是Hope的专属介绍彩蛋哦)
"""

# 之前的惊喜彩蛋
def easter_egg_func(args):
    if len(args) != 0:
        raise InterpreterError("这个函数不需要参数哦")
    return """
🎉 Hope解释器彩蛋触发！ 🎉
你发现了隐藏的小惊喜~
这个解释器是你一步步开发出来的，
已经支持了变量、函数、列表、内置工具等很多功能啦！
继续加油，把它变得更强大吧！
------------------------
(这是一个隐藏的彩蛋哦)
"""

# 彩蛋函数的注册列表
EGG_FUNCTIONS = {
    "_hope_intro": ([], hope_intro_egg),
    "_surprise": ([], easter_egg_func)
}