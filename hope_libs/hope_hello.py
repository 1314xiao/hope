from errors import InterpreterError


def hello_func(args):
    # 允许参数为空，为空时使用默认值"world"
    if len(args) > 1:
        raise InterpreterError("hello函数最多支持1个参数（名称）")
    # 处理参数，为空的话使用默认值
    name = args[0] if args and args[0] != "" else "world"
    if type(name).__name__ != 'str':
        raise InterpreterError("hello函数仅支持字符串参数")
    
    class Hello:
        def __init__(self, name):
            self.name = name
        
        def greet(self):
            return f"Hello {self.name}"
    
    hello_obj = Hello(name)
    return hello_obj.greet()
            
# 注册函数的地方不需要修改
#BUILTIN_FUNCTIONS["hello"] = (["name"], hello_func)
EGG_HELLO = {
     "_hello": ([], hello_func)
 }