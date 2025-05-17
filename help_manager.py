import wx

class HelpManager:
    def __init__(self, parent, colors):
        """初始化帮助管理器
        
        Args:
            parent: 父窗口对象
            colors: 颜色方案字典
        """
        self.parent = parent
        self.colors = colors
        # 修改字体为20号
        self.font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑")
        self.current_language = "cn"  # 默认中文
        
        # 定义帮助文本
        self.help_content = {
            "cn": {
                "title": "操作帮助",
                "text": """
操作说明：
1. 在主界面可以看到当前日期和时间
2. 右上角的⚙按钮用于打开设置菜单
3. 在设置菜单中可以：
   - 选择关机时间（小时和分钟）
   - 选择重复的星期（可多选）
   - 点击确定保存设置，点击取消放弃更改
4. 设置完成后：
   - 左上角会显示⚠图标表示定时关机已启用
   - 主界面会显示设置的关机时间和重复星期
5. 关机提醒：
   - 关机前10分钟会弹出第一次提醒
   - 关机前1分钟会弹出最后警告
6. 右上角的中文/EN按钮可以切换界面语言
7. 顶部菜单的"帮助"提供操作说明和关于信息
"""
            },
            "en": {
                "title": "Help",
                "text": """
Instructions:
1. The main interface shows current date and time
2. Click ⚙ button in top right to open settings
3. In settings menu you can:
   - Select shutdown time (hour and minute)
   - Select repeat days (multiple selection)
   - Click OK to save or Cancel to discard
4. After setting:
   - ⚠ icon in top left indicates auto shutdown is enabled
   - Main interface shows shutdown time and repeat days
5. Shutdown warnings:
   - First warning 10 minutes before shutdown
   - Final warning 1 minute before shutdown
6. Click 中文/EN button to switch language
7. Help menu in top bar provides instructions and about info
"""
            }
        }
        
        # 定义关于文本
        self.about_content = {
            "cn": {
                "title": "关于",
                "text": """
定时关机助手 v1.0.0

功能特点：
• 精确的定时关机功能
• 支持每周重复定时
• 双语界面（中文/英文）
• 关机前10分钟和1分钟预警提醒
• 自动保存语言偏好设置

技术信息：
• 开发语言：Python 3.10
• GUI框架：wxPython 4.2
• 开发者：bjkbj@outlook.com
• 发布日期：2024-05-17

版权所有 © 2024 
保留所有权利
"""
            },
            "en": {
                "title": "About",
                "text": """
Auto Shutdown Assistant v1.0.0

Features:
• Precise timed shutdown
• Weekly schedule support
• Bilingual interface (CN/EN)
• 10-min and 1-min shutdown warnings
• Auto-save language preference

Technical Info:
• Language: Python 3.10
• GUI Framework: wxPython 4.2
• Developer: bjkbj@outlook.com
• Release Date: 2024-05-17

Copyright © 2024
All rights reserved
"""
            }
        }
    
    def show_help(self):
        """显示帮助窗口"""
        dialog = wx.MessageDialog(
            self.parent,
            self.help_content[self.current_language]["text"],
            self.help_content[self.current_language]["title"],
            wx.OK | wx.ICON_INFORMATION
        )
        # 设置对话框字体
        dialog.SetFont(self.font)
        dialog.ShowModal()
        dialog.Destroy()
    
    def show_about(self):
        """显示关于窗口"""
        dialog = wx.MessageDialog(
            self.parent,
            self.about_content[self.current_language]["text"],
            self.about_content[self.current_language]["title"],
            wx.OK | wx.ICON_INFORMATION
        )
        # 设置对话框字体
        dialog.SetFont(self.font)
        dialog.ShowModal()
        dialog.Destroy()
    
    def set_language(self, lang):
        """设置当前语言"""
        self.current_language = lang