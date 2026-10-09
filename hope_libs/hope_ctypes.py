from errors import InterpreterError
import ctypes
from ctypes import CDLL, WinDLL
from ctypes import CFUNCTYPE
# WndProc回调签名：LRESULT(HWND, UINT, WPARAM, LPARAM)
WNDPROC = CFUNCTYPE(ctypes.c_ssize_t, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p)
#全局保存回调实例，防止垃圾回收释放
_ffi_callback_store = []
_ffi_lib_pool = {}
_next_handle_id = 1
_ffi_restype_map = {}
# key：内存基地址(int)  value：(buf对象,分配字节大小)
_ffi_owned_memory = dict()
# Windows系统库
_kernel32 = CDLL("kernel32.dll")
_kernel32.FreeLibrary.argtypes = [ctypes.c_void_p]
_kernel32.FreeLibrary.restype = ctypes.c_int
# 返回类型映射表
RESTYPE_MAP = {
    "int": ctypes.c_int,
    "void*": ctypes.c_void_p,
    "str": ctypes.c_char_p,
    "wstr": ctypes.c_wchar_p
}

def hope_load(args):
    if len(args) not in (1, 2):
        raise InterpreterError("load(库路径,[是否stdcall:1/0])")
    libpath = str(args[0])
    stdcall = bool(args[1]) if len(args) == 2 else False
    try:
        if stdcall:
            lib = WinDLL(libpath)
        else:
            lib = CDLL(libpath)
    except Exception as e:
        raise InterpreterError(f"加载DLL失败:{e}")
    global _next_handle_id
    hid = _next_handle_id
    _ffi_lib_pool[hid] = {
        "lib": lib,
        "hmodule": lib._handle
    }
    _next_handle_id += 1
    return hid

def hope_ffi_set_restype(args):
    if len(args) != 3:
        raise InterpreterError("ffi_set_restype(库id,函数名,返回类型)")
    hid = args[0]
    func_name = str(args[1])
    type_key = str(args[2])
    if hid not in _ffi_lib_pool:
        raise InterpreterError(f"无效库句柄 {hid}")
    if type_key not in RESTYPE_MAP:
        raise InterpreterError(f"不支持的返回类型，可选：int,void*,str,wstr")
    _ffi_restype_map[(hid, func_name)] = RESTYPE_MAP[type_key]
    return 0

def hope_ffi_call(args):
    if len(args) < 2:
        raise InterpreterError("ffi_call(库id,函数名,...参数)")
    hid = args[0]
    funcname = str(args[1])
    call_args = args[2:]
    if hid not in _ffi_lib_pool:
        raise InterpreterError(f"无效库句柄 {hid}")
    entry = _ffi_lib_pool[hid]
    lib = entry["lib"]
    try:
        fn = getattr(lib, funcname)
    except AttributeError:
        raise InterpreterError(f"DLL内未找到导出函数: {funcname}")
    restype = _ffi_restype_map.get((hid, funcname), ctypes.c_int)
    fn.restype = restype
    c_args = []
    for arg in call_args:
        if isinstance(arg, int):
            c_args.append(ctypes.c_void_p(arg))
        elif isinstance(arg, float):
            c_args.append(ctypes.c_double(arg))
        elif isinstance(arg, str):
            raise InterpreterError("ffi_call不允许直接传入字符串，请使用ffi_alloc_a / ffi_alloc_w获取指针")
        elif arg is None:
            c_args.append(ctypes.c_void_p(0))
        else:
            raise InterpreterError(f"FFI不支持该参数类型 {type(arg)}")
    res = fn(*c_args)
    if restype == ctypes.c_char_p:
        if res:
            res = res.decode("gbk", errors="replace")
        else:
            res = ""
    elif restype == ctypes.c_wchar_p:
        res = res if res else ""
    elif restype == ctypes.c_void_p:
        res = ctypes.cast(res, ctypes.c_void_p).value
    return res

