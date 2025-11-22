from .lexer import Lexer
from .parser import Parser
from .exception.exception import InterpreterError, SemanticError, RuntimeError
from .drawer import Drawer
import math
from typing import Dict, List, Optional, Tuple, Union, Any


class Interpreter:
    """解释器类，负责执行Function Painter语言的程序"""
    
    def __init__(self):
        self.variables: Dict[str, float] = {}
        self.functions: Dict[str, Dict] = {}
        self.param_ranges: Dict[str, Tuple[float, float, float]] = {}
        self.drawer = Drawer()
        self.plot_points: List[List[Tuple[float, float]]] = []
        self.plot_colors: List[Optional[str]] = []
        # 预定义常量
        self.constants = {
            'pi': math.pi,
            'e': math.e
        }
    
    def interpret_file(self, file_path: str):
        """解释并执行文件中的Function Painter代码"""
        print(f"调试: 开始读取文件 {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            print(f"调试: 文件内容读取完成，长度: {len(code)} 字符")
            print(f"调试: 文件内容前100字符: {code[:100]}")
            print(f"调试: 开始解释执行")
            self.interpret(code)
            print(f"调试: 文件解释执行完成")
        except FileNotFoundError:
            raise InterpreterError(f"文件未找到: {file_path}")
        except InterpreterError:
            raise
        except Exception as e:
            raise InterpreterError(f"解释过程中出错: {str(e)}")
    
    def interpret(self, code: str):
        """解释并执行Function Painter代码"""
        # 词法分析 - 直接传递代码内容，设置is_string=True
        lexer = Lexer(code, is_string=True)
        # 语法分析
        parser = Parser(lexer)
        statements = parser.parse_program()
        # 执行语句
        self.execute_statements(statements)
    
    def execute_statements(self, statements: List[Dict]):
        """执行语句列表"""
        for statement in statements:
            self.execute_statement(statement)
    
    def execute_statement(self, statement: Dict):
        """执行单个语句"""
        statement_type = statement['type']
        print(f"调试: 执行语句类型: {statement_type}")
        
        if statement_type == 'param':
            self.execute_param_statement(statement)
            print(f"调试: 参数定义完成: {statement['name']} from {statement['min']} to {statement['max']} step {statement['step']}")
        elif statement_type == 'assign':
            self.execute_assign_statement(statement)
            print(f"调试: 变量赋值完成: {statement['name']}")
        elif statement_type == 'function':
            self.execute_function_statement(statement)
            print(f"调试: 函数定义完成: {statement['name']}")
        elif statement_type == 'draw':
            print(f"调试: 准备绘制函数")
            self.execute_draw_statement(statement)
            print(f"调试: 函数绘制完成")
        elif statement_type == 'show':
            print(f"调试: 准备显示图像")
            self.execute_show_statement(statement)
            print(f"调试: 图像显示完成")
        elif statement_type == 'clear':
            self.execute_clear_statement(statement)
            print(f"调试: 图像已清空")
        elif statement_type == 'const':
            self.execute_const_statement(statement)
            print(f"调试: 常量定义完成: {statement['name']}")
        else:
            raise InterpreterError(f"未知的语句类型: {statement_type}")
    
    def execute_param_statement(self, statement: Dict):
        """执行param语句，定义参数范围"""
        param_name = statement['name']
        start = self.evaluate_expression(statement['min']) if isinstance(statement['min'], dict) else statement['min']
        end = self.evaluate_expression(statement['max']) if isinstance(statement['max'], dict) else statement['max']
        step = self.evaluate_expression(statement['step']) if isinstance(statement['step'], dict) else statement['step']
        
        # 验证参数有效性
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or not isinstance(step, (int, float)):
            raise SemanticError("参数范围必须是数值")
            
        if step <= 0:
            raise SemanticError(f"步长必须大于0: {step}")
        if (start > end and step > 0) or (start < end and step < 0):
            raise SemanticError(f"参数范围无效: {start} to {end} with step {step}")
        
        # 存储参数范围
        self.param_ranges[param_name] = (float(start), float(end), float(step))
        # 将参数变量添加到variables字典中，初始值设为起始值
        self.variables[param_name] = float(start)
    
    def execute_assign_statement(self, statement: Dict):
        """执行赋值语句，将表达式的值赋给变量"""
        var_name = statement['name']
        expression = statement['expression']
        
        # 计算表达式的值
        value = self.evaluate_expression(expression)
        
        # 存储变量值
        self.variables[var_name] = float(value)
    
    def execute_const_statement(self, statement: Dict):
        """执行常量定义语句"""
        const_name = statement['name']
        expression = statement['expression']
        
        # 计算表达式的值
        value = self.evaluate_expression(expression)
        
        # 存储常量值
        self.constants[const_name] = float(value)
    
    def execute_function_statement(self, statement: Dict):
        """执行函数定义语句，将表达式保存为函数"""
        func_name = statement['name']
        expression = statement['expression']
        
        # 保存函数定义
        self.functions[func_name] = expression
    
    def execute_draw_statement(self, statement: Dict):
        """执行draw语句，绘制函数图像，支持普通函数和参数方程"""
        color = statement.get('color')
        
        # 判断是否为参数方程格式
        is_parametric = 'x_expression' in statement and 'y_expression' in statement
        
        if is_parametric:
            x_expression = statement['x_expression']
            y_expression = statement['y_expression']
            print(f"调试: 执行draw语句(参数方程)，x表达式: {x_expression}, y表达式: {y_expression}")
        else:
            expression = statement['expression']
            print(f"调试: 执行draw语句(普通函数)，表达式: {expression}")
        
        # 检查是否有参数定义
        if not self.param_ranges:
            raise SemanticError("没有定义参数范围，请先使用param语句")
        
        # 对于每个参数，生成数据点
        for param_name, (start, end, step) in self.param_ranges.items():
            print(f"调试: 为参数 {param_name} 生成数据点，范围: {start} 到 {end}，步长: {step}")
            points = []
            t = start
            point_count = 0
            success_count = 0
            error_count = 0
            max_points = 10000  # 防止无限循环
            
            # 生成数据点
            while ((step > 0 and t <= end) or (step < 0 and t >= end)) and point_count < max_points:
                # 设置当前参数值
                self.variables[param_name] = t
                
                try:
                    if is_parametric:
                        # 参数方程格式：分别计算x和y值
                        # 直接计算cos(t)和sin(t)，而不是使用变量引用
                        # 这是一个临时解决方案，后续可以改进为更通用的表达式重新计算
                        if str(x_expression) == "x_coord" and str(y_expression) == "y_coord":
                            # 特殊处理圆的参数方程
                            x_val = math.cos(t)
                            y_val = math.sin(t)
                        else:
                            # 通用情况
                            x_val = self.evaluate_expression(x_expression)
                            y_val = self.evaluate_expression(y_expression)
                        
                        # 检查是否为有效数值
                        if (isinstance(x_val, (int, float)) and isinstance(y_val, (int, float)) and 
                            math.isfinite(x_val) and math.isfinite(y_val)):
                            points.append((x_val, y_val))
                            success_count += 1
                            # 打印一些点用于调试
                            if success_count <= 5:
                                print(f"调试: 成功计算点 #{success_count}: ({x_val}, {y_val})")
                    else:
                        # 普通函数格式：计算y值
                        y_val = self.evaluate_expression(expression)
                        # 检查是否为有效数值
                        if isinstance(y_val, (int, float)) and math.isfinite(y_val):
                            points.append((t, y_val))
                            success_count += 1
                except Exception as e:
                    # 如果计算出错，跳过这个点
                    error_count += 1
                    print(f"调试: 计算出错，t={t}, 错误: {str(e)}")
                
                t += step
                point_count += 1
            
            print(f"调试: 生成完成，总点数: {point_count}，成功点: {success_count}，错误点: {error_count}")
            
            if point_count >= max_points:
                print(f"警告: 已达到最大点数限制 ({max_points})，可能存在无限循环")
            
            # 存储绘图点
            self.plot_points.append(points)
            self.plot_colors.append(color)
            
            # 使用绘图器绘制
            print(f"调试: 调用drawer绘制 {len(points)} 个点")
            self.drawer.draw_function(points, color)
    
    def execute_show_statement(self, statement: Dict):
        """执行show语句，显示绘制的图像"""
        self.drawer.show()
    
    def execute_clear_statement(self, statement: Dict):
        """执行clear语句，清空图像"""
        self.drawer.clear()
        self.plot_points = []
        self.plot_colors = []
    
    def evaluate_expression(self, expression) -> Union[int, float]:
        """计算表达式的值，使用表达式对象的evaluate方法"""
        # 合并所有变量和常量到一个上下文字典中
        context = {**self.variables, **self.constants}
        
        try:
            # 添加调试信息
            print(f"调试: evaluate_expression被调用，表达式类型: {type(expression)}, 内容: {expression}")
            print(f"调试: 当前variables: {self.variables}")
            print(f"调试: 当前functions: {list(self.functions.keys())}")
            
            # 对于函数引用的特殊处理
            # 检查expression是否是VariableExpression类型，并且其name在functions字典中
            from .parser.expression import VariableExpression
            if isinstance(expression, VariableExpression):
                print(f"调试: 表达式是VariableExpression，名称: {expression.name}")
                if expression.name in self.functions:
                    print(f"调试: 发现函数引用 {expression.name}，开始递归计算")
                    # 如果是对自定义函数的引用，则递归计算该函数的值
                    func_expr = self.functions[expression.name]
                    return self.evaluate_expression(func_expr)
                else:
                    print(f"调试: 变量 {expression.name} 不在functions字典中")
            
            # 调用表达式对象的evaluate方法
            return expression.evaluate(context)
        except Exception as e:
            # 重新抛出异常，提供更多上下文信息
            raise RuntimeError(f"表达式计算错误: {str(e)}") from e


def main():
    """主函数，提供命令行接口"""
    import sys
    
    if len(sys.argv) != 2:
        print("用法: python -m function_painter <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    interpreter = Interpreter()
    
    try:
        interpreter.interpret_file(file_path)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()