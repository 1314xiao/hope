import re
from typing import Tuple
from errors import LexerError

# Token 类型：三元组 (类型, 值, 行号)
Token = Tuple[str, str | None, int]

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.token_specs = [
            ('MULTI_COMMENT', r'/\*[\s\S]*?\*/'),
            ('SINGLE_COMMENT', r'//.*'),
            ('KEYWORD', r'set|show|if|else|loop|func|return|import|input'),
            ('STRING', r'"(?:\\.|[^\\"])*"'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER', r'-?\d+(\.\d+)?'),
            ('ARITH_OP', r'[\+\-\*\/\%]'),
            ('COMP_OP', r'==|>=|<=|>|<'),
            ('EQUALS', r'='),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('COMMA', r','),
            ('WHITESPACE', r'\s+'),
        ]
        self.pattern = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs))

    def get_next_token(self) -> Token:
        while self.pos < len(self.code):
            match = self.pattern.match(self.code, self.pos)
            if not match:
                raise LexerError(f"词法错误[第{self.line}行]：位置{self.pos}存在无效字符 '{self.code[self.pos]}'")
            
            token_type = match.lastgroup
            token_value = match.group(token_type)
            line = self.line
            # 更新行号
            if '\n' in token_value:
                self.line += token_value.count('\n')
            
            self.pos = match.end()

            if token_type in ['SINGLE_COMMENT', 'MULTI_COMMENT', 'WHITESPACE']:
                continue
            if token_type == 'STRING':
                if not self.code[:self.pos].count('"') % 2 == 0:
                    raise LexerError(f"词法错误[第{self.line}行]：字符串未闭合，缺少右双引号")
                token_value = token_value.strip('"').replace(r'\"', '"')
            return (token_type, token_value, line)
        return ('EOF', None, self.line)