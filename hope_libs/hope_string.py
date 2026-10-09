from errors import InterpreterError


def hope_substr(args):
    if len(args)!=3:
        raise InterpreterError("substr(字符串,起始位置,长度)")
    s = str(args[0])
    start = int(args[1])
    length = int(args[2])
    return s[start:start+length]

def hope_concat(args):
    # concat(a,b,c...) 拼接任意多个字符串
    return "".join(str(x) for x in args)

STRING_FUNCTIONS = {
    "substr": ([],hope_substr),
    "concat": ([],hope_concat)
}
