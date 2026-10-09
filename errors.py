#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2025/11/9 18:21

class LexerError(Exception):
    """词法分析异常"""
    pass

class ParserError(Exception):
    """语法分析异常"""
    pass

class InterpreterError(Exception):
    """解释执行异常"""
    pass
