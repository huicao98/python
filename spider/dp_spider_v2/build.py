import PyInstaller.__main__
import os

if __name__ == '__main__':
    PyInstaller.__main__.run([
        'dp_spider_main.py',  # 替换为你的主应用程序脚本
        '--onefile',        # 打包为单个可执行文件
        '--windowed',       # 创建一个窗口应用程序而不是命令行应用程序
        '--name=dp_spider120',  # 指定应用程序的名称
        '--add-binary=chromedriver.exe;.' # 使用逗号分隔文件路径和目标路径
    ])
