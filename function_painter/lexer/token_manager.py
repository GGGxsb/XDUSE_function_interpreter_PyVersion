from enum import Enum
from typing import Dict, Any, Optional, Callable, List
import math


class TokenTypeEnum(Enum):
    """Token类型枚举"""
    # 注释
    COMMENT = "COMMENT"
    
    # 保留字
    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    FOR = "FOR"
    FROM = "FROM"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"
    DEF = "DEF"
    LET = "LET"
    PARAM = "PARAM"
    SHOW = "SHOW"
    CLEAR = "CLEAR"
    WITH = "WITH"
    COLOR = "COLOR"
    
    # for语句固定参数
    T = "T"
    # 变量
    VARIABLE = "VARIABLE"
    
    # 分隔符
    SEMICO = "SEMICO"
    LBRACKET = "LBRACKET"  # [
    RBRACKET = "RBRACKET"  # ]
    LPAREN = "LPAREN"      # (
    RPAREN = "RPAREN"      # )
    COMMA = "COMMA"
    
    # 赋值
    ASSIGN = "ASSIGN"
    
    # 运算符
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    POWER = "POWER"
    
    # 函数名
    FUNC = "FUNC"
    # 常数（数值字面量、命名常量）
    CONSTID = "CONSTID"
    
    # 源程序结束
    NONTOKEN = "NONTOKEN"
    # 错误Token
    ERRTOKEN = "ERRTOKEN"