def hope_free_lib(args):
    if len(args) != 1:
        raise InterpreterError("free_lib(库id)")
    hid = args[0]
    if hid not in _ffi_lib_pool:
        return 0
    entry = _ffi_lib_pool[hid]
    hmod = entry["hmodule"]
    ret = _kernel32.FreeLibrary(hmod)
    keys_to_del = [k for k in _ffi_restype_map if k[0]==hid]
    for k in keys_to_del:
        del _ffi_restype_map[k]
    del _ffi_lib_pool[hid]
    return 0

def hope_ffi_alloc(args):
    """ffi_alloc(size) 分配原始字节缓冲区，返回指针"""
    if len(args) != 1:
        raise InterpreterError("ffi_alloc(字节数)")
    size = int(args[0])
    if size <= 0:
        raise InterpreterError("分配大小必须大于0")
    buf = ctypes.create_string_buffer(size)
    ptr = ctypes.cast(buf, ctypes.c_void_p).value
    _ffi_owned_memory[ptr] = (buf, size)
    return ptr

def hope_ffi_alloc_a(args):
    """ffi_alloc_a(str) GBK‑ANSI字符串缓冲区，返回指针（以0结尾）"""
    if len(args) !=1:
        raise InterpreterError("ffi_alloc_a(字符串)")
    text = str(args[0])
    data = text.encode("gbk",errors="replace") + b"\x00"
    buf = ctypes.create_string_buffer(data)
    ptr = ctypes.cast(buf, ctypes.c_void_p).value
    _ffi_owned_memory[ptr] = (buf, len(data))
    return ptr

def hope_ffi_alloc_w(args):
    """ffi_alloc_w(str) UTF‑16LE宽字符串缓冲区，返回指针（以0结尾）"""
    if len(args) !=1:
        raise InterpreterError("ffi_alloc_w(字符串)")
    text = str(args[0])
    buf = ctypes.create_unicode_buffer(text)
    byte_size = ctypes.sizeof(buf)
    ptr = ctypes.cast(buf, ctypes.c_void_p).value
    _ffi_owned_memory[ptr] = (buf, byte_size)
    return ptr

def hope_ffi_free(args):
    """ffi_free(ptr) 释放 ffi_alloc / ffi_alloc_a / ffi_alloc_w 创建的内存。禁止释放外部DLL返回指针！"""
    if len(args) != 1:
        raise InterpreterError("ffi_free(内存指针)")
    ptr = int(args[0])
    #支持传入偏移地址，自动查找原始基地址
    target_base = None
    for base_addr,(buf,alloc_size) in _ffi_owned_memory.items():
        if base_addr <= ptr < base_addr + alloc_size:
            target_base = base_addr
            break
    if target_base is not None:
        del _ffi_owned_memory[target_base]
    return 0

def hope_ffi_mem_read(args):
    """ffi_mem_read(ptr,size) 读取内存，返回原始字节字符串"""
    if len(args)!=2:
        raise InterpreterError("ffi_mem_read(指针,读取字节数)")
    ptr = int(args[0])
    size = int(args[1])
    if size <= 0:
        raise InterpreterError("读取长度>0")
    #区间校验
    ok = False
    for base_addr,(buf,alloc_size) in _ffi_owned_memory.items():
        end = base_addr + alloc_size
        if base_addr <= ptr and (ptr + size) <= end:
            ok = True
            break
    if not ok:
        raise InterpreterError("ffi_mem_read仅允许读取ffi_alloc分配的内存，或者读取越界")
    buf = (ctypes.c_ubyte * size).from_address(ptr)
    return bytes(buf)

def hope_ffi_mem_write(args):
    """ffi_mem_write(ptr, bytes_obj) 将二进制字节写入内存地址"""
    if len(args)!=2:
        raise InterpreterError("ffi_mem_write(指针,字节串)")
    ptr = int(args[0])
    raw = bytes(args[1])
    size = len(raw)
    #区间校验，支持偏移地址，检查不越界
    ok = False
    for base_addr,(buf,alloc_size) in _ffi_owned_memory.items():
        end = base_addr + alloc_size
        if base_addr <= ptr and (ptr + size) <= end:
            ok = True
            break
    if not ok:
        raise InterpreterError("ffi_mem_write仅允许写入ffi_alloc分配的内存，或者写入越界")
    dst = (ctypes.c_ubyte * size).from_address(ptr)
    for i,b in enumerate(raw):
        dst[i]=b
    return size

