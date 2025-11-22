from typing import Optional


class FunctionPainterException(Exception):
    """函数绘图器异常基类"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        self.message = message
        self.line = line
        self.column = column
        
        if line is not None and column is not None:
            full_message = f"{message} (行 {line}, 列 {column})"
        else:
            full_message = message
        
        super().__init__(full_message)


class LexerError(FunctionPainterException):
    """词法分析错误"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(f"词法错误: {message}", line, column)


class ParserError(FunctionPainterException):
    """语法分析错误"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(f"语法错误: {message}", line, column)


class InterpreterError(FunctionPainterException):
    """解释执行错误"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(f"执行错误: {message}", line, column)


class SemanticError(InterpreterError):
    """语义错误"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(f"语义错误: {message}", line, column)


class RuntimeError(InterpreterError):
    """运行时错误"""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None):
        super().__init__(f"运行时错误: {message}", line, column)