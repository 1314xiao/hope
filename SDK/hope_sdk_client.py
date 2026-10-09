#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2026/9/29 23:21

import subprocess
import json


class HopeSdkClient:
    def __init__(self, exe_path: str):
        self.proc = subprocess.Popen(
            [exe_path, "--sdk"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    def _send(self, payload: dict):
        req_str = json.dumps(payload, ensure_ascii=False) + "\n"
        self.proc.stdin.write(req_str)
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        return json.loads(line)

    def run_code(self, source: str):
        resp = self._send({"action": "run_code", "source": source})
        if not resp["ok"]:
            raise RuntimeError(resp["error"])
        return resp["data"]

    def call(self, func_name: str, *args):
        resp = self._send({"action": "call", "func": func_name, "args": list(args)})
        if not resp["ok"]:
            raise RuntimeError(resp["error"])
        return resp["data"]

    def set_global(self, var_name: str, value):
        resp = self._send({"action": "set_global", "var": var_name, "value": value})
        if not resp["ok"]:
            raise RuntimeError(resp["error"])
        return resp["data"]

    def get_global(self, var_name: str):
        resp = self._send({"action": "get_global", "var": var_name})
        if not resp["ok"]:
            raise RuntimeError(resp["error"])
        return resp["data"]

    def close(self):
        self._send({"action": "quit"})
        self.proc.wait()

if __name__ == "__main__":
    client = HopeSdkClient(r"hope.exe")
    client.run_code("""
func add(a,b){
    return a + b
}
func calc(x,y){
    set t = add(x,y)
    return t * 2
}
""")
    print("calc(10,20) =", client.call("calc",10,20))
    print("calc(5,7) =", client.call("calc",5,7))
    client.set_global("g", 1234)
    print("g =", client.get_global("g"))
    client.close()
