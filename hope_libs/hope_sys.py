import sys
import os
from errors import InterpreterError

# ========== 核心函数 ==========
def os(args):
    if len(args) != 0:
        raise InterpreterError("sys.os(): 无需传入参数")
    plat = sys.platform
    if plat.startswith("win"):
        return "windows"
    elif plat == "linux":
        return "linux"
    elif plat == "darwin":
        return "macos"
    return "unknown"

def argv(args):
    if len(args) != 0:
        raise InterpreterError("sys.argv(): 无需传入参数")
    return sys.argv

def get_env(args):
    if len(args) != 1:
        raise InterpreterError("sys.get_env(变量名): 需传入1个环境变量名参数")
    return os.environ.get(str(args[0]), "")

def exit(args):
    if len(args) == 0:
        sys.exit(0)
    elif len(args) == 1:
        code = args[0]
        if isinstance(code, int):
            sys.exit(code)
        raise InterpreterError("exit 退出码必须是整数")
    raise InterpreterError("sys.exit(退出码): 最多传入1个整数参数")

def hope_print(args):
    # 简易print，兼容你现有的show，也可以单独print
    print(*args)
    return ""

# ========== Hope 库注册字典 ==========
SYS_FUNCTIONS = {
    "os": ([], os),
    "argv": ([], argv),
    "get_env": (["var_name"], get_env),
    "exit": ([], exit),
    "print": ([], hope_print)
}
