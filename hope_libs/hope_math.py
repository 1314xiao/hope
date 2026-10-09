import math
from errors import InterpreterError

# 常用数学常量
def math_pi_func(args):
    if len(args) != 0:
        raise InterpreterError("math_pi函数不需要参数")
    return math.pi

def math_e_func(args):
    if len(args) != 0:
        raise InterpreterError("math_e函数不需要参数")
    return math.e

# 基本数学运算
def math_abs_func(args):
    if len(args) != 1:
        raise InterpreterError("math_abs函数需要1个参数：math_abs(数字)")
    num = args[0]
    if not isinstance(num, (int, float)):
        raise InterpreterError("math_abs函数的参数必须是数字")
    return abs(num)

def math_sqrt_func(args):
    if len(args) != 1:
        raise InterpreterError("math_sqrt函数需要1个参数：math_sqrt(数字)")
    num = args[0]
    if not isinstance(num, (int, float)):
        raise InterpreterError("math_sqrt函数的参数必须是数字")
    if num < 0:
        raise InterpreterError("math_sqrt函数的参数不能是负数")
    return math.sqrt(num)

def math_pow_func(args):
    if len(args) != 2:
        raise InterpreterError("math_pow函数需要2个参数：math_pow(底数, 指数)")
    base, exp = args[0], args[1]
    if not (isinstance(base, (int, float)) and isinstance(exp, (int, float))):
        raise InterpreterError("math_pow函数的参数必须是数字")
    return math.pow(base, exp)

# 三角函数（弧度）
def math_sin_func(args):
    if len(args) != 1:
        raise InterpreterError("math_sin函数需要1个参数：math_sin(弧度值)")
    rad = args[0]
    if not isinstance(rad, (int, float)):
        raise InterpreterError("math_sin函数的参数必须是数字")
    return math.sin(rad)

def math_cos_func(args):
    if len(args) != 1:
        raise InterpreterError("math_cos函数需要1个参数：math_cos(弧度值)")
    rad = args[0]
    if not isinstance(rad, (int, float)):
        raise InterpreterError("math_cos函数的参数必须是数字")
    return math.cos(rad)

def math_tan_func(args):
    if len(args) != 1:
        raise InterpreterError("math_tan函数需要1个参数：math_tan(弧度值)")
    rad = args[0]
    if not isinstance(rad, (int, float)):
        raise InterpreterError("math_tan函数的参数必须是数字")
    return math.tan(rad)

# 角度和弧度的转换
def math_radians_func(args):
    if len(args) != 1:
        raise InterpreterError("math_radians函数需要1个参数：math_radians(角度值)")
    deg = args[0]
    if not isinstance(deg, (int, float)):
        raise InterpreterError("math_radians函数的参数必须是数字")
    return math.radians(deg)

def math_degrees_func(args):
    if len(args) != 1:
        raise InterpreterError("math_degrees函数需要1个参数：math_degrees(弧度值)")
    rad = args[0]
    if not isinstance(rad, (int, float)):
        raise InterpreterError("math_degrees函数的参数必须是数字")
    return math.degrees(rad)

# 原有函数保留，新增以下函数
# --------------------------
# 对数相关函数
def math_log_func(args):
    if len(args) < 1 or len(args) > 2:
        raise InterpreterError("math_log函数需要1-2个参数：math_log(数字, [底数])")
    num = args[0]
    base = args[1] if len(args) == 2 else math.e
    if not (isinstance(num, (int, float)) and isinstance(base, (int, float))):
        raise InterpreterError("math_log函数的参数必须是数字")
    if num <= 0 or base <= 0 or base == 1:
        raise InterpreterError("math_log函数的数字必须大于0，底数必须大于0且不等于1")
    return math.log(num, base)

def math_log10_func(args):
    if len(args) != 1:
        raise InterpreterError("math_log10函数需要1个参数：math_log10(数字)")
    num = args[0]
    if not isinstance(num, (int, float)):
        raise InterpreterError("math_log10函数的参数必须是数字")
    if num <= 0:
        raise InterpreterError("math_log10函数的参数必须大于0")
    return math.log10(num)

# 取整相关函数
def math_ceil_func(args):
    if len(args) != 1:
        raise InterpreterError("math_ceil函数需要1个参数：math_ceil(数字)")
    num = args[0]
    if not isinstance(num, (int, float)):
        raise InterpreterError("math_ceil函数的参数必须是数字")
    return math.ceil(num)

def math_floor_func(args):
    if len(args) != 1:
        raise InterpreterError("math_floor函数需要1个参数：math_floor(数字)")
    num = args[0]
    if not isinstance(num, (int, float)):
        raise InterpreterError("math_floor函数的参数必须是数字")
    return math.floor(num)

def math_round_func(args):
    if len(args) < 1 or len(args) > 2:
        raise InterpreterError("math_round函数需要1-2个参数：math_round(数字, [保留小数位数])")
    num = args[0]
    ndigits = args[1] if len(args) == 2 else 0
    if not isinstance(num, (int, float)) or not isinstance(ndigits, int):
        raise InterpreterError("math_round函数的数字参数必须是数字，小数位数必须是整数")
    return round(num, ndigits)

# 其他补充数学函数
def math_modf_func(args):
    if len(args) != 1:
        raise InterpreterError("math_modf函数需要1个参数：math_modf(数字)")
    num = args[0]
    if not isinstance(num, (int, float)):
        raise InterpreterError("math_modf函数的参数必须是数字")
    frac, integ = math.modf(num)
    return [frac, integ]

# 更新MATH_FUNCTIONS，加入新增的函数
MATH_FUNCTIONS = {
    # 原有函数保留...
    "math_pi": ([], math_pi_func),
    "math_e": ([], math_e_func),
    "math_abs": (["num"], math_abs_func),
    "math_sqrt": (["num"], math_sqrt_func),
    "math_pow": (["base", "exp"], math_pow_func),
    "math_sin": (["rad"], math_sin_func),
    "math_cos": (["rad"], math_cos_func),
    "math_tan": (["rad"], math_tan_func),
    "math_radians": (["deg"], math_radians_func),
    "math_degrees": (["rad"], math_degrees_func),
    # 新增的对数、取整函数
    "math_log": (["num", "base"], math_log_func),
    "math_log10": (["num"], math_log10_func),
    "math_ceil": (["num"], math_ceil_func),
    "math_floor": (["num"], math_floor_func),
    "math_round": (["num", "ndigits"], math_round_func),
    "math_modf": (["num"], math_modf_func)
}