class Token:
    """Token类"""
    def __init__(self, token_type: TokenTypeEnum, lexeme: str, value: float = 0.0, func: Optional[Callable] = None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.value = value
        self.func = func
    
    def __str__(self):
        return f"Token(token_type={self.token_type}, lexeme='{self.lexeme}', value={self.value})"
    
    def __repr__(self):
        return self.__str__()


class TokenBuilder:
    """Token建造者"""
    def __init__(self):
        self.token_type: Optional[TokenTypeEnum] = None
        self.lexeme: Optional[str] = None
        self.value: Optional[float] = None
        self.func: Optional[Callable] = None
    
    def set_token_type(self, token_type: TokenTypeEnum):
        self.token_type = token_type
        return self
    
    def set_lexeme(self, lexeme: str):
        self.lexeme = lexeme
        return self
    
    def set_value(self, value: float):
        self.value = value
        return self
    
    def set_func(self, func: Callable):
        self.func = func
        return self
    
    def build(self) -> Token:
        if self.token_type is None or self.lexeme is None:
            raise ValueError("Token type and lexeme must be set")
        return Token(
            token_type=self.token_type,
            lexeme=self.lexeme,
            value=self.value or 0.0,
            func=self.func
        )


def generate_token_match_map() -> Dict[str, Token]:
    """生成Token匹配映射表"""
    print("调试-TokenMap: 开始生成Token匹配映射表")
    token_map = {}
    
    # 保留字
    reserved_words = {
        'origin': TokenTypeEnum.ORIGIN,
        'scale': TokenTypeEnum.SCALE,
        'rot': TokenTypeEnum.ROT,
        'is': TokenTypeEnum.IS,
        'for': TokenTypeEnum.FOR,
        'from': TokenTypeEnum.FROM,
        'to': TokenTypeEnum.TO,
        'step': TokenTypeEnum.STEP,
        'draw': TokenTypeEnum.DRAW,
        'def': TokenTypeEnum.DEF,
        'let': TokenTypeEnum.LET,
    # 将't'从特殊关键字中移除，使其作为普通变量处理
    # 't': TokenTypeEnum.T,
    'param': TokenTypeEnum.PARAM,
        'show': TokenTypeEnum.SHOW,
        'clear': TokenTypeEnum.CLEAR,
        'with': TokenTypeEnum.WITH,
        'color': TokenTypeEnum.COLOR
    }
    
    print(f"调试-TokenMap: 保留字列表: {reserved_words}")
    
    for word, token_type in reserved_words.items():
        lower_word = word.lower()
        print(f"调试-TokenMap: 添加关键字 '{lower_word}' 映射到 {token_type}")
        token_map[lower_word] = TokenBuilder()\
            .set_token_type(token_type)\
            .set_lexeme(word)\
            .build()
    
    print(f"调试-TokenMap: Token映射表生成完成，包含 {len(token_map)} 个关键字")
    
    # 分隔符和运算符
    special_tokens = {
        ';': (TokenTypeEnum.SEMICO, None),
        '[': (TokenTypeEnum.LBRACKET, None),
        ']': (TokenTypeEnum.RBRACKET, None),
        '(': (TokenTypeEnum.LPAREN, None),
        ')': (TokenTypeEnum.RPAREN, None),
        ',': (TokenTypeEnum.COMMA, None),
        '=': (TokenTypeEnum.ASSIGN, None),
        '+': (TokenTypeEnum.PLUS, None),
        '-': (TokenTypeEnum.MINUS, None),
        '*': (TokenTypeEnum.MUL, None),
        '/': (TokenTypeEnum.DIV, None),
        '**': (TokenTypeEnum.POWER, None)
    }
    
    for symbol, (token_type, _) in special_tokens.items():
        token_map[symbol] = TokenBuilder()\
            .set_token_type(token_type)\
            .set_lexeme(symbol)\
            .build()
    
    # 函数
    def sin_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("sin requires exactly 1 argument")
        return math.sin(args[0])
    
    def cos_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("cos requires exactly 1 argument")
        return math.cos(args[0])
    
    def tan_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("tan requires exactly 1 argument")
        return math.tan(args[0])
    
    def ln_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("ln requires exactly 1 argument")
        return math.log(args[0])
    
    def log_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("log requires exactly 1 argument")
        return math.log(args[0])
    
    def log10_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("log10 requires exactly 1 argument")
        return math.log10(args[0])
    
    def exp_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("exp requires exactly 1 argument")
        return math.exp(args[0])
    
    def sqrt_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("sqrt requires exactly 1 argument")
        return math.sqrt(args[0])
    
    def abs_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("abs requires exactly 1 argument")
        return abs(args[0])
    
    def asin_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("asin requires exactly 1 argument")
        return math.asin(args[0])
    
    def acos_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("acos requires exactly 1 argument")
        return math.acos(args[0])
    
    def atan_func(args: List[float]) -> float:
        if len(args) != 1:
            raise ValueError("atan requires exactly 1 argument")
        return math.atan(args[0])
    
    def max_func(args: List[float]) -> float:
        if len(args) < 2:
            raise ValueError("max requires at least 2 arguments")
        return max(args)
    
    def min_func(args: List[float]) -> float:
        if len(args) < 2:
            raise ValueError("min requires at least 2 arguments")
        return min(args)
    
    def aver_func(args: List[float]) -> float:
        if not args:
            raise ValueError("aver requires at least 1 argument")
        return sum(args) / len(args)
    
    functions = {
        'sin': sin_func,
        'cos': cos_func,
        'tan': tan_func,
        'asin': asin_func,
        'acos': acos_func,
        'atan': atan_func,
        'ln': ln_func,
        'log': log_func,
        'log10': log10_func,
        'exp': exp_func,
        'sqrt': sqrt_func,
        'abs': abs_func,
        'max': max_func,
        'min': min_func,
        'aver': aver_func
    }
    
    for func_name, func in functions.items():
        token_map[func_name.lower()] = TokenBuilder()\
            .set_token_type(TokenTypeEnum.FUNC)\
            .set_lexeme(func_name)\
            .set_func(func)\
            .build()
    
    return token_map


def generate_eof_token() -> Token:
    """生成EOF Token"""
    return Token(
        token_type=TokenTypeEnum.NONTOKEN,
        lexeme="EOF",
        value=0.0
    )


def generate_err_token(lexeme: str) -> Token:
    """生成错误Token"""
    return Token(
        token_type=TokenTypeEnum.ERRTOKEN,
        lexeme=lexeme,
        value=0.0
    )