import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import webbrowser
import subprocess

# 获取脚本所在目录的绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_absolute_path(*paths):
    """构建基于脚本目录的绝对路径"""
    return os.path.join(SCRIPT_DIR, *paths)


# 创建必要的目录结构
def create_directories():
    """创建程序运行所需的目录结构"""

    # 端口检查目录
    port_dir = get_absolute_path("端口检查")
    if not os.path.exists(port_dir):
        os.makedirs(get_absolute_path("端口检查", "检查前"))
        os.makedirs(get_absolute_path("端口检查", "检查后"))

    # 文件检查目录
    file_dir = get_absolute_path("文件检查")
    if not os.path.exists(file_dir):
        os.makedirs(get_absolute_path("文件检查", "检查前"))
        os.makedirs(get_absolute_path("文件检查", "检查后"))

    # 创建空文件占位
    for dir_type in ["端口检查", "文件检查"]:
        for check_type in ["检查前", "检查后"]:
            file_path = get_absolute_path(dir_type, check_type, "1.txt")
            if not os.path.exists(file_path):
                open(file_path, 'w').close()


# 端口检查功能
def port_check():
    """执行端口检查并生成报告"""

    print("开始端口检查...")

    # 使用绝对路径定义文件位置
    port_before_file = get_absolute_path("端口检查", "检查前", "1.txt")
    port_after_file = get_absolute_path("端口检查", "检查后", "1.txt")
    result_file = get_absolute_path("端口检查", "result.txt")
    html_file = get_absolute_path("端口检查", "result_for_port.html")

    # 生成端口检查前的快照
    #subprocess.run(f"netstat -ano > \"{port_before_file}\"", shell=True)

    # 提示用户进行某些操作
    messagebox.showinfo("提示", "请进行您需要监控的操作，完成后点击确定继续")

    # 生成端口检查后的快照
    subprocess.run(f"netstat -ano > \"{port_after_file}\"", shell=True)

    # 比较差异
    try:
        with open(port_before_file, 'r') as f1:
            set1 = set(f1.read().splitlines())
    except FileNotFoundError:
        set1 = set()

    try:
        with open(port_after_file, 'r') as f2:
            set2 = set(f2.read().splitlines())
    except FileNotFoundError:
        set2 = set()

    # 计算差异
    diff = set2 - set1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if diff:
        # 写入文本结果
        with open(result_file, 'w', encoding='utf-8') as f_out:
            f_out.write(f"端口变动检测报告 - {current_time}\n")
            f_out.write("=" * 50 + "\n")
            f_out.write('\n'.join(diff))

        # 生成HTML报告
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>端口变动报告</title>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .port-item {{ padding: 5px; border-bottom: 1px solid #eee; }}
                .timestamp {{ color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h1>端口变动检测报告</h1>
            <p class="timestamp">检测时间: {current_time}</p>
            <div id="results">
                {"".join(f'<div class="port-item">{item}</div>' for item in diff)}
            </div>
        </body>
        </html>
        """

        with open(html_file, 'w', encoding='utf-8') as f_html:
            f_html.write(html_content)

        # 在浏览器中打开报告
        try:
            webbrowser.open(f"file://{html_file}")
            messagebox.showinfo("完成", f"发现 {len(diff)} 处端口变动，报告已生成")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开报告: {str(e)}")
    else:
        messagebox.showinfo("完成", "没有发现新的端口变动")


# 文件检查功能
def file_check():
    """执行文件检查并生成报告"""

    print("开始文件检查...")

    # 使用绝对路径定义文件位置
    file_before_file = get_absolute_path("文件检查", "检查前", "1.txt")
    file_after_file = get_absolute_path("文件检查", "检查后", "1.txt")
    result_file = get_absolute_path("文件检查", "result.txt")
    html_file = get_absolute_path("文件检查", "result_for_dir.html")

    # 生成文件检查前的快照
    #subprocess.run(f"dir /s /b > \"{file_before_file}\"", shell=True)

    # 提示用户进行某些操作
    messagebox.showinfo("提示", "请进行您需要监控的文件操作，完成后点击确定继续")

    # 生成文件检查后的快照
    subprocess.run(f"dir /s /b > \"{file_after_file}\"", shell=True)

    # 比较差异
    try:
        with open(file_before_file, 'r') as f1:
            set1 = set(f1.read().splitlines())
    except FileNotFoundError:
        set1 = set()

    try:
        with open(file_after_file, 'r') as f2:
            set2 = set(f2.read().splitlines())
    except FileNotFoundError:
        set2 = set()

    # 计算差异
    diff = set2 - set1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if diff:
        # 写入文本结果
        with open(result_file, 'w', encoding='utf-8') as f_out:
            f_out.write(f"文件变动检测报告 - {current_time}\n")
            f_out.write("=" * 50 + "\n")
            f_out.write('\n'.join(diff))

        # 生成HTML报告
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>文件变动报告</title>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .file-item {{ padding: 5px; border-bottom: 1px solid #eee; }}
                .timestamp {{ color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <h1>文件变动检测报告</h1>
            <p class="timestamp">检测时间: {current_time}</p>
            <div id="results">
                {"".join(f'<div class="file-item">{item}</div>' for item in diff)}
            </div>
        </body>
        </html>
        """

        with open(html_file, 'w', encoding='utf-8') as f_html:
            f_html.write(html_content)

        # 在浏览器中打开报告
        try:
            webbrowser.open(f"file://{html_file}")
            messagebox.showinfo("完成", f"发现 {len(diff)} 处文件变动，报告已生成")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开报告: {str(e)}")
    else:
        messagebox.showinfo("完成", "没有发现新的文件变动")


# 一键检查功能
def all_check():
    """同时执行端口和文件检查"""

    print("开始一键检查...")

    # 执行端口检查
    port_check()

    # 执行文件检查
    file_check()

    # 合并结果
    merge_results()


# 合并结果功能
def merge_results():
    """合并端口和文件检查结果"""

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 读取端口检查结果
    port_result = ""
    port_file = get_absolute_path("端口检查", "result.txt")
    if os.path.exists(port_file):
        with open(port_file, 'r', encoding='utf-8') as f:
            port_result = f.read()

    # 读取文件检查结果
    file_result = ""
    file_file = get_absolute_path("文件检查", "result.txt")
    if os.path.exists(file_file):
        with open(file_file, 'r', encoding='utf-8') as f:
            file_result = f.read()

    # 写入合并的文本结果
    result_file = get_absolute_path("all_result.txt")
    with open(result_file, 'w', encoding='utf-8') as f_out:
        f_out.write(f"综合检测报告 - {current_time}\n\n")
        f_out.write("=" * 50 + "\n")
        f_out.write("端口变动:\n")
        f_out.write(port_result if port_result else "无端口变动\n")
        f_out.write("\n" + "=" * 50 + "\n")
        f_out.write("文件变动:\n")
        f_out.write(file_result if file_result else "无文件变动\n")

    # 生成合并的HTML报告
    html_file = get_absolute_path("all_result.html")
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>综合检测报告</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ color: #333; }}
            .item {{ padding: 5px; border-bottom: 1px solid #eee; }}
            .timestamp {{ color: #666; font-size: 0.9em; }}
            .section {{ margin-bottom: 30px; }}
        </style>
    </head>
    <body>
        <h1>综合检测报告</h1>
        <p class="timestamp">检测时间: {current_time}</p>

        <div class="section">
            <h2>端口变动</h2>
            <div id="port-results">
                {port_result.replace('\n', '<br>') if port_result else '无端口变动'}
            </div>
        </div>

        <div class="section">
            <h2>文件变动</h2>
            <div id="file-results">
                {file_result.replace('\n', '<br>') if file_result else '无文件变动'}
            </div>
        </div>
    </body>
    </html>
    """

    with open(html_file, 'w', encoding='utf-8') as f_html:
        f_html.write(html_content)

    # 在浏览器中打开报告
    try:
        webbrowser.open(f"file://{html_file}")
    except Exception as e:
        messagebox.showerror("错误", f"无法打开综合报告: {str(e)}")


# 创建GUI界面
def create_gui():
    """创建图形用户界面"""

    # 创建主窗口
    root = tk.Tk()
    root.title("系统监控工具")

    # 设置窗口大小和位置
    window_width = 300
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 添加标题标签
    title_label = tk.Label(root, text="请选择监控类型", font=("Arial", 14))
    title_label.pack(pady=10)

    # 添加按钮
    port_button = tk.Button(root, text="端口检查", command=port_check, width=20)
    port_button.pack(pady=5)

    file_button = tk.Button(root, text="文件检查", command=file_check, width=20)
    file_button.pack(pady=5)

    all_button = tk.Button(root, text="一键检查", command=all_check, width=20)
    all_button.pack(pady=5)

    # 运行主循环
    root.mainloop()


# 主函数
def main():
    """程序入口"""

    # 创建必要的目录结构
    create_directories()

    # 创建GUI界面
    create_gui()


if __name__ == "__main__":
    main()