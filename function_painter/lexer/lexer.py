from typing import Optional, Dict
from .token_manager import Token, TokenTypeEnum, generate_token_match_map, generate_eof_token, generate_err_token
from .text_reader import TextReader


class Lexer:
    """词法分析器，支持从文件或代码字符串读取"""
    def __init__(self, source: str, is_string: bool = False):
        self.text_reader = TextReader(source, is_string)
        self.curr_char: Optional[str] = self.text_reader.eat_char()
        self.token_match_map: Dict[str, Token] = generate_token_match_map()
    
    def fetch_token(self) -> Token:
        """获取下一个token"""
        print(f"调试-Lexer: 开始获取下一个token，当前字符: '{self.curr_char}'")
        self._skip_whitespace()
        
        if self.curr_char is None:
            print(f"调试-Lexer: 到达文件结束，返回EOF token")
            return generate_eof_token()
        
        # 检查是否是注释
        if self.curr_char == '/':
            print(f"调试-Lexer: 检测到可能的注释")
            # 由于_peek_char可能有问题，我们直接使用text_reader.peek_char()
            next_char = self.text_reader.peek_char()
            if next_char == '/':
                print(f"调试-Lexer: 确认是注释，跳过")
                self._skip_comment()
                return self.fetch_token()  # 递归获取下一个token
        
        # 根据开头字符，分为三种情况进行拼接
        token_result = None
        if self.curr_char.isdigit() or self.curr_char == '.':
            # 1. 数字开头或小数点开头。必须是数字字面值
            print(f"调试-Lexer: 收集数字token")
            token_result = self._collect_digit_token()
        elif self.curr_char.isalpha():
            # 2. 字母开头。保留字、函数名、参数、变量、常数
            print(f"调试-Lexer: 收集单词token")
            token_result = self._collect_word_token()
        else:
            # 3. 运算符、分隔符
            print(f"调试-Lexer: 收集特殊token")
            token_result = self._collect_special_token()
        
        print(f"调试-Lexer: 获取到token: {token_result.token_type}, lexeme: '{token_result.lexeme}'")
        return token_result
    
    def get_char_position(self) -> tuple[int, int]:
        """获取当前字符位置"""
        return self.text_reader.get_char_position()
    
    def _skip_whitespace(self):
        """跳过空白字符"""
        while self.curr_char is not None and self.curr_char.isspace():
            self._read_new_char()
    
    def _skip_comment(self):
        """跳过注释"""
        while self.curr_char is not None and self.curr_char != '\n':
            self._read_new_char()
        self._read_new_char()  # 跳过换行符
    
    def _collect_digit_token(self) -> Token:
        """收集数字token"""
        lexeme = []
        has_dot = False
        
        while self.curr_char is not None and (self.curr_char.isdigit() or self.curr_char == '.'):
            if self.curr_char == '.':
                if has_dot:
                    # 已经有小数点了，结束收集
                    break
                has_dot = True
            lexeme.append(self.curr_char)
            self._read_new_char()
        
        lexeme_str = ''.join(lexeme)
        
        # 检查是否是有效的数字
        try:
            value = float(lexeme_str)
            return Token(
                token_type=TokenTypeEnum.CONSTID,
                lexeme=lexeme_str,
                value=value
            )
        except ValueError:
            return generate_err_token(lexeme_str)
    
    def _collect_word_token(self) -> Token:
        """收集单词token"""
        print(f"调试-Lexer-单词收集: 开始收集单词token，当前字符: '{self.curr_char}'")
        lexeme = []
        
        while self.curr_char is not None and (self.curr_char.isalnum() or self.curr_char == '_'):
            print(f"调试-Lexer-单词收集: 添加字符 '{self.curr_char}' 到lexeme")
            lexeme.append(self.curr_char.lower())  # 不区分大小写
            self._read_new_char()
        
        lexeme_str = ''.join(lexeme)
        print(f"调试-Lexer-单词收集: 收集完成，lexeme_str = '{lexeme_str}'")
        
        # 打印token_match_map中的关键字，用于调试
        print(f"调试-Lexer-单词收集: token_match_map中包含以下关键字: {list(self.token_match_map.keys())}")
        
        # 检查是否在保留字或函数映射表中
        if lexeme_str in self.token_match_map:
            print(f"调试-Lexer-单词收集: '{lexeme_str}' 在token_match_map中，返回对应的token")
            return self.token_match_map[lexeme_str]
        else:
            print(f"调试-Lexer-单词收集: '{lexeme_str}' 不在token_match_map中，返回VARIABLE类型token")
            # 否则视为变量
            return Token(
                token_type=TokenTypeEnum.VARIABLE,
                lexeme=lexeme_str,
                value=0.0
            )
    
    def _collect_special_token(self) -> Token:
        """收集特殊字符token"""
        # 单符号处理
        lexeme = self.curr_char
        
        # 检查是否是双符号（如**）
        if lexeme == '*':
            # 先读取下一个字符检查是否是*
            next_char = self.text_reader.peek_char()
            print(f"调试-Lexer-特殊字符: 检查是否是双符号，当前字符: '{lexeme}', 下一个字符: '{next_char}'")
            if next_char == '*':
                # 确认是**，读取两个字符
                self._read_new_char()  # 读取第一个*
                self._read_new_char()  # 读取第二个*
                print(f"调试-Lexer-特殊字符: 成功收集双符号 **")
                return self.token_match_map['**']
        
        # 对于其他字符，直接读取当前字符
        self._read_new_char()
        print(f"调试-Lexer-特殊字符: 收集单符号 '{lexeme}', 当前字符变为: '{self.curr_char}'")
        
        if lexeme in self.token_match_map:
            return self.token_match_map[lexeme]
        else:
            return generate_err_token(lexeme)
    
    def _read_new_char(self):
        """读取新字符"""
        self.curr_char = self.text_reader.eat_char()
    
    def _peek_char(self) -> Optional[str]:
        """预览下一个字符，但不移动指针
        注意：这个方法在当前实现中可能不完美，但我们已经修改了_collect_special_token
        不再直接依赖它来进行双符号检测。
        """
        # 由于TextReader不支持真正的回退，这里简单返回None
        # 我们已经修改了代码不再依赖这个方法进行关键操作
        return None
    
    def close(self):
        """关闭词法分析器"""
        self.text_reader.close()