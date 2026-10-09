import os
from errors import InterpreterError

# 之前的函数保留，新增os相关函数

# getcwd()：返回当前工作目录
def os_getcwd_func(args):
    if len(args) != 0:
        raise InterpreterError("getcwd函数不需要参数")
    return os.getcwd()

# listdir(path)：返回指定目录下的所有文件和目录名列表，默认返回当前目录
def os_listdir_func(args):
    path = args[0] if len(args) == 1 else "."
    if not isinstance(path, str):
        raise InterpreterError("listdir函数的参数必须是字符串")
    if not os.path.exists(path):
        raise InterpreterError(f"目录 {path} 不存在")
    if not os.path.isdir(path):
        raise InterpreterError(f"{path} 不是一个目录")
    return os.listdir(path)

# exists(path)：判断指定的文件/目录是否存在，返回True/False
def os_exists_func(args):
    if len(args) != 1:
        raise InterpreterError("exists函数需要1个参数：exists(路径)")
    path = args[0]
    if not isinstance(path, str):
        raise InterpreterError("exists函数的参数必须是字符串")
    return os.path.exists(path)

# isfile(path)：判断指定路径是否是文件，返回True/False
def os_isfile_func(args):
    if len(args) != 1:
        raise InterpreterError("isfile函数需要1个参数：isfile(路径)")
    path = args[0]
    if not isinstance(path, str):
        raise InterpreterError("isfile函数的参数必须是字符串")
    return os.path.isfile(path)

# isdir(path)：判断指定路径是否是目录，返回True/False
def os_isdir_func(args):
    if len(args) != 1:
        raise InterpreterError("isdir函数需要1个参数：isdir(路径)")
    path = args[0]
    if not isinstance(path, str):
        raise InterpreterError("isdir函数的参数必须是字符串")
    return os.path.isdir(path)
import os
from errors import InterpreterError

# 之前的函数保留，新增文件读写函数

# readfile(path)：读取指定文本文件的内容，返回字符串
def readfile_func(args):
    if len(args) != 1:
        raise InterpreterError("readfile函数需要1个参数：readfile(文件路径)")
    path = args[0]
    if not isinstance(path, str):
        raise InterpreterError("readfile函数的参数必须是字符串")
    if not os.path.exists(path):
        raise InterpreterError(f"文件 {path} 不存在")
    if not os.path.isfile(path):
        raise InterpreterError(f"{path} 不是一个文件")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise InterpreterError(f"读取文件失败：{str(e)}")

# writefile(path, content, append=False)：写入内容到指定文本文件
# append为True时追加写入，默认是覆盖写入
def writefile_func(args):
    if len(args) < 2 or len(args) > 3:
        raise InterpreterError("writefile函数需要2-3个参数：writefile(文件路径, 内容, [是否追加])")
    path = args[0]
    content = args[1]
    append = args[2] if len(args) == 3 else False

    if not isinstance(path, str):
        raise InterpreterError("writefile函数的路径参数必须是字符串")
    if not isinstance(content, str):
        raise InterpreterError("writefile函数的内容参数必须是字符串")
    if not isinstance(append, bool):
        raise InterpreterError("writefile函数的append参数必须是布尔值")

    try:
        mode = 'a' if append else 'w'
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
        return "文件写入成功"
    except Exception as e:
        raise InterpreterError(f"写入文件失败：{str(e)}")

# 更新BUILTIN_FUNCTIONS
OS_FUNCTIONS={
    "readfile": (["path"], readfile_func),
    "writefile": (["path", "content", "append"], writefile_func),
    "getcwd": ([], os_getcwd_func),
    "listdir": (["path"], os_listdir_func),
    "exists": (["path"], os_exists_func),
    "isfile": (["path"], os_isfile_func),
    "isdir": (["path"], os_isdir_func)
}
