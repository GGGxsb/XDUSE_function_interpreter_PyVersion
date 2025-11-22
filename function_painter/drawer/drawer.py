import matplotlib
# 设置matplotlib使用TkAgg后端，确保能显示图像窗口
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
import numpy as np
import sys


class Drawer:
    """绘图模块"""
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.setup_plot()
        self.plot_count = 0
        self.color_map = {
            'red': 'r',
            'blue': 'b', 
            'green': 'g',
            'yellow': 'y',
            'purple': 'purple',
            'orange': 'orange',
            'cyan': 'c',
            'magenta': 'm'
        }
        # 确保图像窗口在前台显示
        self.fig.canvas.manager.window.attributes('-topmost', True)
    
    def setup_plot(self):
        """设置绘图环境"""
        self.ax.set_title('函数绘图')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        # 设置坐标轴范围自适应
        self.ax.autoscale(True)
    
    def draw_function(self, points: List[Tuple[float, float]], color: Optional[str] = None):
        """绘制函数曲线"""
        print(f"调试: draw_function被调用，收到 {len(points)} 个点")
        if not points:
            print("警告: 没有有效的数据点可供绘制")
            return
        
        # 显示前几个点作为示例
        print(f"调试: 前5个点示例: {points[:5]}")
        
        # 分离x和y坐标
        x_values = [x for x, y in points]
        y_values = [y for x, y in points]
        
        # 打印数据范围
        print(f"调试: x值范围: {min(x_values)} 到 {max(x_values)}")
        print(f"调试: y值范围: {min(y_values)} 到 {max(y_values)}")
        
        # 验证数据有效性
        x_values = np.array(x_values)
        y_values = np.array(y_values)
        
        # 过滤无效数据
        valid_mask = np.isfinite(x_values) & np.isfinite(y_values)
        x_values = x_values[valid_mask]
        y_values = y_values[valid_mask]
        
        print(f"调试: 过滤后有效点数量: {len(x_values)}")
        
        if len(x_values) == 0:
            print("警告: 所有数据点都无效")
            return
        
        # 处理颜色
        plot_color = self._get_color(color)
        print(f"调试: 使用颜色: {plot_color}")
        
        # 绘制曲线
        print(f"调试: 准备调用matplotlib绘制曲线")
        self.ax.plot(x_values, y_values, color=plot_color, linewidth=2, label=f'曲线 {self.plot_count + 1}')
        self.plot_count += 1
        print(f"调试: 绘制完成，当前已绘制 {self.plot_count} 条曲线")
        
        # 更新图例
        self.ax.legend(loc='best')
        print(f"调试: 图例已更新")
    
    def _get_color(self, color_name: Optional[str]) -> str:
        """获取有效的颜色值"""
        if color_name and color_name.lower() in self.color_map:
            return self.color_map[color_name.lower()]
        # 如果没有指定有效颜色，则使用自动颜色循环
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        return colors[self.plot_count % len(colors)]
    
    def show(self):
        """显示图像"""
        print(f"调试: 准备显示图像，已绘制 {self.plot_count} 条曲线")
        # 设置中文字体以避免中文显示警告
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.tight_layout()
        # 强制显示图像窗口并保持阻塞，直到用户关闭窗口
        print(f"调试: 调用plt.show()显示图像")
        plt.show(block=True)
    
    def clear(self):
        """清空图像"""
        self.ax.clear()
        self.setup_plot()
        self.plot_count = 0
    
    def save_figure(self, file_path: str):
        """保存图像到文件"""
        self.fig.savefig(file_path)
    
    def close(self):
        """关闭绘图窗口"""
        plt.close(self.fig)