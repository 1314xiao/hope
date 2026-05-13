class LexerError(Exception):
    """词法分析异常"""
    pass

class ParserError(Exception):
    """语法分析异常"""
    pass

class InterpreterError(Exception):
    """解释执行异常"""
    pass