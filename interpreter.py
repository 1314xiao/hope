#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2025/11/9 18:30

import sys 
import os
from typing import List, Tuple, Union, Dict, Optional
from parser import Parser, ASTNode
from errors import InterpreterError
from hope_builtins import BUILTIN_FUNCTIONS


class Interpreter:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.env: Dict[str, Union[int, float, str, list]] = {
            "PI": 3.1415926535,
            "E": 2.7182818284  
        }
        self.functions: Dict[str, Union[Tuple[List[str], ASTNode], Tuple[List[str], callable]]] = {}
        self._add_builtin_functions()
        self.lib_map = self._load_lib_config()

    def _load_lib_config(self) -> Dict[str, Tuple[str, str]]:
        config_filename = "lib_config.hope"
        if hasattr(sys, '_MEIPASS'):
            exe_dir = os.path.dirname(sys.executable)
        else:
            exe_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(exe_dir, config_filename)
        lib_map = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_code = f.read()
                from lexer import Lexer
                lexer = Lexer(config_code)
                parser = Parser(lexer)
                config_ast = parser.parse()
                temp_env = self.env.copy()
                old_env = self.env
                self.env = temp_env
                for stmt in config_ast[1]:
                    self._eval_stmt(stmt)
                if "LIB_MAP" in self.env:
                    for item in self.env["LIB_MAP"]:
                        lib_name, module, func_dict = item
                        lib_map[lib_name] = (module, func_dict)
                self.env = old_env
            except Exception as e:
                raise InterpreterError(f"加载配置文件lib_config.hope失败:{str(e)}")
        return lib_map

    def _add_builtin_functions(self):
        for func_name, func_def in BUILTIN_FUNCTIONS.items():
            self.functions[func_name] = func_def

    def _load_hope_lib(self, lib_name: str):
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, base_path)
        if hasattr(sys, '_MEIPASS'):
            exe_dir = os.path.dirname(sys.executable)
        else:
            exe_dir = os.path.dirname(os.path.abspath(__file__))
        self.lib_root = os.path.join(exe_dir, "hope_libs")
        sys.path.insert(0, self.lib_root)
        ext_root = os.path.join(exe_dir, "Lib")
        sys.path.insert(0, ext_root)

        lib_map = self.lib_map
        if lib_name in lib_map:
            module_name, func_name = lib_map[lib_name]
            try:
                module = __import__(module_name)
                func_dict = getattr(module, func_name)
                for name, func_def in func_dict.items():
                    self.functions[name] = func_def
            except ImportError:
                lib_file = os.path.join(base_path, f"{module_name}.py")
                if not os.path.exists(lib_file):
                    raise InterpreterError(f"扩展库文件 {module_name}.py 缺失")
                raise InterpreterError(f"无法导入扩展库：{lib_name}（文件存在但导入失败）")
            except AttributeError:
                raise InterpreterError(f"扩展库 {lib_name} 格式错误，缺少 {func_name} 字典")
        else:
            # 尝试加载 .hope 或 .hopec 脚本库
            lib_filename = os.path.join(ext_root, f"{lib_name}.hopec")
            if not os.path.exists(lib_filename):
                lib_filename = os.path.join(ext_root, f"{lib_name}.hope")
                if not os.path.exists(lib_filename):
                    lib_filename = f"{lib_name}.hopec"
                    if not os.path.exists(lib_filename):
                        lib_filename = f"{lib_name}.hope"
                        if not os.path.exists(lib_filename):
                            raise InterpreterError(f"库文件'{lib_filename}'不存在")
            from lexer import Lexer
            try:
                with open(lib_filename, 'r', encoding='utf-8') as f:
                    lib_code = f.read()
                lib_lexer = Lexer(lib_code)
                lib_parser = Parser(lib_lexer)
                lib_ast = lib_parser.parse()
                for stmt in lib_ast[1]:
                    self._eval_stmt(stmt)
            except InterpreterError as e:
                raise InterpreterError(f"加载库'{lib_name}'失败：{str(e)}")
            except Exception as e:
                raise InterpreterError(f"加载库'{lib_name}'失败（非执行错误）：{str(e)}")

    def _eval_input(self, prompt: str, input_type: str) -> Union[int, float, str]:
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                confirm = input("输入为空，是否确认提交空值？(y/n)：")
                if confirm.lower() == 'y':
                    if input_type == 'str':
                        return ""
                    else:
                        print("错误：整数/浮点数不能为空！")
                        continue
                else:
                    continue
            if input_type == 'str':
                return user_input
            elif input_type == 'int':
                try:
                    return int(user_input)
                except ValueError:
                    print("输入错误！请输入整数，重新输入：")
                    continue
            elif input_type == 'float':
                try:
                    return float(user_input)
                except ValueError:
                    print("输入错误！请输入数字，重新输入：")
                    continue
            else:
                raise InterpreterError(f"不支持的input类型: {input_type}")

    def _eval_arith(self, node: ASTNode) -> Union[int, float, str, list]:
        if node[0] == 'INPUT_STMT':
            return self._eval_stmt(node)
        elif node[0] == 'NUM':
            return node[1]
        elif node[0] == 'VAR':
            var_name = node[1]
            if var_name not in self.env:
                raise InterpreterError(f"变量'{var_name}'未定义")
            return self.env[var_name]
        elif node[0] == 'LIST':
            return [self._eval_arith(item) for item in node[1]]
        elif node[0] == 'INDEXED_VAR':
            var_name, index_expr = node[1], node[2]
            if var_name not in self.env:
                raise InterpreterError(f"变量'{var_name}'未定义")
            var_val = self.env[var_name]
            if not isinstance(var_val, list):
                raise InterpreterError(f"变量'{var_name}'不是列表，无法使用索引")
            index = self._eval_arith(index_expr)
            if not isinstance(index, int):
                raise InterpreterError("列表索引必须是整数")
            if index < 0 or index >= len(var_val):
                raise InterpreterError(f"列表索引{index}超出范围（列表长度为{len(var_val)}）")
            return var_val[index]
        elif node[0] == 'ARITH_EXPR':
            op, left, right = node[1], node[2], node[3]
            left_val = self._eval_arith(left)
            right_val = self._eval_arith(right)
            
            if op == '+':
                # 字符串与数字自动转换
                if isinstance(left_val, str) and isinstance(right_val, str):
                    return left_val + right_val
                if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                    return left_val + right_val
                if isinstance(left_val, str) and isinstance(right_val, (int, float)):
                    return left_val + str(right_val)
                if isinstance(left_val, (int, float)) and isinstance(right_val, str):
                    return str(left_val) + right_val
                raise InterpreterError(f"加法不支持 {type(left_val).__name__} 和 {type(right_val).__name__} 类型")
            elif op == '-':
                if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                    return left_val - right_val
                raise InterpreterError("减法仅支持数字类型")
            elif op == '*':
                if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                    return left_val * right_val
                raise InterpreterError("乘法仅支持数字类型")
            elif op == '/':
                if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                    if right_val == 0:
                        raise InterpreterError("除法除数不能为0")
                    return left_val / right_val
                raise InterpreterError("除法仅支持数字类型")
            elif op == '%':
                if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                    if right_val == 0:
                        raise InterpreterError("取模运算除数不能为0")
                    return left_val % right_val
                raise InterpreterError("取模仅支持数字类型")
            else:
                raise InterpreterError(f"不支持的算术运算符: {op}")
        elif node[0] == 'FUNC_CALL':
            func_name, args = node[1], node[2]
            if func_name not in self.functions:
                raise InterpreterError(f"函数'{func_name}'未定义")
            func_def = self.functions[func_name]
            if callable(func_def[1]):
                arg_values = [self._eval_arith(arg) for arg in args]
                return func_def[1](arg_values)
            else:
                func_params, func_body = func_def
                if len(args) != len(func_params):
                    raise InterpreterError(f"函数'{func_name}'期望{len(func_params)}个参数，实际传入{len(args)}个")
                old_env = self.env.copy()
                for param, arg in zip(func_params, args):
                    self.env[param] = self._eval_arith(arg)
                return_val = None
                for stmt in func_body[1]:
                    ret = self._eval_stmt(stmt)
                    if ret is not None:
                        return_val = ret
                        break
                self.env = old_env
                return return_val
        elif node[0] == 'STR':
            return node[1]
        else:
            raise InterpreterError(f"非法算术表达式节点'{node[0]}'")

    def _eval_cond(self, node: ASTNode) -> bool:
        op, left, right = node[1], node[2], node[3]
        left_val = self._eval_arith(left)
        right_val = self._eval_arith(right)
        if not isinstance(left_val, (int, float, str)) or not isinstance(right_val, (int, float, str)):
            raise InterpreterError("仅数字和字符串支持比较")
        if op == '==':
            return left_val == right_val
        elif op == '>':
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val > right_val
            return False
        elif op == '<':
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val < right_val
            return False
        elif op == '>=':
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val >= right_val
            return False
        elif op == '<=':
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val <= right_val
            return False
        else:
            raise InterpreterError(f"不支持的比较运算符'{op}'")

    def _eval_stmt(self, stmt: ASTNode) -> Optional[Union[int, float, str]]:
        # 提取行号（语句节点格式为 (type, line, ...)）
        stmt_type = stmt[0]
        line = stmt[1] if len(stmt) > 1 and isinstance(stmt[1], int) else None

        try:
            if stmt_type == 'INPUT_STMT':
                _, line, (prompt, input_type) = stmt
                return self._eval_input(prompt, input_type)
            elif stmt_type == 'IMPORT_STMT':
                _, line, lib_name = stmt
                self._load_hope_lib(lib_name)
            elif stmt_type == 'SET_STMT':
                _, line, var_name, expr_node = stmt
                self.env[var_name] = self._eval_arith(expr_node)
            elif stmt_type == 'SET_IDX_STMT':
                _, line, var_name, index_node, expr_node = stmt
                if var_name not in self.env:
                    raise InterpreterError(f"变量'{var_name}'未定义")
                lst = self.env[var_name]
                if not isinstance(lst, list):
                    raise InterpreterError(f"变量'{var_name}'不是列表，无法使用索引赋值")
                idx = self._eval_arith(index_node)
                if not isinstance(idx, int):
                    raise InterpreterError("列表索引必须是整数")
                if idx < 0 or idx >= len(lst):
                    raise InterpreterError(f"索引{idx}超出范围(0-{len(lst)-1})")
                val = self._eval_arith(expr_node)
                lst[idx] = val
            elif stmt_type == 'SHOW_STMT':
                _, line, expr_list = stmt
                outputs = []
                for expr in expr_list:
                    val = self._eval_arith(expr)
                    outputs.append(str(val))
                print(" ".join(outputs))
            elif stmt_type == 'RETURN_STMT':
                _, line, expr = stmt
                return self._eval_arith(expr)
            elif stmt_type == 'FUNC_DEF':
                _, line, func_name, params, body = stmt
                self.functions[func_name] = (params, body)
            elif stmt_type == 'LOOP_STMT':
                _, line, cond, body = stmt
                while self._eval_cond(cond):
                    for s in body[1]:
                        self._eval_stmt(s)
            elif stmt_type == 'IF_STMT':
                _, line, cond, if_body, else_body = stmt
                if self._eval_cond(cond):
                    for s in if_body[1]:
                        self._eval_stmt(s)
                elif else_body:
                    for s in else_body[1]:
                        self._eval_stmt(s)
            elif stmt_type == 'EXPR_STMT':
                _, line, expr = stmt
                self._eval_arith(expr)
            else:
                raise InterpreterError(f"未知语句类型: {stmt_type}")
        except InterpreterError as e:
            # 重新抛出带行号的异常
            if line is not None:
                raise InterpreterError(f"[第{line}行] {str(e)}")
            else:
                raise
        return None

    def run(self):
        ast = self.parser.parse()
        if ast[0] == 'PROGRAM':
            for stmt in ast[1]:
                self._eval_stmt(stmt)
