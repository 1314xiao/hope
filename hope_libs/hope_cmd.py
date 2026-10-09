# hope_cmd.py - Hope 语言 CMD 接口库的 Python 实现
import subprocess
import sys
import os

class HopeCmdError(Exception):
    """自定义异常，用于封装命令执行错误"""
    pass

def _get_shell():
    """跨平台获取默认 shell"""
    if sys.platform == "win32":
        return ["cmd.exe", "/c"]
    else:
        return ["/bin/bash", "-c"]

def cmd_run(command, capture_output=True, encoding="utf-8"):
    """
    同步执行系统命令
    :param command: 字符串格式的命令
    :param capture_output: 是否捕获输出（stdout/stderr）
    :param encoding: 输出编码
    :return: 字典 {status: 退出码, stdout: 标准输出, stderr: 标准错误}
    """
    try:
        shell_cmd = _get_shell() + [command]
        result = subprocess.run(
            shell_cmd,
            capture_output=capture_output,
            encoding=encoding,
            check=False
        )
        return {
            "status": result.returncode,
            "stdout": result.stdout if capture_output else "",
            "stderr": result.stderr if capture_output else ""
        }
    except Exception as e:
        raise HopeCmdError(f"Command execution failed: {str(e)}")

def cmd_start(command, wait=False):
    """
    启动后台命令/程序（无阻塞）
    :param command: 命令字符串
    :param wait: 是否等待程序退出
    """
    try:
        if sys.platform == "win32":
            # Windows 后台启动无控制台窗口
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            proc = subprocess.Popen(
                command,
                startupinfo=si,
                shell=True
            )
        else:
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        if wait:
            proc.wait()
        return proc.pid
    except Exception as e:
        raise HopeCmdError(f"Start process failed: {str(e)}")

def cmd_interactive():
    """启动交互式命令行会话（接管当前终端）"""
    shell = _get_shell()[0]
    subprocess.run([shell])

# Hope 模块导出表
HOPE_CMD_EXPORTS = {
    "cmd_run": ([], cmd_run),
    "cmd_start": ([], cmd_start),
    "cmd_interactive": ([], cmd_interactive),
}
