import random
from errors import InterpreterError

# random()：返回0-1的随机浮点数
def random_func(args):
    if len(args) != 0:
        raise InterpreterError("random函数不需要参数")
    return random.random()

# randint(a, b)：返回a到b的随机整数
def randint_func(args):
    if len(args) != 2:
        raise InterpreterError("randint函数需要2个参数：randint(最小值, 最大值)")
    a, b = args[0], args[1]
    if not (isinstance(a, int) and isinstance(b, int)):
        raise InterpreterError("randint函数的参数必须是整数")
    if a > b:
        raise InterpreterError("randint函数的第一个参数不能大于第二个参数")
    return random.randint(a, b)

# choice(seq)：从列表随机选择一个元素
def choice_func(args):
    if len(args) != 1:
        raise InterpreterError("choice函数需要1个参数：choice(列表)")
    seq = args[0]
    if not isinstance(seq, list):
        raise InterpreterError("choice函数的参数必须是列表")
    if len(seq) == 0:
        raise InterpreterError("choice函数的参数不能是空列表")
    return random.choice(seq)

def hope_seed(args):
    if len(args) !=1:
        raise InterpreterError("seed 需要1参数：seed(随机种子)")
    random.seed(args[0])
    return "种子设置完成"

RANDOM_FUNCTIONS = {
    "random": ([], random_func),
    "randint": (["min", "max"], randint_func),
    "choice": (["seq"], choice_func),
    "seed": ([], hope_seed)
}
