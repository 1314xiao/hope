from typing import Callable, Any

class HopeCmdDispatcher:
    def __init__(self):
        self._cmd_map: dict[str, Callable[..., Any]] = {}

    def register_cmd(self, cmd_name: str):
        def decorator(func: Callable[..., Any]):
            name = cmd_name.strip()
            self._cmd_map[name] = func
            return func
        return decorator

    def unregister(self, cmd_name: str):
        cmd_name = cmd_name.strip()
        if cmd_name in self._cmd_map:
            del self._cmd_map[cmd_name]

    def dispatch(self, cmd_str: str, *args, **kwargs) -> Any:
        cmd_str = cmd_str.strip()
        if cmd_str not in self._cmd_map:
            print(f"[HopeCmdDispatcher] 未知指令：{cmd_str}")
            return None
        target_func = self._cmd_map[cmd_str]
        try:
            return target_func(cmd_str, *args, **kwargs)
        except Exception as e:
            print(f"[HopeCmdDispatcher] 执行异常【{cmd_str}】：{repr(e)}")
            return None

hope_dispatcher = HopeCmdDispatcher()


# hope_decide_equal(left, right, value) 需要3个参数
def hope_decide_equal(args):
    """
    ffi_cmd_dispatch(left, right, value)
    left == right 则返回 value，否则返回 None
    """
    if len(args) != 3:
        raise InterpreterError("hope_decide_equal(left, right, value) 需要3个参数")
    left = args[0]
    right = args[1]
    val = args[2]

    if left == right:
        # 条件成立，调用Hope侧传入的函数对象
        return val
    # 条件不成立，不执行val，直接返回None
    return None

# hope_decide_equals(left, right, true_value, false_value) 需要4个参数
def hope_decide_equals(args):
    """
    ffi_cmd_dispatch(left, right, value)
    left == right 则返回 value，否则返回 None
    """
    if len(args) != 4:
        raise InterpreterError("hope_decide_equals(left, right, true_value, false_value) 需要4个参数")
    left = args[0]
    right = args[1]
    val = args[2]
    val1 = args[3]

    if left == right:
        # 条件成立，调用Hope侧传入的函数对象
        return val
    # 条件不成立，执行val1，直接返回Hope侧传入的函数对象
    else:
        return val1

# hope_decide_rather(left, op, right, callback) 需要4个参数
def hope_decide_rather(args):
    if len(args) != 4:
        raise InterpreterError("hope_decide_rather(left, op, right, callback) 需要4个参数")
    left = args[0]
    op = args[1]
    right = args[2]
    callback = args[3]

    cond = False
    if op == "==":
        cond = left == right
    elif op == "!=":
        cond = left != right
    elif op == ">":
        cond = left > right
    elif op == "<":
        cond = left < right
    elif op == ">=":
        cond = left >= right
    elif op == "<=":
        cond = left <= right
    else:
        raise InterpreterError(f"不支持的比较运算符: {op}")

    if cond:
        return callback
    return None

def hope_decide_rathers(args):
    if len(args) != 5:
        raise InterpreterError("hope_decide_rathers(left, op, right, true_callback, false_callback) 需要5个参数")
    left = args[0]
    op = args[1]
    right = args[2]
    true_cb = args[3]
    false_cb = args[4]

    cond = False
    if op == "==":
        cond = left == right
    elif op == "!=":
        cond = left != right
    elif op == ">":
        cond = left > right
    elif op == "<":
        cond = left < right
    elif op == ">=":
        cond = left >= right
    elif op == "<=":
        cond = left <= right
    else:
        raise InterpreterError(f"不支持的比较运算符: {op}")

    if cond:
        return true_cb
    else:
        return false_cb

# 德摩根定律
# !(A && B)  =  !A || !B
# !(A || B)  =  !A && !B
# hope_decide_law(logic_op, cond_list, true_name, false_name) 需要4个参数
def hope_decide_law(args):
    try:
        if len(args) != 4:
            raise InterpreterError("hope_decide_law(logic_op, cond_list, true_name, false_name) 需要4个参数")

        logic_op = args[0]
        cond_list = args[1]
        true_name = args[2]
        false_name = args[3]

        if logic_op not in ("AND", "OR"):
            raise InterpreterError(f"logic_op只支持 AND / OR，输入:{logic_op}")

        final_result = None
        for item in cond_list:
            if len(item) != 3:
                raise InterpreterError("条件组每一项格式必须 [left, op, right]")
            left = item[0]
            op = item[1]
            right = item[2]

            res = False
            if op == "==":
                res = left == right
            elif op == "!=":
                res = left != right
            elif op == ">":
                res = left > right
            elif op == "<":
                res = left < right
            elif op == ">=":
                res = left >= right
            elif op == "<=":
                res = left <= right
            else:
                raise InterpreterError(f"不支持运算符 {op}")

            if logic_op == "AND":
                if res is False:
                    final_result = False
                    break
            else:
                if res is True:
                    final_result = True
                    break
        else:
            if logic_op == "AND":
                final_result = True
            else:
                final_result = False

        if final_result:
            return true_name
        else:
            return false_name
    except InterpreterError:
        # 直接抛出给hope解释器处理
        raise
    except Exception as e:
        raise InterpreterError(f"hope_decide_law未知异常: {repr(e)}")


# ===================== HOPE_DECIDE映射表 =====================
HOPE_DECIDE = {
    "decide_equal": (["left","right","value"], hope_decide_equal),
    "decide_equals": (["left","right","true_value", "false_value"], hope_decide_equals),
    "decide_rather": (["left","op","right","callback"], hope_decide_rather),
    "decide_rathers": (["left","op","right","true_callback","false_callback"], hope_decide_rathers),
    "decide_law": (["logic_op", "cond_list", "true_name", "false_name"], hope_decide_law)
}
