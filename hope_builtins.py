from typing import Union
from errors import InterpreterError


# 整型转字符串函数
def int_to_str(args):
    if len(args) != 1:
        raise InterpreterError("int_to_str函数期望1个参数")
    num = args[0]
    if type(num).__name__ != 'int':
        raise InterpreterError("int_to_str仅支持整数类型")

    if num == 0:
        return "0"
    is_negative = False
    if num < 0:
        is_negative = True
        num = abs(num)
    str_val = ""
    while num > 0:
        last_digit = num % 10
        char = chr(48 + last_digit)
        str_val = char + str_val
        num = num // 10
    if is_negative:
        str_val = "-" + str_val
    return str_val
#任意值转换为字符串
def to_str(args):
    """将任意值转换为字符串，支持整数、浮点数、字符串、列表"""
    if len(args) != 1:
        raise InterpreterError("str函数期望1个参数")
    val = args[0]

    # 整数转字符串（保留原逻辑）
    if isinstance(val, int):
        if val == 0:
            return "0"
        is_negative = False
        if val < 0:
            is_negative = True
            val = -val
        str_val = ""
        while val > 0:
            last_digit = val % 10
            char = chr(48 + last_digit)
            str_val = char + str_val
            val //= 10
        if is_negative:
            str_val = "-" + str_val
        return str_val

    # 浮点数转字符串
    elif isinstance(val, float):
        # 去除末尾多余的 .0 保持整洁（可选）
        s = str(val)
        if s.endswith('.0'):
            s = s[:-2]
        return s

    # 字符串直接返回
    elif isinstance(val, str):
        return val

    # 列表转字符串，格式如 [1, 2, 3]
    elif isinstance(val, list):
        parts = []
        for item in val:
            # 递归调用 to_str 处理每个元素（但注意 to_str 接收列表参数）
            # 简单起见，使用 Python 的 str，但字符串元素不会加引号
            # 如果想保留引号，可使用 repr(item)，这里为了清晰，不加引号
            parts.append(str(item))
        return "[" + ", ".join(parts) + "]"

    else:
        raise InterpreterError(f"str函数不支持类型 {type(val).__name__}")
#字符串/数字转整数函数
def int_func(args):
     if len(args) != 1:
         raise InterpreterError("int函数期望1个参数")
     val = args[0]
     # 支持字符串（数字格式）、浮点数转整数
     if type(val).__name__ == 'str':
         try:
             return int(val)
         except ValueError:
             raise InterpreterError("int函数仅支持可以转换为整数的字符串")
     elif type(val).__name__ == 'float':
         return int(val)
     elif type(val).__name__ == 'int':
         return val
     else:
         raise InterpreterError("int函数仅支持字符串、整数或浮点数")
# 字符串/数字转浮点数函数
def float_func(args):
     if len(args) != 1:
         raise InterpreterError("float函数期望1个参数")
     val = args[0]
     # 支持字符串（数字格式）、整数转浮点数
     if type(val).__name__ == 'str':
         try:
             return float(val)
         except ValueError:
             raise InterpreterError("float函数仅支持可以转换为浮点数的字符串")
     elif type(val).__name__ == 'int':
         return float(val)
     elif type(val).__name__ == 'float':
         return val
     else:
         raise InterpreterError("float函数仅支持字符串、整数或浮点数")
         

# 长度计算函数
def len_func(args):
    if len(args) != 1:
        raise InterpreterError("len函数期望1个参数")
    val = args[0]
    # 支持字符串和列表
    if isinstance(val, (str, list)):
        return len(val)
    # 支持整数和浮点数（转换为字符串后计算长度）
    elif isinstance(val, (int, float)):
        return len(str(val))
    else:
        raise InterpreterError("len函数仅支持字符串、列表、整数或浮点数")

# 最大值函数
def max_func(args):
    if len(args) < 1:
        raise InterpreterError("max函数至少需要1个参数")
    nums = []
    for arg in args:
        if type(arg).__name__ in ['int', 'float']:
            nums.append(arg)
        else:
            raise InterpreterError("max函数仅支持数字类型的参数")
    if not nums:
        raise InterpreterError("max函数需要至少1个有效数字参数")
    return max(nums)

# 最小值函数
def min_func(args):
    if len(args) < 1:
        raise InterpreterError("min函数至少需要1个参数")
    nums = []
    for arg in args:
        if type(arg).__name__ in ['int', 'float']:
            nums.append(arg)
        else:
            raise InterpreterError("min函数仅支持数字类型的参数")
    if not nums:
        raise InterpreterError("min函数需要至少1个有效数字参数")
    return min(nums)

# 求和函数
def sum_func(args):
    if len(args) < 1:
        raise InterpreterError("sum函数至少需要1个参数")
    total = 0
    for arg in args:
        if type(arg).__name__ in ['int', 'float']:
            total += arg
        else:
            raise InterpreterError("sum函数仅支持数字类型的参数")
    return total
