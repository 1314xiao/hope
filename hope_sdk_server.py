#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2026/9/29 23:21
# hope_sdk_server.py

import sys
import json
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import LexerError, ParserError, InterpreterError
from hope_vm import HopeVM


def run_sdk_main():
    vm = HopeVM()
    sys.stdout.reconfigure(line_buffering=True)

    while True:
        try:
            line = sys.stdin.readline()
        except EOFError:
            break
        if not line:
            continue
        line = line.strip()
        if not line:
            continue

        resp = {"ok": True, "data": None, "error": ""}
        should_exit = False
        try:
            req = json.loads(line)
            action = req.get("action")

            if action == "run_code":
                src = req["source"]
                vm.run_code(src)
                resp["data"] = None

            elif action == "call":
                func_name = req["func"]
                args = req["args"]
                ret = vm.call(func_name, *args)
                resp["data"] = ret

            elif action == "set_global":
                var = req["var"]
                val = req["value"]
                vm.set_global(var, val)
                resp["data"] = None

            elif action == "get_global":
                var = req["var"]
                resp["data"] = vm.get_global(var)

            elif action == "quit":
                resp["data"] = "exit"
                should_exit = True

            else:
                resp["ok"] = False
                resp["error"] = f"未知action:{action}"

        except Exception as e:
            resp["ok"] = False
            resp["error"] = str(e)

        # 无论正常还是异常，都回写一条JSON；quit也先回写再退出
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()

        if should_exit:
            break


if __name__ == "__main__":
    run_sdk_main()

