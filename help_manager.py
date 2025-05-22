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
1. 主界面功能：
   - 顶部显示当前日期（YYYY/MM/DD格式）
   - 中部显示实时时间（HH:MM:SS格式）
   - 底部显示定时关机设置信息

2. 界面控制：
   - 右上角的⚙按钮：打开设置菜单
   - 右上角的中文/EN按钮：切换中英文界面
   - 左上角的⚠图标：表示定时关机已启用
   - 顶部菜单栏：提供帮助和关于信息

3. 设置功能：
   - 时间设置：
     • 可选择0-23小时
     • 可选择0-59分钟
   - 重复设置：
     • 可选择一周中的任意天数
     • 默认选中周一到周五
   - 设置保存：
     • 点击确定保存设置
     • 关闭窗口取消更改

4. 关机提醒：
   - 首次提醒：关机前10分钟弹出系统通知
   - 最终提醒：关机前1分钟弹出系统通知
   - 关机执行：到达设定时间自动关机

5. 数据保存：
   - 自动保存语言偏好设置
   - 自动保存关机时间设置
   - 自动保存重复日期设置

6. 安全保护：
   - 关机前会预留60秒供用户保存工作
   - 可随时通过设置取消定时关机
"""
            },
            "en": {
                "title": "Help",
                "text": """
Instructions:
1. Main Interface:
   - Top: Current date (YYYY/MM/DD format)
   - Middle: Real-time clock (HH:MM:SS format)
   - Bottom: Shutdown timer settings info

2. Interface Controls:
   - ⚙ button (top right): Open settings
   - 中文/EN button (top right): Switch language
   - ⚠ icon (top left): Timer active indicator
   - Top menu bar: Help and About info

3. Settings:
   - Time Selection:
     • Hours: 0-23 available
     • Minutes: 0-59 available
   - Repeat Selection:
     • Any days of week selectable
     • Monday to Friday by default
   - Settings Control:
     • Click OK to save
     • Close window to cancel

4. Shutdown Alerts:
   - First alert: 10 minutes before
   - Final alert: 1 minute before
   - Auto shutdown: At set time

5. Data Persistence:
   - Auto-save language preference
   - Auto-save shutdown time
   - Auto-save repeat days

6. Safety Features:
   - 60-second grace period before shutdown
   - Timer can be cancelled anytime
"""
            }
        }
        
        # 定义关于文本
        self.about_content = {
            "cn": {
                "title": "关于",
                "text": """
定时关机助手 v1.0.3

功能特点：
• 精确的定时关机功能
• 支持每周重复定时
• 双语界面（中文/英文）
• 关机前10分钟和1分钟预警提醒
• 自动保存语言偏好设置

更新说明：
v1.0.3
- 优化设置窗口的错误处理
- 改进空设置的保存逻辑
- 提升程序稳定性

v1.0.2
- 修复语言切换问题
- 优化界面显示效果

v1.0.1
- 初始版本发布

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
Auto Shutdown Assistant v1.0.3

Features:
• Precise timed shutdown
• Weekly schedule support
• Bilingual interface (CN/EN)
• 10-min and 1-min shutdown warnings
• Auto-save language preference

Update Notes:
v1.0.3
- Optimized settings window error handling
- Improved empty settings save logic
- Enhanced program stability

v1.0.2
- Fixed language switching issues
- Optimized interface display

v1.0.1
- Initial release

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