import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from function_painter.interpreter import Interpreter
from function_painter.exception.exception import FunctionPainterException


def main():
    """程序主入口"""
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python -m function_painter.main <源文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        # 创建解释器并执行文件
        interpreter = Interpreter()
        interpreter.interpret_file(file_path)
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{file_path}'")
        sys.exit(1)
    except FunctionPainterException as e:
        print(f"解释错误: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"未预期的错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()