def hope_substr(args):
    if len(args)!=3:
        raise InterpreterError("substr(字符串,起始位置,长度)")
    s = str(args[0])
    start = int(args[1])
    length = int(args[2])
    return s[start:start+length]

def hope_concat(args):
    return "".join(str(x) for x in args)

def hope_ffi_bytes(args):
    """ffi_bytes(数字列表): hope脚本构造bytes字节对象"""
    num_list = args[0]
    data = bytes(int(x) for x in num_list)
    return data

def hope_ffi_u64_bytes(args):
    """ffi_u64_bytes(整数)：把uint64指针转为8字节小端bytes，用于结构体写入指针"""
    val = int(args[0])
    return val.to_bytes(8, byteorder="little")

def hope_ffi_add(args):
    a = int(args[0])
    b = int(args[1])
    return a + b

def hope_ffi_callback(args):
    """
    ffi_callback() 返回WNDPROC回调指针
    脚本回调约定：脚本函数签名 fn(hwnd,msg,wparam,lparam) 返回整数返回值
    """
    if len(args) !=1:
        raise InterpreterError("ffi_callback(脚本函数名)")
    script_func_name = str(args[0])

    def _wndproc(hwnd, msg, wparam, lparam):
        #调度到解释器内部执行脚本函数
        from main import run_user_function
        ret = run_user_function(script_func_name,[hwnd,msg,wparam,lparam])
        return int(ret)

    cb_wrapper = WNDPROC(_wndproc)
    _ffi_callback_store.append(cb_wrapper) #保存引用阻止GC回收
    ptr = ctypes.cast(cb_wrapper, ctypes.c_void_p).value
    return ptr


def hope_ffi_get_message(args):
    """ffi_get_message(msg_ptr,hwnd_filter,min_msg,max_msg) 返回BOOL"""
    if len(args)!=4:
        raise InterpreterError("ffi_get_message(msg_ptr,hwnd,min,max)")
    msg_ptr = int(args[0])
    hwnd = int(args[1])
    msgMin = int(args[2])
    msgMax = int(args[3])
    ret = ctypes.windll.user32.GetMessageW(ctypes.c_void_p(msg_ptr), ctypes.c_void_p(hwnd), msgMin, msgMax)
    return ret

def hope_ffi_translate_message(args):
    if len(args)!=1:
        raise InterpreterError("ffi_translate_message(msg_ptr)")
    msg_ptr = int(args[0])
    ctypes.windll.user32.TranslateMessage(ctypes.c_void_p(msg_ptr))
    return 0

def hope_ffi_dispatch_message(args):
    if len(args)!=1:
        raise InterpreterError("ffi_dispatch_message(msg_ptr)")
    msg_ptr = int(args[0])
    res = ctypes.windll.user32.DispatchMessageW(ctypes.c_void_p(msg_ptr))
    return res


HOPE_CTYPES = {
    "substr": ([],hope_substr),
    "concat": ([],hope_concat),
    "load": ([], hope_load),
    "ffi_set_restype": ([], hope_ffi_set_restype),
    "ffi_call": ([], hope_ffi_call),
    "free_lib": ([], hope_free_lib),
    "ffi_alloc": ([], hope_ffi_alloc),
    "ffi_alloc_a": ([], hope_ffi_alloc_a),
    "ffi_alloc_w": ([], hope_ffi_alloc_w),
    "ffi_free": ([], hope_ffi_free),
    "ffi_mem_read": ([], hope_ffi_mem_read),
    "ffi_mem_write": ([], hope_ffi_mem_write),
    "ffi_u64_bytes": ([], hope_ffi_u64_bytes),
    "ffi_add": ([], hope_ffi_add),
    "ffi_bytes": ([], hope_ffi_bytes),
    "ffi_callback": ([], hope_ffi_callback),
    "ffi_get_message": ([], hope_ffi_get_message),
    "ffi_translate_message": ([], hope_ffi_translate_message),
    "ffi_dispatch_message": ([], hope_ffi_dispatch_message),
}
