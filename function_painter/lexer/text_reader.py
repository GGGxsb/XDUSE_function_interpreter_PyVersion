from typing import Optional, Union, IO


class TextReader:
    """简化的文本读取器，支持从文件或字符串读取"""
    def __init__(self, source: Union[str, IO], is_string: bool = False):
        self.buffer = []  # 使用一个字符缓冲区
        self.line_number = 1
        self.column_number = 0
        self.file = None
        
        if is_string:
            # 从字符串读取，将整个字符串转换为字符列表
            self.buffer = list(source)
        else:
            # 从文件读取，一次性读取所有内容
            self.file = open(source, 'r')
            content = self.file.read()
            self.buffer = list(content)
            self.file.close()  # 立即关闭文件，避免资源泄漏
    
    def eat_char(self) -> Optional[str]:
        """读取下一个字符并消耗它"""
        if not self.buffer:
            return None
        
        char = self.buffer.pop(0)
        self.column_number += 1
        
        # 处理换行
        if char == '\n':
            self.line_number += 1
            self.column_number = 0
        
        return char
    
    def peek_char(self) -> Optional[str]:
        """预览下一个字符，但不消耗它"""
        if not self.buffer:
            return None
        return self.buffer[0]
    
    def get_char_position(self) -> tuple[int, int]:
        """获取当前字符位置"""
        return (self.line_number, self.column_number)
    
    def close(self):
        """关闭文件"""
        # 由于我们在初始化时就已经读取了所有内容并关闭了文件，这里不需要做任何事情
        pass