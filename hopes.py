#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2025/11/9 18:21

import sys
import os
import readline  # 提供命令行编辑历史功能（可选）

# 直接导入同路径下的核心模块
try:
    from lexer import Lexer
    from parser import Parser
    from interpreter import Interpreter
    from errors import LexerError, ParserError, InterpreterError
except ImportError:
    print("错误：同目录下缺少 lexer.py、parser.py、interpreter.py、errors.py 核心文件！")
    sys.exit(1)

HOPE_VERSION = "1.5.1"

def run_repl():
    """交互式 REPL：逐行执行代码，保持环境"""
    #print("Hope 语言交互环境 (REPL)")
    #print("输入 'exit()' 或 'quit()' 退出")
    #print("注意：多行语句（如函数定义）请写在一行内\n")
    print(f"Hope {HOPE_VERSION} (tags/v1.5.1:de54cf5, Apr  4 2026, 10:12:12) [py v.2025 64 bit (AMD64)] on win32")
    print("Please write multi-line statements in a single line")
    print("Type 'exit()' or 'quit()' to exit.")
    # 创建解释器实例，环境会持续保留
    dummy_parser = Parser(Lexer(""))  # 临时解析器，后面每行会重新创建
    interpreter = Interpreter(dummy_parser)
    
    while True:
        try:
            line = input(">>> ")
        except EOFError:
            print()
            break
        
        line = line.strip()
        if line in ('exit()', 'quit()'):
            break
        if not line:
            continue
        
        # 每次将单行代码包装为完整程序执行
        try:
            lexer = Lexer(line)
            parser = Parser(lexer)
            # 注意：需要重新设置 interpreter 的 parser 为当前行解析器
            interpreter.parser = parser
            interpreter.run()
        except (LexerError, ParserError, InterpreterError) as e:
            print(f"错误: {e}")
        except Exception as e:
            print(f"未知错误: {e}")

def run_file(file_path):
    """执行 .hope 文件"""
    if not os.path.exists(file_path) or not file_path.endswith('.hope'):
        print("错误：请传入有效 .hope 文件路径")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        hope_code = f.read()
    try:
        print(f"执行 {file_path}...")
        lexer = Lexer(hope_code)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.run()
        print("执行完成！")
    except (LexerError, ParserError, InterpreterError) as e:
        print(f"执行错误：{e}")
    except Exception as e:
        print(f"未知错误：{str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        run_repl()
    else:
        run_file(sys.argv[1])