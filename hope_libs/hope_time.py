import time
from errors import InterpreterError

# time()：返回当前时间戳
def time_func(args):
    if len(args) != 0:
        raise InterpreterError("time函数不需要参数")
    return time.time()

# sleep(seconds)：让程序暂停指定秒数
def sleep_func(args):
    if len(args) != 1:
        raise InterpreterError("sleep函数需要1个参数：sleep(秒数)")
    sec = args[0]
    if not isinstance(sec, (int, float)):
        raise InterpreterError("sleep函数的参数必须是数字")
    if sec < 0:
        raise InterpreterError("sleep函数的参数不能是负数")
    time.sleep(sec)
    return "暂停完成"

# localtime()：返回当前本地时间
def localtime_func(args):
    if len(args) != 0:
        raise InterpreterError("localtime函数不需要参数")
    t = time.localtime()
    return f"{t.tm_year}年{t.tm_mon}月{t.tm_mday}日 {t.tm_hour}:{t.tm_min}:{t.tm_sec}"

#strftime(format_str)：按照指定格式返回当前时间
# 支持的格式占位符：
# %Y：年，%m：月，%d：日，%H：时（24小时制），%M：分，%S：秒，%A：星期全称，%B：月份全称
def strftime_func(args):
     if len(args) != 1:
         raise InterpreterError("strftime函数需要1个参数：strftime(格式字符串)")
     format_str = args[0]
     if not isinstance(format_str, str):
         raise InterpreterError("strftime函数的参数必须是字符串")
     try:
         return time.strftime(format_str, time.localtime())
     except Exception as e:
         raise InterpreterError(f"时间格式错误：{str(e)}")

# hour()：返回当前小时（24小时制）
def hour_func(args):
    if len(args) != 0:
        raise InterpreterError("hour函数不需要参数")
    return time.localtime().tm_hour

# minute()：返回当前分钟
def minute_func(args):
    if len(args) != 0:
        raise InterpreterError("minute函数不需要参数")
    return time.localtime().tm_min

# second()：返回当前秒
def second_func(args):
    if len(args) != 0:
        raise InterpreterError("second函数不需要参数")
    return time.localtime().tm_sec


TIME_FUNCTIONS = {
    "time": ([], time_func),
    "sleep": (["seconds"], sleep_func),
    "localtime": ([], localtime_func),
    "strftime": (["format"], strftime_func),
    "hour": ([], hour_func),
    "minute": ([], minute_func),
    "second": ([], second_func)
}
