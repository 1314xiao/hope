import os
import tempfile
import shutil
from errors import InterpreterError

# ========== 核心函数 ==========
def exists(args):
    if len(args) != 1:
        raise InterpreterError("fs.exists(路径): 需传入1个路径参数")
    path = args[0]
    return os.path.exists(str(path))

def read_file(args):
    if len(args) != 1:
        raise InterpreterError("fs.read_file(路径): 需传入1个文件路径参数")
    path = str(args[0])
    if not os.path.isfile(path):
        raise InterpreterError(f"文件不存在: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(args):
    if len(args) != 2:
        raise InterpreterError("fs.write_file(路径, 内容): 需传入路径和内容2个参数")
    path, content = str(args[0]), str(args[1])
    parent_dir = os.path.dirname(path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def mkdir(args):
    if len(args) != 1:
        raise InterpreterError("fs.mkdir(路径): 需传入1个目录路径参数")
    path = str(args[0])
    os.makedirs(path, exist_ok=True)
    return True

def list_dir(args):
    if len(args) != 1:
        raise InterpreterError("fs.list_dir(路径): 需传入1个目录路径参数")
    path = str(args[0])
    if not os.path.isdir(path):
        raise InterpreterError(f"目录不存在: {path}")
    return os.listdir(path)

def temp_dir(args):
    if len(args) != 0:
        raise InterpreterError("fs.temp_dir(): 无需传入参数")
    return tempfile.mkdtemp(prefix="hope_packer_")

def remove(args):
    if len(args) != 1:
        raise InterpreterError("fs.remove(路径): 需传入1个路径参数")
    path = str(args[0])
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    return True

def basename(args):
    if len(args) != 1:
        raise InterpreterError("fs.basename(路径): 需传入1个路径参数")
    return os.path.basename(str(args[0]))

def dirname(args):
    if len(args) != 1:
        raise InterpreterError("fs.dirname(路径): 需传入1个路径参数")
    return os.path.dirname(str(args[0]))

# ========== Hope 库注册字典 ==========
FS_FUNCTIONS = {
    "exists": ([], exists),
    "read_file": ([], read_file),
    "write_file": (["path", "content"], write_file),
    "mkdir": ([], mkdir),
    "list_dir": ([], list_dir),
    "temp_dir": ([], temp_dir),
    "remove": ([], remove),
    "basename": ([], basename),
    "dirname": ([], dirname)
}
