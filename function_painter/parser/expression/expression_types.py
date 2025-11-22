from typing import Dict, Optional
import math
from .expression_base import Expression, BinaryExpression, UnaryExpression


class ConstantExpression(Expression):
    """常量表达式"""
    def __init__(self, value: float):
        self.value = value
    
    def evaluate(self, variables: dict[str, float]) -> float:
        return self.value
    
    def __str__(self) -> str:
        return str(self.value)


class VariableExpression(Expression):
    """变量表达式"""
    def __init__(self, name: str):
        self.name = name
    
    def evaluate(self, variables: dict[str, float]) -> float:
        if self.name not in variables:
            raise ValueError(f"变量 '{self.name}' 未定义")
        return variables[self.name]
    
    def __str__(self) -> str:
        return self.name


class AddExpression(BinaryExpression):
    """加法表达式"""
    def evaluate(self, variables: dict[str, float]) -> float:
        return self.left.evaluate(variables) + self.right.evaluate(variables)
    
    def __str__(self) -> str:
        return f"({self.left} + {self.right})"


class SubtractExpression(BinaryExpression):
    """减法表达式"""
    def evaluate(self, variables: dict[str, float]) -> float:
        return self.left.evaluate(variables) - self.right.evaluate(variables)
    
    def __str__(self) -> str:
        return f"({self.left} - {self.right})"


class MultiplyExpression(BinaryExpression):
    """乘法表达式"""
    def evaluate(self, variables: dict[str, float]) -> float:
        return self.left.evaluate(variables) * self.right.evaluate(variables)
    
    def __str__(self) -> str:
        return f"({self.left} * {self.right})"


class DivideExpression(BinaryExpression):
    """除法表达式"""
    def evaluate(self, variables: dict[str, float]) -> float:
        divisor = self.right.evaluate(variables)
        if divisor == 0:
            raise ZeroDivisionError("除数不能为零")
        return self.left.evaluate(variables) / divisor
    
    def __str__(self) -> str:
        return f"({self.left} / {self.right})"


class PowerExpression(BinaryExpression):
    """幂运算表达式"""
    def evaluate(self, variables: dict[str, float]) -> float:
        return math.pow(self.left.evaluate(variables), self.right.evaluate(variables))
    
    def __str__(self) -> str:
        return f"({self.left} ** {self.right})"


class NegateExpression(UnaryExpression):
    """负号表达式"""
    def evaluate(self, variables: dict[str, float]) -> float:
        return -self.operand.evaluate(variables)
    
    def __str__(self) -> str:
        return f"-({self.operand})"


class FunctionExpression(Expression):
    """函数表达式"""
    def __init__(self, name: str, arg: Expression):
        self.name = name
        self.arg = arg
    
    def evaluate(self, variables: dict[str, float]) -> float:
        arg_value = self.arg.evaluate(variables)
        
        # 根据函数名调用对应的数学函数
        if self.name == "sin":
            return math.sin(arg_value)
        elif self.name == "cos":
            return math.cos(arg_value)
        elif self.name == "tan":
            return math.tan(arg_value)
        elif self.name == "asin":
            return math.asin(arg_value)
        elif self.name == "acos":
            return math.acos(arg_value)
        elif self.name == "atan":
            return math.atan(arg_value)
        elif self.name == "sqrt":
            return math.sqrt(arg_value)
        elif self.name == "exp":
            return math.exp(arg_value)
        elif self.name == "log":
            return math.log(arg_value)
        elif self.name == "log10":
            return math.log10(arg_value)
        elif self.name == "abs":
            return abs(arg_value)
        else:
            raise ValueError(f"未知函数名: {self.name}")
    
    def __str__(self) -> str:
        return f"{self.name}({self.arg})"