from typing import Optional, Dict
from ..lexer import Lexer, Token, TokenTypeEnum
from .expression import (
    Expression,
    ConstantExpression,
    VariableExpression,
    AddExpression,
    SubtractExpression,
    MultiplyExpression,
    DivideExpression,
    PowerExpression,
    NegateExpression,
    FunctionExpression
)


class Parser:
    """语法分析器"""
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token: Optional[Token] = self.lexer.fetch_token()
    
    def parse_program(self) -> list[dict]:
        """解析整个程序"""
        statements = []
        print(f"调试: 开始解析程序")
        
        # 检查初始token
        if not self.current_token:
            print(f"调试: 没有可用的token，重新获取")
            self.current_token = self.lexer.fetch_token()
        
        print(f"调试: 初始token: {self.current_token}")
        
        statement_count = 0
        
        while self.current_token and self.current_token.token_type != TokenTypeEnum.NONTOKEN:
            statement_count += 1
            print(f"调试: 解析第 {statement_count} 个语句，当前token: {self.current_token}")
            
            # 解析语句
            statement = self.parse_statement()
            
            if statement:
                print(f"调试: 第 {statement_count} 个语句解析成功: {statement}")
                print(f"调试: 语句类型: {statement.get('type')}")
                statements.append(statement)
            else:
                print(f"调试: 第 {statement_count} 个语句解析失败，跳过")
                # 确保总是有下一个token
                if not self.current_token:
                    break
        
        # 调试信息
        print(f"调试: 程序解析完成，共解析 {len(statements)} 个语句")
        for i, stmt in enumerate(statements):
            print(f"调试: 最终语句 {i+1} 类型: {stmt.get('type')}")
        
        return statements
    
    def parse_statement(self) -> Optional[dict]:
        """解析单个语句"""
        print(f"调试: 当前解析语句，token类型: {self.current_token.token_type if self.current_token else None}, lexeme: '{self.current_token.lexeme if self.current_token else None}'")
        if not self.current_token:
            return None
        
        # 解析参数声明
        if self.current_token.token_type == TokenTypeEnum.PARAM:
            return self.parse_param_statement()
        
        # 解析变量赋值
        elif self.current_token.token_type == TokenTypeEnum.VARIABLE:
            return self.parse_assignment_statement()
        
        # 解析函数定义
        elif self.current_token.token_type == TokenTypeEnum.FUNC:
            return self.parse_function_definition()
        
        # 解析绘图指令
        elif self.current_token.token_type == TokenTypeEnum.DRAW:
            return self.parse_draw_statement()
        
        # 解析显示指令
        elif self.current_token.token_type == TokenTypeEnum.SHOW:
            return self.parse_show_statement()
        
        # 解析清除指令
        elif self.current_token.token_type == TokenTypeEnum.CLEAR:
            return self.parse_clear_statement()
        
        # 跳过未知token
        self._eat_token()
        return None
    
    def parse_param_statement(self) -> dict:
        """解析参数声明，支持两种格式：
        1. param x from min_val to max_val step step_val
        2. param x [min_val, max_val, step_val]
        """
        print(f"调试: 解析param语句，当前token: {self.current_token}")
        self._eat_token()  # 吃掉PARAM
        
        # 确保是变量名
        if not self.current_token or self.current_token.token_type != TokenTypeEnum.VARIABLE:
            raise ValueError("语法错误: 参数声明缺少变量名")
        name = self.current_token.lexeme
        self._eat_token()  # 吃掉变量名
        
        min_val = -1.0
        max_val = 1.0
        step = 0.01
        
        # 检查是否是方括号格式
        if self.current_token and self.current_token.token_type == TokenTypeEnum.LBRACKET:
            print(f"调试: 检测到方括号格式")
            self._eat_token()  # 吃掉[
            
            # 解析最小值
            if self.current_token.token_type == TokenTypeEnum.MINUS:
                self._eat_token()  # 吃掉负号
                if not self.current_token or self.current_token.token_type != TokenTypeEnum.CONSTID:
                    raise ValueError("语法错误: 参数声明缺少最小值")
                min_val = -self.current_token.value
                self._eat_token()  # 吃掉数值
            elif self.current_token.token_type == TokenTypeEnum.CONSTID:
                min_val = self.current_token.value
                self._eat_token()  # 吃掉数值
            else:
                raise ValueError("语法错误: 参数声明缺少最小值")
            
            # 解析逗号
            if not self.current_token or self.current_token.token_type != TokenTypeEnum.COMMA:
                raise ValueError("语法错误: 参数声明缺少逗号分隔符")
            self._eat_token()  # 吃掉,
            
            # 解析最大值
            if self.current_token.token_type == TokenTypeEnum.MINUS:
                self._eat_token()  # 吃掉负号
                if not self.current_token or self.current_token.token_type != TokenTypeEnum.CONSTID:
                    raise ValueError("语法错误: 参数声明缺少最大值")
                max_val = -self.current_token.value
                self._eat_token()  # 吃掉数值
            elif self.current_token.token_type == TokenTypeEnum.CONSTID:
                max_val = self.current_token.value
                self._eat_token()  # 吃掉数值
            else:
                raise ValueError("语法错误: 参数声明缺少最大值")
            
            # 解析逗号
            if not self.current_token or self.current_token.token_type != TokenTypeEnum.COMMA:
                raise ValueError("语法错误: 参数声明缺少逗号分隔符")
            self._eat_token()  # 吃掉,
            
            # 解析步长
            if self.current_token.token_type == TokenTypeEnum.MINUS:
                self._eat_token()  # 吃掉负号
                if not self.current_token or self.current_token.token_type != TokenTypeEnum.CONSTID:
                    raise ValueError("语法错误: 参数声明缺少步长")
                step = -self.current_token.value
                self._eat_token()  # 吃掉数值
            elif self.current_token.token_type == TokenTypeEnum.CONSTID:
                step = self.current_token.value
                self._eat_token()  # 吃掉数值
            else:
                raise ValueError("语法错误: 参数声明缺少步长")
            
            # 解析右括号
            if not self.current_token or self.current_token.token_type != TokenTypeEnum.RBRACKET:
                raise ValueError("语法错误: 参数声明缺少右括号")
            self._eat_token()  # 吃掉]
        else:
            # 传统格式：FROM ... TO ... STEP
            if not self.current_token or self.current_token.token_type != TokenTypeEnum.FROM:
                raise ValueError("语法错误: 参数声明缺少FROM关键字")
            self._eat_token()
            
            # 解析起始值
            if self.current_token.token_type == TokenTypeEnum.MINUS:
                self._eat_token()
                if not self.current_token or self.current_token.token_type != TokenTypeEnum.CONSTID:
                    raise ValueError("语法错误: 参数声明缺少最小值")
                min_val = -self.current_token.value
                self._eat_token()
            elif self.current_token.token_type == TokenTypeEnum.CONSTID:
                min_val = self.current_token.value
                self._eat_token()
            else:
                raise ValueError("语法错误: 参数声明缺少最小值")
            
            if not self.current_token or self.current_token.token_type != TokenTypeEnum.TO:
                raise ValueError("语法错误: 参数声明缺少TO关键字")
            self._eat_token()
            
            # 解析结束值
            if self.current_token.token_type == TokenTypeEnum.MINUS:
                self._eat_token()
                if not self.current_token or self.current_token.token_type != TokenTypeEnum.CONSTID:
                    raise ValueError("语法错误: 参数声明缺少最大值")
                max_val = -self.current_token.value
                self._eat_token()
            elif self.current_token.token_type == TokenTypeEnum.CONSTID:
                max_val = self.current_token.value
                self._eat_token()
            else:
                raise ValueError("语法错误: 参数声明缺少最大值")
            
            if not self.current_token or self.current_token.token_type != TokenTypeEnum.STEP:
                raise ValueError("语法错误: 参数声明缺少STEP关键字")
            self._eat_token()
            
            # 解析步长
            if self.current_token.token_type == TokenTypeEnum.MINUS:
                self._eat_token()
                if not self.current_token or self.current_token.token_type != TokenTypeEnum.CONSTID:
                    raise ValueError("语法错误: 参数声明缺少步长")
                step = -self.current_token.value
                self._eat_token()
            elif self.current_token.token_type == TokenTypeEnum.CONSTID:
                step = self.current_token.value
                self._eat_token()
            else:
                raise ValueError("语法错误: 参数声明缺少步长")
        
        print(f"调试: param语句解析完成，参数: {name} [{min_val}, {max_val}, {step}]")
        return {
            'type': 'param',
            'name': name,
            'min': min_val,
            'max': max_val,
            'step': step
        }

    
    def parse_assignment_statement(self) -> dict:
        """解析赋值语句"""
        name = self.current_token.lexeme
        self._eat_token()  # 吃掉变量名
        
        if self.current_token and self.current_token.token_type == TokenTypeEnum.ASSIGN:
            self._eat_token()  # 吃掉=
            expr = self.parse_expression()
            
            return {
                'type': 'assign',
                'name': name,
                'expression': expr
            }
        
        # 不是有效的赋值语句，返回None而不是错误类型
        print(f"调试: 无效的赋值语句，缺少等号")
        return None
    
    def parse_function_definition(self) -> dict:
        """解析函数定义"""
        self._eat_token()  # 吃掉FUNC
        
        if self.current_token and self.current_token.token_type == TokenTypeEnum.VARIABLE:
            name = self.current_token.lexeme
            self._eat_token()  # 吃掉函数名
            
            if self.current_token and self.current_token.token_type == TokenTypeEnum.ASSIGN:
                self._eat_token()  # 吃掉=
                expr = self.parse_expression()
                
                return {
                    'type': 'function',
                    'name': name,
                    'expression': expr
                }
        
        # 不是有效的函数定义，返回None而不是错误类型
        print(f"调试: 无效的函数定义")
        return None
    
    def parse_draw_statement(self) -> dict:
        """解析绘图语句，支持单一表达式或参数方程格式"""
        self._eat_token()  # 吃掉DRAW
        
        # 解析第一个表达式
        expr1 = self.parse_expression()
        
        # 检查是否有逗号，判断是否为参数方程格式
        is_parametric = False
        expr2 = None
        if self.current_token and self.current_token.token_type == TokenTypeEnum.COMMA:
            is_parametric = True
            self._eat_token()  # 吃掉逗号
            expr2 = self.parse_expression()  # 解析第二个表达式
        
        # 检查是否有颜色
        color = None
        if self.current_token and self.current_token.token_type == TokenTypeEnum.WITH:
            self._eat_token()  # 吃掉WITH
            if self.current_token and self.current_token.token_type == TokenTypeEnum.COLOR:
                color = self.current_token.lexeme
                self._eat_token()  # 吃掉颜色
        
        result = {
            'type': 'draw',
            'color': color
        }
        
        # 根据是否为参数方程格式设置不同的字段
        if is_parametric:
            result['x_expression'] = expr1
            result['y_expression'] = expr2
        else:
            result['expression'] = expr1
        
        return result
    
    def parse_show_statement(self) -> dict:
        """解析显示语句"""
        self._eat_token()  # 吃掉SHOW
        return {'type': 'show'}
    
    def parse_clear_statement(self) -> dict:
        """解析清除语句"""
        self._eat_token()  # 吃掉CLEAR
        return {'type': 'clear'}
    
    def parse_expression(self) -> Expression:
        """解析表达式"""
        return self._parse_equality()
    
    def _parse_equality(self) -> Expression:
        """解析相等性表达式"""
        expr = self._parse_addition()
        
        while self.current_token and self.current_token.token_type in [TokenTypeEnum.ASSIGN]: # 暂时只支持ASSIGN，NEQ可能也需要添加
            token = self.current_token
            self._eat_token()  # 吃掉比较运算符
            
            right = self._parse_addition()
            # 暂时不支持比较操作，简单地返回表达式的一部分
            # 后续可以扩展支持比较操作
        
        return expr
    
    def _parse_addition(self) -> Expression:
        """解析加法和减法"""
        expr = self._parse_multiplication()
        
        while self.current_token and self.current_token.token_type in [TokenTypeEnum.PLUS, TokenTypeEnum.MINUS]:
            token = self.current_token
            self._eat_token()  # 吃掉+或-
            
            right = self._parse_multiplication()
            
            if token.token_type == TokenTypeEnum.PLUS:
                expr = AddExpression(expr, right)
            else:
                expr = SubtractExpression(expr, right)
        
        return expr
    
    def _parse_multiplication(self) -> Expression:
        """解析乘法和除法"""
        expr = self._parse_power()
        
        while self.current_token and self.current_token.token_type in [TokenTypeEnum.MUL, TokenTypeEnum.DIV]:
            token = self.current_token
            self._eat_token()  # 吃掉*或/
            
            right = self._parse_power()
            
            if token.token_type == TokenTypeEnum.MUL:
                expr = MultiplyExpression(expr, right)
            else:
                expr = DivideExpression(expr, right)
        
        return expr
    
    def _parse_power(self) -> Expression:
        """解析幂运算"""
        expr = self._parse_unary()
        
        while self.current_token and self.current_token.token_type == TokenTypeEnum.POWER:
            self._eat_token()  # 吃掉**
            right = self._parse_unary()
            expr = PowerExpression(expr, right)
        
        return expr
    
    def _parse_unary(self) -> Expression:
        """解析一元运算符"""
        if self.current_token and self.current_token.token_type == TokenTypeEnum.MINUS:
            self._eat_token()  # 吃掉-
            return NegateExpression(self._parse_unary())
        
        return self._parse_primary()
    
    def _parse_primary(self) -> Expression:
        """解析基本表达式"""
        if not self.current_token:
            raise ValueError("语法错误: 意外的文件结束")
        
        token = self.current_token
        
        # 常量
        if token.token_type == TokenTypeEnum.CONSTID:
            self._eat_token()  # 吃掉常量
            return ConstantExpression(token.value)
        
        # 变量或函数名
        elif token.token_type in (TokenTypeEnum.VARIABLE, TokenTypeEnum.FUNC):
            func_name = token.lexeme
            self._eat_token()  # 吃掉函数名或变量名
            
            # 检查是否是函数调用
            if self.current_token and self.current_token.token_type == TokenTypeEnum.LPAREN:
                self._eat_token()  # 吃掉(
                
                # 解析参数表达式
                arg_expr = self.parse_expression()
                
                # 吃掉右括号
                if self.current_token and self.current_token.token_type == TokenTypeEnum.RPAREN:
                    self._eat_token()
                else:
                    raise ValueError("语法错误: 缺少右括号")
                
                return FunctionExpression(func_name, arg_expr)
            
            # 否则是普通变量
            return VariableExpression(func_name)
        
        # 括号表达式
        elif token.token_type == TokenTypeEnum.LPAREN:
            self._eat_token()  # 吃掉(
            expr = self.parse_expression()
            
            # 吃掉右括号
            if self.current_token and self.current_token.token_type == TokenTypeEnum.RPAREN:
                self._eat_token()
            else:
                raise ValueError("语法错误: 缺少右括号")
        
            return expr
        
        raise ValueError(f"语法错误: 意外的token {token.lexeme}")
    
    def _eat_token(self):
        """消费当前token"""
        self.current_token = self.lexer.fetch_token()
    
    def _expect_token(self, token_type: TokenTypeEnum):
        """期望当前token是指定类型"""
        if not self.current_token or self.current_token.token_type != token_type:
            raise ValueError(f"语法错误: 期望 {token_type}，但得到 {self.current_token.token_type if self.current_token else None}")