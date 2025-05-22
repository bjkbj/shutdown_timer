import wx
import os
from time import strftime, time, localtime
from help_manager import HelpManager
from settings_manager import SettingsManager

# 禁用sizer一致性检查（不推荐）
wx.SIZER_FLAGS_CONSISTENCY_CHECK = False

class MainFrame(wx.Frame):
    def __init__(self):
        # 修改窗口大小为500x400
        super().__init__(parent=None, title='时间与自动关机', size=(500, 400))
        
        # 定义统一的颜色方案
        self.colors = {
            'bg': '#ffffff',          # 纯白背景
            'text': '#333333',        # 深灰文字
            'accent': '#1a73e8',      # Google蓝作为强调色
            'warning': '#dc3545',     # 警告红色
            'hover': '#f8f9fa'        # 悬停背景色
        }
        
        # 定义统一的字体
        self.fonts = {
            'large': wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑"),
            'normal': wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑"),
            'small': wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑"),
            'icon': wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑"),
            'button': wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑")
        }
        
        # 创建主面板
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(self.colors['bg'])
        
        # 初始化所有管理器 - 删除 config_manager
        self.help_manager = HelpManager(self, self.colors)
        self.settings_manager = SettingsManager(self, self.colors)
        
        # 创建日期和时间标签的字体
        font = wx.Font(36, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑")
        
        # 创建所有显示标签
        window_width = 500  # 更新窗口宽度
        
        # 创建日期标签
        self.date_label = wx.StaticText(self.panel, label="", pos=(0, 100), size=(window_width, -1), 
                                  style=wx.ALIGN_CENTER_HORIZONTAL)
        self.date_label.SetFont(self.fonts['large'])  # 使用36号字体
        self.date_label.SetForegroundColour('#1a73e8')  # Google蓝色
        
        # 创建时间标签
        self.time_label = wx.StaticText(self.panel, label="", pos=(0, 160), size=(window_width, -1), 
                                  style=wx.ALIGN_CENTER_HORIZONTAL)
        self.time_label.SetFont(self.fonts['large'])  # 使用36号字体
        self.time_label.SetForegroundColour('#1a73e8')  # Google蓝色
        
        # 创建关机时间标签
        self.shutdown_time_display = wx.StaticText(self.panel, label="", pos=(0, 220), size=(window_width, -1),
                                             style=wx.ALIGN_CENTER_HORIZONTAL)
        self.shutdown_time_display.SetForegroundColour('#dc3545')  # 设置为红色
        
        # 创建星期显示标签
        self.weekday_display = wx.StaticText(self.panel, label="", pos=(0, 245), size=(window_width, -1),
                                       style=wx.ALIGN_CENTER_HORIZONTAL)
        self.weekday_display.SetForegroundColour('#dc3545')  # 设置为红色
        
        # 创建菜单栏
        menubar = wx.MenuBar()
        
        # 创建help菜单
        help_menu = wx.Menu()
        
        # 创建更大的字体以实现80px高度
        menu_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="微软雅黑")
        
        # 添加help菜单项并保存引用
        help_item = help_menu.Append(wx.ID_HELP, "操作帮助")
        about_item = help_menu.Append(wx.ID_ABOUT, "关于")
        
        # 设置菜单项字体
        help_item.SetFont(menu_font)
        about_item.SetFont(menu_font)
        
        # 添加到菜单栏并保存为实例变量供后续使用
        menubar.Append(help_menu, "帮助")
        self.help_menu = help_menu
        self.help_item = help_item
        self.about_item = about_item
        
        # 设置菜单栏
        self.SetMenuBar(menubar)
        
        # 设置整个菜单栏的字体来控制高度
        menubar.SetOwnFont(menu_font)
        
        # 绑定菜单事件
        self.Bind(wx.EVT_MENU, self.on_help, id=wx.ID_HELP)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        
        # 设置警告状态标签和提示框
        self.shutdown_status = wx.StaticText(self.panel, label="⚠", pos=(10, 10), size=(48, 48))
        self.shutdown_status.SetForegroundColour('red')
        self.shutdown_status.SetFont(self.fonts['icon'])
        self.shutdown_status.Hide()
        
        # 创建并设置提示框
        self.tooltip = wx.ToolTip("")
        self.shutdown_status.SetToolTip(self.tooltip)
        
        # 添加语言切换按钮
        self.lang_toggle = wx.ToggleButton(self.panel, label="中文", pos=(380, 10), size=(50, 30),
                                       style=wx.NO_BORDER|wx.TRANSPARENT_WINDOW)
        
        # 从shutdown_settings.json读取语言设置
        from setting_data import shutdown_settings
        saved_language = shutdown_settings.get_language()
        is_chinese = saved_language == "cn"
        self.lang_toggle.SetValue(is_chinese)
        self.lang_toggle.SetLabel("中文" if is_chinese else "EN")
        self.lang_toggle.SetFont(self.fonts['small'])
        self.lang_toggle.SetBackgroundColour(self.colors['bg'])  # 设置背景色为白色
        self.lang_toggle.Bind(wx.EVT_TOGGLEBUTTON, self.on_language_change)
        
        # 添加鼠标悬停效果
        self.lang_toggle.Bind(wx.EVT_ENTER_WINDOW, 
            lambda evt: self.lang_toggle.SetBackgroundColour(self.colors['hover']))
        self.lang_toggle.Bind(wx.EVT_LEAVE_WINDOW, 
            lambda evt: self.lang_toggle.SetBackgroundColour(self.colors['bg']))
        
        # 修改设置按钮
        self.settings_btn = wx.Button(self.panel, wx.ID_ANY, label="⚙", pos=(440, 0), size=(48, 48), 
                       style=wx.NO_BORDER|wx.TRANSPARENT_WINDOW)
        self.settings_btn.SetFont(self.fonts['button'])
        self.settings_btn.SetBackgroundColour(self.colors['bg'])
        self.settings_btn.SetForegroundColour(self.colors['text'])
        # 绑定设置按钮点击事件
        self.settings_btn.Bind(wx.EVT_BUTTON, self.show_settings)
        
        # 添加鼠标悬停效果
        self.settings_btn.Bind(wx.EVT_ENTER_WINDOW, 
            lambda evt: self.settings_btn.SetBackgroundColour(self.colors['hover']))
        self.settings_btn.Bind(wx.EVT_LEAVE_WINDOW, 
            lambda evt: self.settings_btn.SetBackgroundColour(self.colors['bg']))
        
        # 初始化变量
        self.shutdown_time = None
        self.settings_dialog = None
        self.is_settings_open = False
        self.notification_shown = False  # 添加通知显示标志
        
        # 初始化界面语言 - 确保所有UI元素都已创建
        self._update_language(is_chinese)
        
        # 启动时钟更新
        self.update_clock()
        
        # 显示窗口
        self.Center()
        self.Show()
        
        
    
    def update_clock(self):
        """更新时钟显示"""
        try:
            # 更新日期和时间显示
            current_date = strftime('%Y/%m/%d')
            self.date_label.SetLabel(current_date)
            current_time = strftime('%H:%M:%S')
            self.time_label.SetLabel(current_time)
            
            # 从 shutdown_settings.json 读取设置
            from setting_data import shutdown_settings
            saved_time, saved_days = shutdown_settings.get_settings()
            
            # 如果有设定的时间和星期，更新显示
            if saved_time and saved_days:
                # 获取当前语言设置
                is_chinese = self.lang_toggle.GetValue()
                
                # 显示关机时间
                if is_chinese:
                    shutdown_text = f"关机时间设置为: {saved_time[0]:02d}:{saved_time[1]:02d}"
                else:
                    shutdown_text = f"Shutdown time set to: {saved_time[0]:02d}:{saved_time[1]:02d}"
                self.shutdown_time_display.SetLabel(shutdown_text)
                
                # 显示选中的星期
                if is_chinese:
                    weekdays = ['一', '二', '三', '四', '五', '六', '日']
                    selected_weekdays = [f"周{weekdays[i]}" for i in saved_days]
                    weekday_text = f"选中的星期: {', '.join(selected_weekdays)}"
                else:
                    weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
                    selected_weekdays = [weekdays[i] for i in saved_days]
                    weekday_text = f"Repeat on: {', '.join(selected_weekdays)}"
                self.weekday_display.SetLabel(weekday_text)
                
                # 显示关机状态图标
                self.shutdown_status.Show()
                
                # 获取当前时间
                current_time = localtime()
                current_hours = int(strftime('%H', current_time))
                current_minutes = int(strftime('%M', current_time))
                current_weekday = int(strftime('%w', current_time)) - 1  # 转换为0-6的范围
                if current_weekday == -1:  # 处理周日的情况
                    current_weekday = 6
                    
                # 计算剩余时间（分钟）
                remaining_minutes = (saved_time[0] - current_hours) * 60 + (saved_time[1] - current_minutes)
                if remaining_minutes < 0:
                    remaining_minutes += 24 * 60  # 如果是第二天的时间，加上24小时
                
                # 先判断星期是否匹配
                if current_weekday in saved_days:
                    # 检查是否需要显示10分钟警告
                    if remaining_minutes == 10 and not self.notification_shown:
                        # 创建并显示Windows通知
                        from winotify import Notification
                        
                        # 根据语言设置显示不同的通知消息
                        if is_chinese:
                            title = "关机提醒"
                            message = "系统将在10分钟后关机，请注意保存您的工作！"
                        else:
                            title = "Shutdown Warning"
                            message = "System will shutdown in 10 minutes. Please save your work!"
                        
                        # 创建通知
                        toast = Notification(
                            app_id="自动关机程序",
                            title=title,
                            msg=message,
                            duration="short"
                        )
                        toast.show()
                        self.notification_shown = True
                    
                    # 如果剩余时间不是10分钟，重置通知标志
                    elif remaining_minutes != 10:
                        self.notification_shown = False
                    
                    # 再判断时间是否相同
                    if saved_time[0] == current_hours and saved_time[1] == current_minutes:
                        # 执行关机命令（增加60秒延迟给用户最后保存的机会）
                        os.system("shutdown /s /t 60")
            else:
                # 如果没有设定时间和星期，清除显示
                self.shutdown_time_display.SetLabel("")
                self.weekday_display.SetLabel("")
                self.shutdown_status.Hide()
            
            # 每秒更新一次
            wx.CallLater(1000, self.update_clock)
        except Exception as e:
            wx.MessageBox(
                f"时钟更新出错：{str(e)}",
                "错误",
                wx.OK | wx.ICON_ERROR
            )
    


    def on_help(self, event):
        """显示帮助窗口"""
        self.help_manager.show_help()
    
    def on_about(self, event):
        """显示关于窗口"""
        self.help_manager.show_about()
    
    def show_settings(self, event):
        """显示设置对话框"""
        if self.is_settings_open:
            return
        
        self.is_settings_open = True
        
        try:
            self.settings_manager.set_shutdown_status(self.shutdown_status)
            self.settings_manager.set_displays(self.shutdown_time_display, self.weekday_display)
            self.settings_dialog = self.settings_manager.show_settings()
        except:
            # 静默处理错误，不显示错误提示
            pass
        finally:
            self.is_settings_open = False
            self.settings_manager.current_dialog = None

    def on_language_change(self, event):
        """语言切换事件处理"""
        is_chinese = self.lang_toggle.GetValue()
        new_lang = "cn" if is_chinese else "en"
        self.settings_manager.set_language(new_lang)  # 保存语言设置
        # 更新界面语言
        self._update_language(is_chinese)
    
    def _update_language(self, is_chinese):
        """更新界面语言"""
        menubar = self.GetMenuBar()
        
        if is_chinese:
            # 中文显示
            self.lang_toggle.SetLabel("中文")
            self.SetTitle('时间与自动关机')
            
            # 更新菜单项文本
            self.help_item.SetItemLabel("操作帮助")
            self.about_item.SetItemLabel("关于")
            menubar.SetMenuLabel(0, "帮助")
            
            # 更新关机状态提示
            self.tooltip.SetTip("定时关机已启用")
            
            # 更新设置界面文本
            settings_dialog = self.settings_manager.get_current_dialog()
            if settings_dialog:
                settings_dialog.SetTitle("定时关机设置")
        
            # 更新帮助管理器的语言
            self.help_manager.set_language("cn")
            
            # 更新显示文本
            if self.shutdown_time_display.GetLabel():
                hours = self.settings_manager.selected_hour
                minutes = self.settings_manager.selected_minute
                self.shutdown_time_display.SetLabel(f"关机时间设置为: {hours:02d}:{minutes:02d}")
        
            # 更新星期显示
            selected_days = self.settings_manager.get_selected_days()
            if selected_days and self.weekday_display.GetLabel():
                weekdays = ['一', '二', '三', '四', '五', '六', '日']
                selected_weekdays = [f"周{weekdays[i]}" for i in selected_days]
                self.weekday_display.SetLabel(f"选中的星期: {', '.join(selected_weekdays)}")
        else:
            # 英文显示
            self.lang_toggle.SetLabel("EN")
            self.SetTitle('Time and Auto Shutdown')
            
            # 更新菜单项文本
            self.help_item.SetItemLabel("Help")
            self.about_item.SetItemLabel("About")
            menubar.SetMenuLabel(0, "Help")
            
            # 更新关机状态提示
            self.tooltip.SetTip("Auto shutdown enabled")
            
            # 更新设置界面文本
            settings_dialog = self.settings_manager.get_current_dialog()
            if settings_dialog:
                settings_dialog.SetTitle("Shutdown Settings")
        
            # 更新帮助管理器的语言
            self.help_manager.set_language("en")
            
            # 更新显示文本
            if self.shutdown_time_display.GetLabel():
                hours = self.settings_manager.selected_hour
                minutes = self.settings_manager.selected_minute
                self.shutdown_time_display.SetLabel(f"Shutdown time set to: {hours:02d}:{minutes:02d}")
        
            # 更新星期显示
            selected_days = self.settings_manager.get_selected_days()
            if selected_days and self.weekday_display.GetLabel():
                weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
                selected_weekdays = [weekdays[i] for i in selected_days]
                self.weekday_display.SetLabel(f"Repeat on: {', '.join(selected_weekdays)}")

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