# range函数：生成整数序列，支持1-3个参数
def range_func(args):
    arg_len = len(args)
    if arg_len < 1 or arg_len > 3:
        raise InterpreterError("range函数支持1-3个参数")
    
    # 处理参数，只支持整数
    for arg in args:
        if type(arg).__name__ != 'int':
            raise InterpreterError("range函数仅支持整数参数")
    
    if arg_len == 1:
        start = 0
        stop = args[0]
        step = 1
    elif arg_len == 2:
        start = args[0]
        stop = args[1]
        step = 1
    else:
        start = args[0]
        stop = args[1]
        step = args[2]
        if step == 0:
            raise InterpreterError("range函数的步长不能为0")
    
    # 生成序列
    result = []
    current = start
    if step > 0:
        while current < stop:
            result.append(current)
            current += step
    else:
        while current > stop:
            result.append(current)
            current += step
    return result

# enumerate函数：给序列添加索引，返回(索引, 值)的列表
def enumerate_func(args):
    if len(args) != 1:
        raise InterpreterError("enumerate函数期望1个参数")
    seq = args[0]
    # 仅支持列表类型（hope中用模拟的列表实现）
    if type(seq).__name__ != 'list':
        raise InterpreterError("enumerate函数仅支持列表类型")
    
    result = []
    for idx, val in enumerate(seq):
        result.append((idx, val))
    return result

# zip函数：合并多个序列，返回元组列表
def zip_func(args):
    if len(args) < 1:
        raise InterpreterError("zip函数至少需要1个参数")
    # 检查所有参数都是列表
    for seq in args:
        if type(seq).__name__ != 'list':
            raise InterpreterError("zip函数仅支持列表类型的参数")
    
    # 按最短的序列进行合并
    result = []
    min_len = min(len(seq) for seq in args)
    for i in range(min_len):
        item = tuple(seq[i] for seq in args)
        result.append(item)
    return result
#type函数：返回值的类型名称
def type_func(args):
     if len(args) != 1:
         raise InterpreterError("type函数期望1个参数")
     val = args[0]
     return type(val).__name__
# id函数：返回值的内存地址（Python的id）
def id_func(args):
     if len(args) != 1:
         raise InterpreterError("id函数期望1个参数")
     val = args[0]
     return id(val)
#保留两位小数
def round_two_decimals(num:Union[int,float]) ->Union[str,float]:
    # if isinstance(num,str):
    #     try:
    #         num=float(num)
    #     except ValueError:
    #         return "错误：参数必须是数字类型"
    if not isinstance(num[0],(int,float)):
        return "错误：参数必须是数字类型"
    try:
        return round(num[0],2)
    except Exception as e:
        return "错误：处理失败{str(e)}"
def round_custom_decimals(num:Union[int,float]) ->Union[str,float]:
    if not isinstance(num[0],(int,float)):
        return "错误：参数必须是数字类型"
    try:
        return round(num[0],num[1])
    except Exception as e:
        return "错误：处理失败{str(e)}"
# ========== 字符串增强 ==========
def str_get(args):
    """获取字符串中指定索引的字符，str_get(s, index)"""
    if len(args) != 2:
        raise InterpreterError("str_get 需要2个参数: 字符串, 索引")
    s, idx = args[0], args[1]
    if type(s).__name__ != 'str':
        raise InterpreterError("第一个参数必须是字符串")
    if type(idx).__name__ != 'int':
        raise InterpreterError("索引必须是整数")
    if idx < 0 or idx >= len(s):
        raise InterpreterError(f"索引 {idx} 超出范围 (0-{len(s)-1})")
    return s[idx]

def str_slice(args):
    """字符串切片 str_slice(s, start, end)，end可选，默认到末尾"""
    if len(args) not in (2, 3):
        raise InterpreterError("str_slice 需要2或3个参数: 字符串, 起始[, 结束]")
    s = args[0]
    if type(s).__name__ != 'str':
        raise InterpreterError("第一个参数必须是字符串")
    start = args[1]
    if type(start).__name__ != 'int':
        raise InterpreterError("起始索引必须是整数")
    end = args[2] if len(args) == 3 else len(s)
    if type(end).__name__ != 'int':
        raise InterpreterError("结束索引必须是整数")
    # 处理负索引
    start = start if start >= 0 else len(s) + start
    end = end if end >= 0 else len(s) + end
    start = max(0, min(start, len(s)))
    end = max(0, min(end, len(s)))
    if start >= end:
        return ""
    return s[start:end]

def str_find(args):
    """查找子串，返回第一个匹配的索引，找不到返回-1。str_find(s, sub)"""
    if len(args) != 2:
        raise InterpreterError("str_find 需要2个参数: 字符串, 子串")
    s, sub = args[0], args[1]
    if type(s).__name__ != 'str' or type(sub).__name__ != 'str':
        raise InterpreterError("两个参数都必须是字符串")
    return s.find(sub)

def str_split(args):
    """分割字符串，返回列表。str_split(s, sep)"""
    if len(args) != 2:
        raise InterpreterError("str_split 需要2个参数: 字符串, 分隔符")
    s, sep = args[0], args[1]
    if type(s).__name__ != 'str' or type(sep).__name__ != 'str':
        raise InterpreterError("两个参数都必须是字符串")
    return s.split(sep)

