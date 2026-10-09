#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2026/9/29 18:21

"""
hope_vm.py — Hope语言对外嵌入API模块
版本: 1.5.2
说明:
    ✅ 本模块仅用于外部Python程序嵌入Hope语言；
    ✅ hopes.py(原生命令行REPL)不引用此文件，保持原有逻辑不变；
    ✅ interpreter.py / lexer.py / parser.py / errors.py 全部零修改；
    ✅ 每个 HopeVM 实例拥有独立隔离的运行环境。

【重要限制 方案A(不修改interpreter.py)固有约束】
    1. 不支持嵌套双向回调：不要在register_native注册的Python回调内部调用 vm.call / vm.run_code；
    2. vm.call() 参数仅支持 int/float/str/list；不能传递自定义Python对象；
    3. 多线程：不要多线程共享同一个HopeVM实例，每个线程新建独立 vm = HopeVM()；
    4. 与hopes.py原生解释器环境互相隔离：
       - hopes.py：加载 hope_builtins.BUILTIN_FUNCTIONS，不会加载 hope_sys.SYS_FUNCTIONS
       - HopeVM：屏蔽原生builtin加载，自动加载 hope_libs.hope_sys.SYS_FUNCTIONS

对外公共API列表：
    vm = HopeVM()
        创建全新隔离虚拟机实例

    vm.register_native(func_name:str, param_names:list[str], callback)
        Python注册原生函数，供Hope脚本调用。
        callback 接收一个参数:args(列表，已经是hope值)，返回python值。

    vm.run_code(source:str)
        执行Hope源码字符串；变量、函数持久保存在VM内部环境；抛出解析/运行异常。

    vm.run_file(file_path:str)
        读取并执行 .hope 脚本文件。

    vm.call(func_name:str, *py_args)
        Python调用Hope脚本中定义的函数，返回执行结果；
        内部实现：拼接临时代码+全局临时变量中转。

    vm.set_global(var_name:str, py_value)
        设置虚拟机全局变量，Python值自动转为Hope内部值。

    vm.get_global(var_name:str)
        读取虚拟机全局变量，返回Python类型值。

使用示例：
    from hope_vm import HopeVM
    vm = HopeVM()
    def mul(args):
        a,b = args
        return a*b
    vm.register_native("mul",["a","b"],mul)
    vm.run_code('''
    func add(a,b){
        return a + b
    }
    ''')
    res = vm.call("add",10,20)
    print(res)
"""

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import LexerError, ParserError, InterpreterError
from hope_libs.hope_sys import SYS_FUNCTIONS


def py_to_hope(value):
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        return value
    elif isinstance(value, list):
        return [py_to_hope(x) for x in value]
    elif value is None:
        return None
    else:
        raise InterpreterError(f"不支持Python类型 {type(value)}")


def hope_to_py(value):
    return value


class HopeVM:
    def __init__(self):
        self._shared_env = {
            "PI": 3.1415926535,
            "E": 2.7182818284
        }
        self._shared_functions = {}
        self._load_system_lib()

    def _load_system_lib(self):
        for fname, (param_names, cb) in SYS_FUNCTIONS.items():
            self._shared_functions[fname] = (param_names, cb)

    def register_native(self, func_name, param_names, callback):
        self._shared_functions[func_name] = (param_names, callback)

    def _make_interp(self, source):
        lexer = Lexer(source)
        parser = Parser(lexer)
        interp = Interpreter(parser)

        def dummy_add_builtin(self):
            pass
        interp._add_builtin_functions = dummy_add_builtin.__get__(interp, Interpreter)

        interp.env = self._shared_env
        interp.functions = self._shared_functions
        return interp

    def run_code(self, source):
        try:
            interp = self._make_interp(source)
            interp.run()
            # ★关键修复：函数调用会把 self.env 换成 copy 副本，
            #   必须把副本里的新变量（__temp_ret__等）回写到共享环境
            self._shared_env.update(interp.env)
        except (LexerError, ParserError, InterpreterError) as e:
            raise e

    def run_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            src = f.read()
        return self.run_code(src)

    def call(self, func_name, *py_args):
        if func_name not in self._shared_functions:
            raise InterpreterError(f"函数 {func_name} 未定义")

        def to_lit(v):
            if isinstance(v, str):
                return '"' + v.replace('"', '\\"') + '"'
            elif isinstance(v, bool):
                return "true" if v else "false"
            elif isinstance(v, (int, float)):
                return str(v)
            elif isinstance(v, list):
                items = ",".join(to_lit(i) for i in v)
                return "[" + items + "]"
            else:
                raise InterpreterError(f"call()不支持类型 {type(v)}")

        arg_text = ",".join(to_lit(a) for a in py_args)
        temp_code = "set __temp_ret__ = " + func_name + "(" + arg_text + ")"
        self.run_code(temp_code)

        ret = self._shared_env.get("__temp_ret__")
        self._shared_env.pop("__temp_ret__", None)
        return hope_to_py(ret)

    def set_global(self, var_name, py_value):
        self._shared_env[var_name] = py_to_hope(py_value)

    def get_global(self, var_name):
        if var_name not in self._shared_env:
            raise InterpreterError(f"全局变量 {var_name} 未定义")
        return hope_to_py(self._shared_env[var_name])
