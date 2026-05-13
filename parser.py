from typing import List, Tuple, Union
from lexer import Lexer, Token
from errors import ParserError

# AST 节点：普通节点为 (type, ...)，语句节点为 (type, line, ...)
ASTNode = Tuple[str, Union[int, str, List['ASTNode']]]

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Token = self.lexer.get_next_token()
        self.current_line = self.current_token[2]  # 当前 token 行号

    def _consume(self, expected_type: str) -> None:
        if self.current_token[0] == expected_type:
            self.current_token = self.lexer.get_next_token()
            self.current_line = self.current_token[2]
        else:
            raise ParserError(f"语法错误[第{self.current_line}行]：期望'{expected_type}'，实际得到'{self.current_token[0]}'（值：{self.current_token[1]}）")

    def _input_stmt(self) -> ASTNode:
        line = self.current_line
        keyword = self.current_token[1]
        if keyword != 'input':
            raise ParserError(f"语法错误[第{line}行]：期望input关键字，实际得到{keyword}")
        self._consume('KEYWORD')
        prompt = ""
        input_type = "str"
        if self.current_token[0] != 'LPAREN':
            raise ParserError(f"语法错误[第{line}行]：input后需跟(包裹参数")
        self._consume('LPAREN')
        if self.current_token[0] == 'STRING':
            prompt = self.current_token[1]
            self._consume('STRING')
            if self.current_token[0] == 'COMMA':
                self._consume('COMMA')
                if self.current_token[0] == 'IDENTIFIER' and self.current_token[1] in ['int', 'str', 'float']:
                    input_type = self.current_token[1]
                    self._consume('IDENTIFIER')
        if self.current_token[0] != 'RPAREN':
            raise ParserError(f"语法错误[第{line}行]：input参数缺少闭合)")
        self._consume('RPAREN')
        return ('INPUT_STMT', line, (prompt, input_type))

    def _stmt(self) -> ASTNode:
        line = self.current_line
        if self.current_token[0] == 'KEYWORD':
            keyword = self.current_token[1]
            if keyword == 'input':
                return self._input_stmt()
            elif keyword == 'import':
                return self._import_stmt()
            elif keyword == 'set':
                return self._set_stmt()
            elif keyword == 'show':
                return self._show_stmt()
            elif keyword == 'if':
                return self._if_stmt()
            elif keyword == 'loop':
                return self._loop_stmt()
            elif keyword == 'func':
                return self._func_def()
            elif keyword == 'return':
                return self._return_stmt()
        # 表达式语句
        expr = self._arith_expr()
        return ('EXPR_STMT', line, expr)

    def _factor(self) -> ASTNode:
        token = self.current_token
        if token[0] == 'KEYWORD' and token[1] == 'input':
            return self._input_stmt()
        if token[0] == 'NUMBER':
            self._consume('NUMBER')
            num_val = float(token[1]) if '.' in token[1] else int(token[1])
            return ('NUM', num_val)
        elif token[0] == 'IDENTIFIER':
            ident_name = token[1]
            self._consume('IDENTIFIER')
            if self.current_token[0] == 'LPAREN':
                self._consume('LPAREN')
                args = []
                if self.current_token[0] != 'RPAREN':
                    args.append(self._arith_expr())
                    while self.current_token[0] == 'COMMA':
                        self._consume('COMMA')
                        args.append(self._arith_expr())
                self._consume('RPAREN')
                return ('FUNC_CALL', ident_name, args)
            elif self.current_token[0] == 'LBRACKET':
                self._consume('LBRACKET')
                index_expr = self._arith_expr()
                self._consume('RBRACKET')
                return ('INDEXED_VAR', ident_name, index_expr)
            return ('VAR', ident_name)
        elif token[0] == 'STRING':
            self._consume('STRING')
            return ('STR', token[1])
        elif token[0] == 'LPAREN':
            self._consume('LPAREN')
            node = self._arith_expr()
            self._consume('RPAREN')
            return node
        elif token[0] == 'LBRACKET':
            self._consume('LBRACKET')
            elements = []
            if self.current_token[0] != 'RBRACKET':
                elements.append(self._arith_expr())
                while self.current_token[0] == 'COMMA':
                    self._consume('COMMA')
                    elements.append(self._arith_expr())
            self._consume('RBRACKET')
            return ('LIST', elements)
        else:
            raise ParserError(f"语法错误[第{self.current_line}行]：非法表达式元素'{token[1]}'")

    def _term(self) -> ASTNode:
        node = self._factor()
        while self.current_token[0] == 'ARITH_OP' and self.current_token[1] in ['*', '/', '%']:
            op_token = self.current_token
            self._consume('ARITH_OP')
            right = self._factor()
            node = ('ARITH_EXPR', op_token[1], node, right)
        return node

    def _arith_expr(self) -> ASTNode:
        node = self._term()
        while self.current_token[0] == 'ARITH_OP' and self.current_token[1] in ['+', '-']:
            op_token = self.current_token
            self._consume('ARITH_OP')
            right = self._term()
            node = ('ARITH_EXPR', op_token[1], node, right)
        return node

    def _cond_expr(self) -> ASTNode:
        left = self._arith_expr()
        if self.current_token[0] != 'COMP_OP':
            raise ParserError(f"语法错误[第{self.current_line}行]：条件语句缺少比较运算符（当前：{self.current_token[1]}）")
        comp_op = self.current_token
        self._consume('COMP_OP')
        right = self._arith_expr()
        return ('COND_EXPR', comp_op[1], left, right)

    def _import_stmt(self) -> ASTNode:
        line = self.current_line
        self._consume('KEYWORD')
        lib_name = self.current_token[1]
        self._consume('IDENTIFIER')
        return ('IMPORT_STMT', line, lib_name)

    def _stmt_block(self) -> ASTNode:
        self._consume('LBRACE')
        stmts = []
        while self.current_token[0] != 'RBRACE' and self.current_token[0] != 'EOF':
            stmts.append(self._stmt())
        self._consume('RBRACE')
        return ('STMT_BLOCK', stmts)

    def _func_def(self) -> ASTNode:
        line = self.current_line
        self._consume('KEYWORD')
        func_name = self.current_token[1]
        self._consume('IDENTIFIER')
        self._consume('LPAREN')
        params = []
        if self.current_token[0] == 'IDENTIFIER':
            params.append(self.current_token[1])
            self._consume('IDENTIFIER')
            while self.current_token[0] == 'COMMA':
                self._consume('COMMA')
                params.append(self.current_token[1])
                self._consume('IDENTIFIER')
        self._consume('RPAREN')
        func_body = self._stmt_block()
        return ('FUNC_DEF', line, func_name, params, func_body)

    def _return_stmt(self) -> ASTNode:
        line = self.current_line
        self._consume('KEYWORD')
        expr = self._arith_expr()
        return ('RETURN_STMT', line, expr)

    def _if_stmt(self) -> ASTNode:
        line = self.current_line
        self._consume('KEYWORD')
        if self.current_token[0] != 'LPAREN':
            raise ParserError(f"语法错误[第{line}行]：if后需跟(包裹条件")
        self._consume('LPAREN')
        cond = self._cond_expr()
        self._consume('RPAREN')
        if_block = self._stmt_block()
        else_block = None
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
            self._consume('KEYWORD')
            else_block = self._stmt_block()
        return ('IF_STMT', line, cond, if_block, else_block)

    def _loop_stmt(self) -> ASTNode:
        line = self.current_line
        self._consume('KEYWORD')
        if self.current_token[0] != 'LPAREN':
            raise ParserError(f"语法错误[第{line}行]：loop后需跟(包裹条件")
        self._consume('LPAREN')
        cond = self._cond_expr()
        self._consume('RPAREN')
        loop_block = self._stmt_block()
        return ('LOOP_STMT', line, cond, loop_block)

    def _show_stmt(self) -> ASTNode:
        line = self.current_line
        self._consume('KEYWORD')
        if self.current_token[0] != 'LPAREN':
            raise ParserError(f"语法错误[第{line}行]：show后需跟(包裹输出内容")
        self._consume('LPAREN')
        expr_list = []
        if self.current_token[0] != 'RPAREN':
            expr_list.append(self._arith_expr())
            while self.current_token[0] == 'COMMA':
                self._consume('COMMA')
                expr_list.append(self._arith_expr())
        if self.current_token[0] != 'RPAREN':
            raise ParserError(f"语法错误[第{line}行]：show参数缺少闭合)")
        self._consume('RPAREN')
        return ('SHOW_STMT', line, expr_list)

    def _set_stmt(self) -> ASTNode:
        line = self.current_line
        self._consume('KEYWORD')
        if self.current_token[0] != 'IDENTIFIER':
            raise ParserError(f"语法错误[第{line}行]：set后需跟变量名")
        var_name = self.current_token[1]
        self._consume('IDENTIFIER')
        if self.current_token[0] == 'LBRACKET':
            self._consume('LBRACKET')
            index_expr = self._arith_expr()
            self._consume('RBRACKET')
            self._consume('EQUALS')
            expr_node = self._arith_expr()
            return ('SET_IDX_STMT', line, var_name, index_expr, expr_node)
        else:
            self._consume('EQUALS')
            expr_node = self._arith_expr()
            return ('SET_STMT', line, var_name, expr_node)

    def parse(self) -> ASTNode:
        program = []
        while self.current_token[0] != 'EOF':
            program.append(self._stmt())
        return ('PROGRAM', program)