# ========== 列表增强 ==========
def list_append(args):
    """向列表末尾追加元素。list_append(lst, item)"""
    if len(args) != 2:
        raise InterpreterError("list_append 需要2个参数: 列表, 元素")
    lst, item = args[0], args[1]
    if type(lst).__name__ != 'list':
        raise InterpreterError("第一个参数必须是列表")
    lst.append(item)
    return None  # 无返回值

def list_pop(args):
    """弹出并返回列表最后一个元素。list_pop(lst)"""
    if len(args) != 1:
        raise InterpreterError("list_pop 需要1个参数: 列表")
    lst = args[0]
    if type(lst).__name__ != 'list':
        raise InterpreterError("参数必须是列表")
    if not lst:
        raise InterpreterError("不能从空列表弹出元素")
    return lst.pop()

def list_set(args):
    """设置列表指定索引的值。list_set(lst, index, value)"""
    if len(args) != 3:
        raise InterpreterError("list_set 需要3个参数: 列表, 索引, 新值")
    lst, idx, val = args[0], args[1], args[2]
    if type(lst).__name__ != 'list':
        raise InterpreterError("第一个参数必须是列表")
    if type(idx).__name__ != 'int':
        raise InterpreterError("索引必须是整数")
    if idx < 0 or idx >= len(lst):
        raise InterpreterError(f"索引 {idx} 超出范围 (0-{len(lst)-1})")
    lst[idx] = val
    return None

# ========== 文件 I/O ==========
def file_read(args):
    """读取整个文件内容，返回字符串。file_read(path)"""
    if len(args) != 1:
        raise InterpreterError("file_read 需要1个参数: 文件路径")
    path = args[0]
    if type(path).__name__ != 'str':
        raise InterpreterError("文件路径必须是字符串")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise InterpreterError(f"读取文件失败: {str(e)}")

def file_write(args):
    """写入字符串到文件（覆盖模式）。file_write(path, content)"""
    if len(args) != 2:
        raise InterpreterError("file_write 需要2个参数: 文件路径, 内容")
    path, content = args[0], args[1]
    if type(path).__name__ != 'str':
        raise InterpreterError("文件路径必须是字符串")
    if type(content).__name__ != 'str':
        raise InterpreterError("内容必须是字符串")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return None
    except Exception as e:
        raise InterpreterError(f"写入文件失败: {str(e)}")

def file_append(args):
    """追加字符串到文件末尾。file_append(path, content)"""
    if len(args) != 2:
        raise InterpreterError("file_append 需要2个参数: 文件路径, 内容")
    path, content = args[0], args[1]
    if type(path).__name__ != 'str':
        raise InterpreterError("文件路径必须是字符串")
    if type(content).__name__ != 'str':
        raise InterpreterError("内容必须是字符串")
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)
        return None
    except Exception as e:
        raise InterpreterError(f"追加文件失败: {str(e)}")

# ========== 异常处理辅助 ==========
def try_catch(args):
    """
    执行一个无参函数，如果发生异常则执行错误处理函数。
    try_catch(func, handler) -> 返回 func() 的结果，若出错则调用 handler(err) 并返回其返回值。
    """
    if len(args) != 2:
        raise InterpreterError("try_catch 需要2个参数: 要执行的函数, 错误处理函数")
    func, handler = args[0], args[1]
    # 注意：func 和 handler 应该是 Hope 的函数对象（在 interpreter 中表现为 ('FUNC_CALL', ...) 或内置函数）
    # 这里简单假设传入的是已经可调用的对象（实际在解释器中，func 是函数名，需要特殊处理）
    # 更好的实现是扩展语法 try-except，但为简化，我们在 interpreter 中特殊处理 try_catch 调用。
    raise NotImplementedError("try_catch 需要配合 interpreter 修改，请参考下文解释器改动")  
# 定义内置函数的注册列表
BUILTIN_FUNCTIONS = {
    "itr": (["num"], int_to_str),
    "str": (["val"], to_str),
    "int": (["val"], int_func),
    "float": (["val"], float_func),
    "len": (["val"], len_func),
    "max": (["*args"], max_func),
    "min": (["*args"], min_func),
    "sum": (["*args"], sum_func),
    "range": (["*args"], range_func),
    "enumerate": (["seq"], enumerate_func),
    "zip": (["*args"], zip_func),
    "type": (["val"], type_func),
    "id": (["val"], id_func),
    "round_two": (["val"], round_two_decimals),
    "round_custom": (["num","decimals"], round_custom_decimals),
    # 新增字符串函数
    "str_get": (["s", "idx"], str_get),
    "str_slice": (["s", "start", "end"], str_slice),
    "str_find": (["s", "sub"], str_find),
    "str_split": (["s", "sep"], str_split),
    # 新增列表函数
    "list_append": (["lst", "item"], list_append),
    "list_pop": (["lst"], list_pop),
    "list_set": (["lst", "idx", "val"], list_set),
    # 新增文件函数
    "file_read": (["path"], file_read),
    "file_write": (["path", "content"], file_write),
    "file_append": (["path", "content"], file_append),
    # try_catch 稍后在解释器中实现，暂不注册为普通内置函数
}