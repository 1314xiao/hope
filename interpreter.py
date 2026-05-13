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
        self.modules = {}  # 缓存已导入的模块：模块名 -> 模块环境字典

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
        """
        动态加载 Hope 模块。
        1. 如果 lib_name 在内置扩展库映射中，则加载 Python 扩展
        2. 否则，从文件系统查找并加载 .hope 文件
        """
        # 1. 先检查内置扩展库（lib_config.hope 配置的）
        if lib_name in self.lib_map:
            self._load_python_extension(lib_name)
            return

        # 2. 检查是否已缓存
        if lib_name in self.modules:
            # 将缓存的模块环境合并到当前环境
            for name, value in self.modules[lib_name].items():
                if name not in self.env:  # 不覆盖已有变量
                    self.env[name] = value
            return

        # 3. 查找 .hope 文件
        hope_file = self._find_hope_file(lib_name)
        if not hope_file:
            raise InterpreterError(f"无法找到模块 '{lib_name}'（未找到 .hope 文件）")

        # 4. 读取并执行模块代码（在独立环境中）
        try:
            with open(hope_file, 'r', encoding='utf-8') as f:
                module_code = f.read()
        except Exception as e:
            raise InterpreterError(f"读取模块文件失败: {str(e)}")

        # 创建独立的模块环境（继承当前环境的部分内容？为简单起见，全新环境）
        module_env = {}
        # 保留原始环境
        old_env = self.env
        self.env = module_env

        try:
            from lexer import Lexer
            from parser import Parser
            lexer = Lexer(module_code)
            parser = Parser(lexer)
            module_ast = parser.parse()
            for stmt in module_ast[1]:
                self._eval_stmt(stmt)
        except Exception as e:
            self.env = old_env
            raise InterpreterError(f"加载模块 '{lib_name}' 失败: {str(e)}")

        # 恢复当前环境
        self.env = old_env

        # 将模块中的非内置变量（排除以下）导入到当前环境
        builtin_names = dir(__builtins__) if '__builtins__' in globals() else []
        builtin_names.extend(['PI', 'E'])  # 预定义常量
        for name, value in module_env.items():
            # 排除内置变量、私有变量（以_开头）以及函数对象中的特殊属性
            if name.startswith('_') or name in builtin_names:
                continue
            # 避免覆盖当前环境已有变量（可改为警告或覆盖，这里选择不覆盖）
            if name not in self.env:
                self.env[name] = value

        # 缓存模块环境（以备后续重复导入）
        self.modules[lib_name] = module_env

    def _load_python_extension(self, lib_name: str):
        """加载 Python 扩展（原有逻辑）"""
        module_name, func_dict_name = self.lib_map[lib_name]
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, base_path)
        try:
            module = __import__(module_name)
            func_dict = getattr(module, func_dict_name)
            for name, func_def in func_dict.items():
                self.functions[name] = func_def
        except ImportError:
            lib_file = os.path.join(base_path, f"{module_name}.py")
            if not os.path.exists(lib_file):
                raise InterpreterError(f"扩展库文件 {module_name}.py 缺失")
            raise InterpreterError(f"无法导入扩展库：{lib_name}（文件存在但导入失败）")
        except AttributeError:
            raise InterpreterError(f"扩展库 {lib_name} 格式错误，缺少 {func_dict_name} 字典")

    def _find_hope_file(self, lib_name: str) -> str:
        """
        查找 .hope 文件，搜索顺序：
        1. 当前工作目录
        2. 脚本所在目录下的 hope_libs 子目录
        3. 可执行文件所在目录下的 hope_libs 子目录（打包后）
        """
        # 候选路径列表
        candidates = []
        # 当前工作目录
        candidates.append(os.path.join(os.getcwd(), f"{lib_name}.hope"))
        # 脚本所在目录 / hope_libs
        script_dir = os.path.dirname(os.path.abspath(__file__))
        candidates.append(os.path.join(script_dir, "hope_libs", f"{lib_name}.hope"))
        # 打包后 exe 所在目录 / hope_libs
        if hasattr(sys, '_MEIPASS'):
            exe_dir = os.path.dirname(sys.executable)
            candidates.append(os.path.join(exe_dir, "hope_libs", f"{lib_name}.hope"))
        # 用户可在此扩展其他路径

        for path in candidates:
            if os.path.exists(path):
                return path
        return None
    
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