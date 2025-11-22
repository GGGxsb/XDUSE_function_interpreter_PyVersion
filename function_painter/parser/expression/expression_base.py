from abc import ABC, abstractmethod
from typing import Any, Optional


class Expression(ABC):
    """表达式基类"""
    @abstractmethod
    def evaluate(self, variables: dict[str, float]) -> float:
        """计算表达式的值"""
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """返回表达式的字符串表示"""
        pass


class BinaryExpression(Expression):
    """二元表达式基类"""
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    @abstractmethod
    def evaluate(self, variables: dict[str, float]) -> float:
        pass


class UnaryExpression(Expression):
    """一元表达式基类"""
    def __init__(self, operand: Expression):
        self.operand = operand
    
    @abstractmethod
    def evaluate(self, variables: dict[str, float]) -> float:
        pass